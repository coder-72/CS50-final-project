import sqlite3 
from datetime import datetime
import markdown2

def get_post(post_id):
    # Create a new connection for this thread
    conn = sqlite3.connect('blog.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM posts WHERE id = ? LIMIT 1", (post_id,))
    post = cursor.fetchone()
    print(post)

    # Close the cursor and connection
    cursor.close()
    conn.close()

    return post


    
def format_date(date:str):
    date_obj = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    return date_obj.strftime("%a %d %b %Y")

def markdown_to_html(text:str):
