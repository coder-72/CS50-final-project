import sqlite3 
from datetime import datetime
import markdown2
from bs4 import BeautifulSoup as bs

def get_post(post_id: int):
    conn = sqlite3.connect('blog.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM posts WHERE id = ? LIMIT 1", (post_id,))
    post = cursor.fetchone()
    print(post)

    cursor.close()
    conn.close()

    return post

def add_post(title, subtitle, image, date, content):
    conn = sqlite3.connect('blog.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("INSERT INTO posts (title, subtitle, image, date, content) VALUES (?, ?, ?, ?, ?)", (title, subtitle, image, date, content))

    conn.commit()
    cursor.close()
    conn.close()


    
def format_date(date:str):
    date_obj = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    return date_obj.strftime("%a %d %b %Y")

def markdown_to_html(text:str):
    markup = markdown2.markdown(text,  extras=[
            "fenced-code-blocks",
            "tables",
            "strike",
            "smarty-pants",
            "highlightjs",
            "breaks"
        ])
    soup = bs(markup, "html.parser")
    headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
    for heading in headings:
        heading["class"] = ["section-heading"]

    blockquotes = soup.find_all(["blockquote"])
    for blockquote in blockquotes:
        blockquote["class"] = ["blockquote"]

    images = soup.find_all(["img"])
    for image in images:
        image["class"] = ["img-fluid"]

    links = soup.find_all(["a"])
    for link in links:
        link["target"] = ["_blank"]

    return soup


def get_previews(previews:int = 5):
    conn = sqlite3.connect('blog.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT id, title, subtitle, date FROM posts ORDER BY date DESC LIMIT ?", (previews, ))
    posts = cursor.fetchall()

    cursor.close()
    conn.close()

    html = ""

    for post in posts:
        html_block = f"""
                    <!-- Post preview-->
                    <div class="post-preview">
                        <a href="/post/{post["id"]}">
                            <h2 class="post-title">{post["title"]}</h2>
                            <h3 class="post-subtitle">{post["subtitle"]}</h3>
                        </a>
                        <p class="post-meta">
                            Posted
                            on {format_date(post["date"])}
                        </p>
                    </div>
                    <!-- Divider-->
                    <hr class="my-4" />
        """
        html += html_block

    return html

def get_time():
    now = datetime.now()
    time = now.strftime('%Y-%m-%d %H:%M:%S')
    return time

def search(query: str):
    conn = sqlite3.connect('blog.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM posts_fts WHERE posts_fts MATCH ? ORDER BY rank ASC LIMIT 20;", (query, ))
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results

def search_all():
    conn = sqlite3.connect('blog.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM posts ORDER BY date DESC LIMIT 20;")
    results = cursor.fetchall()
    print("called")
    print([dict(result) for result in results])
    cursor.close()
    conn.close()

    return results
