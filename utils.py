import sqlite3 
from datetime import datetime
import markdown2
from bs4 import BeautifulSoup as bs
from protonmail import ProtonMail
from urllib.parse import urlparse
from flask import url_for, session, redirect
import bcrypt
from email_validator import validate_email, EmailNotValidError
from functools import wraps

def get_post(post_id: int):
    """
    gets all a post's info for displaying

    Params
    ------
        post_id : int
            id of post to get info for
        
    Returns
    -------
        post info : dictionary
            contains post info
    
    Raises
    ------
        SQL exception
            if the table or db don't exist
    """

    #open database connection and cursor
    conn = sqlite3.connect('blog.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    #execute sql statement
    cursor.execute("SELECT * FROM posts WHERE id = ? LIMIT 1", (post_id,))

    #get results
    post = cursor.fetchone()

    #close connection
    cursor.close()
    conn.close()

    return post

def add_post(title: str, subtitle: str, image: str, content: str):
    """
    Adds a new post to the  database

    Params
    ------
        title : str
            title of post to add
        subtitle : str
            subtitle of post to add
        image : str
            link to main header image of post
        content : str
            markdown syntax of post
    Returns
    -------
        nothing
    
    Raises
    ------
        SQL exception 
            if table or db don't exist

    """

    #open db connection and cursor
    conn = sqlite3.connect('blog.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    #get current date
    date = get_time()

    #insert post info into sql table (posts)
    cursor.execute("INSERT INTO posts (title, subtitle, image, date, content) VALUES (?, ?, ?, ?, ?)", (title, subtitle, image, date, content))

    #commit data before closing connection
    conn.commit()
    cursor.close()
    conn.close()


    
def format_date(date:str):
    """
    formats date into human readable form

    Params
    ------
        date : str
            date in form year-month-day hour:minute:second
    Returns
    -------
        date : str
            in human readable format
    """
    #convet date string to date object
    date_obj = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

    #return readable date
    return date_obj.strftime("%a %d %b %Y")

def markdown_to_html(text:str):
    """
    converts markdown to html with proper bootstrap classes for style

    Params
    -------
    text : str
        markdown to convert to html
    
    Returns
    -------
    html : text
        html with bootstrap classes

    Raises
    ------
        Non
    """

    #markup object created with extensions
    markup = markdown2.markdown(text,  extras=[
            "fenced-code-blocks",
            "tables",
            "strike",
            "smarty-pants",
            "break-on-newline",
            "footnotes",
            "task_list",
            "smarty-pants"
        ])
    
    # beautiful soup object for editing classes
    soup = bs(markup, "html.parser")

    #add headings class to all headings
    headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
    for heading in headings:
        heading["class"] = ["section-heading"]

    #add blockquotes bs class to blockquotes
    blockquotes = soup.find_all(["blockquote"])
    for blockquote in blockquotes:
        blockquote["class"] = ["blockquote"]

    #image bs class added to images
    images = soup.find_all(["img"])
    for image in images:
        image["class"] = ["img-fluid", "px-1"]

    #makes links target new windows
    links = soup.find_all(["a"])
    for link in links:
        link["target"] = ["_blank"]

    #adds bs table class to tables
    tables = soup.find_all(["table"])
    for table in tables:
        table["class"] = ["table"]

    #adds classes for code blocks
    old_code= soup.find_all("code")
    for block in old_code:
        contents = block.text
        new_pre = soup.new_tag("pre")
        new_code = soup.new_tag("code")
        new_code.string = contents
        new_code["class"] = ["language-auto"]
        new_pre.append(new_code)
        new_pre["class"] = ["line-numbers", "rounded"]
        block.replace_with(new_pre)

    #returns html with bs classes
    return soup



def get_previews(previews: int = 3) -> str:
    """
    gets html for preview of featured articles

    Params
    ------
    previews : int
        number of previews to get

    Returns
    -------
        html : str
            html to display previews
    
    Raises
    ------
        SQL exception
            if sql table or db don't exist
    """

    #make connection with database and open cursor
    conn = sqlite3.connect('blog.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    #execute sql and get results
    cursor.execute("SELECT id, title, subtitle, date, image FROM posts ORDER BY date DESC LIMIT ?", (previews,))
    posts = cursor.fetchall()

    #close cursor and connection
    cursor.close()
    conn.close()

    html = ""

    #loop through data appending html for preview of that data to html variable
    for post in posts:
        html_block = f"""
    <div class="col-md-4 d-flex align-items-stretch">
        <div class="card mb-4 shadow-sm w-100">
            <img src="{post['image']}" class="card-img-top" alt="Post {post['id']}">
            <div class="card-body d-flex flex-column h-100">
                <h5 class="card-title">{post['title']}</h5>
                <p class="card-text">{post['subtitle']}</p>
                <p class="card-date text-muted">{format_date(post['date'])}</p>
                <div class="mt-auto">
                    <a href="/post/{post["id"]}" class="btn btn-primary p-2">Read More</a>
                </div>
            </div>
        </div>
    </div>
        """
        html += html_block

    #return html for previews
    return html

def get_time():
    """
    gets current time in format year-month-day hour:minute:second

    Params
    -------
        Non
    
    Returns
    -------
        time : str
            time as string in format : year-month-day hour:minute:second
    """

    #get current date object
    now = datetime.now()

    #convert to string in correct format
    time = now.strftime('%Y-%m-%d %H:%M:%S')

    #return time
    return time

def search(query: str):
    """
    uses query to FTS search db and returns results

    Params
    ------
        q : str
            query to search for
    
    Returns
    -------
        results : list of dicts
            results of fts search
    
    Raises
    -------
        SQL exception 
            if db or table doesn't exist or sql query wrong
    """

    #open connection and cursor for database
    conn = sqlite3.connect('blog.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    #execute sql statement for query and get results
    cursor.execute("SELECT * FROM posts_fts WHERE posts_fts MATCH ? ORDER BY rank ASC LIMIT 20;", (query, ))
    results = cursor.fetchall()

    #close database connection and cursor
    cursor.close()
    conn.close()

    #returns results of full text search
    return results

def search_all():
    """
    get all posts without filter by date descsending

    Params
    ------
        non
    Returns
    -------
        results : list of dicts
            results of sql
    """

    #open connection and cursor with db
    conn = sqlite3.connect('blog.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    #execute sql statement and get all results
    cursor.execute("SELECT * FROM posts ORDER BY date DESC LIMIT 20;")
    results = cursor.fetchall()

    #close cursor and connection
    cursor.close()
    conn.close()

    #return results in descending order of date
    return results

def send_email(name: str, email: str, phone: str, message: str):
    emails = get_user_email()
    try:
        proton.load("session.pickle")
    except:
        username = "contact-travel-blog@protonmail.com"
        password = "GCTL6xiGUMq4*av"
        proton = ProtonMail()
        proton.login(username, password)
        proton.revoke_all_sessions()
        proton.save_session("session.pickle")

    html = f"""
    <html>
        <body>
            <h1 style="text-align: center;">CONTACT FORM</h1>
            <p>
                NAME: {name}
                <br>
                EMAIL: {email}
                <br>
                PHONE: {phone}
                <br>
            <p>
            <h2>Message</h2>
            <hr>
            <p>
            {message}
            </p>
        </body>
    </html>

    """
    message = proton.create_message(
        recipients=emails,
        subject="CONTACT",
        body=html
    )
    proton.send_message(message)


def valid_email(email):
    """
    checks for valid email

    Params
    -------
        email: str
            email to check validity of
    Returns
    -------
        email : str
            email in standard form
        None
            if email is invalid
    """

    #check for email invalid error
    try:
        return validate_email(email)["email"]
    except Exception:
        return None

def admin_articles():
    html = ""
    conn = sqlite3.connect('blog.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts ORDER BY date DESC")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    for article in results:
        html += f'''
            <div class="accordion-item">
              <h2 class="accordion-header" id="heading{article["id"]}">
                <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapse{article["id"]}" aria-expanded="true" aria-controls="collapse{article["id"]}">
                  {article['title']}
                </button>
              </h2>
              <div id="collapse{article["id"]}" class="accordion-collapse collapse" aria-labelledby="heading{article["id"]}" data-bs-parent="#accordion">
                <div class="accordion-body">
                  <strong>Description:</strong> {article["subtitle"]}<br>
                  <small class="text-muted">{format_date(article['date'])}</small>
                  <div class="my-2">
                    <button type="button" class="btn btn-danger mx-1 delete-button" data-delete-id="{article['id']}" data-delete-name="{article['title']}">Delete</button>
                    <a href="{url_for('admin.edit_post', post_id=article['id'])}" class="btn btn-warning mx-1">Edit</a>
                    <a href="{ url_for('posts', post_id=article['id']) }" class="btn btn-primary mx-1">View</a>
                  </div>
                </div>
              </div>
            </div>
            '''
    return html

def delete_post(id:int):
    conn = sqlite3.connect('blog.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("DELETE FROM posts WHERE id = ? LIMIT 1", (id, ))
    conn.commit()
    cursor.close()
    conn.close()

#chatgpt used
def allowed_file(filename):
    extensions = [".md", ".txt"]
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions

#chatgpt
def is_valid_url(url):
    parsed_url = urlparse(url)
    return all([parsed_url.scheme, parsed_url.netloc])

def update_post(id:int, title: str, subtitle: str, image: str, content: str):
    conn = sqlite3.connect('blog.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("UPDATE posts SET title = ?, subtitle = ?, image = ?, content = ? WHERE id = ? ", (title, subtitle, image, content, id))

    conn.commit()
    cursor.close()
    conn.close()

def get_user(user):
    conn = sqlite3.connect('blog.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (user,))
    users = cursor.fetchone()

    cursor.close()
    conn.close()

    return users

def login_required(func):
    @wraps(func)
    def decorate(*args, **kwargs):
        print("login")
        if session.get("user_id") is None:
            return redirect("/login")
        return func(*args, **kwargs)
    return decorate

def add_user(user, password, email):
    if valid_email(email.strip()):
        conn = sqlite3.connect('blog.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode("utf-8")
        cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (user, hash, validate_email(email.strip()).email))
        conn.commit()
        cursor.close()
        conn.close()
    else:
        raise TypeError("not a valid email adress")

def logged_in():
    if session.get("user_id") is None:
        return False
    else:
        return True
    
def get_user_email():
    conn = sqlite3.connect('blog.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users ;")
    users = cursor.fetchall()

    cursor.close()
    conn.close()

    emails = []
    for user in users:
        emails.append(user["email"])
    return emails
