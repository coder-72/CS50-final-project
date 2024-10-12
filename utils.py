import sqlite3 

conn = sqlite3.connect("blog.db")
cursor = conn.cursor()

def get_post(id:int):
    cursor.execute("SELECT * FROM posts WHERE id = ? LIMIT 1 ORDER BY date DESC", (id))
    result = cursor.fetchall()
    if len(result) == 1:
        result = result[0]
    else:
        raise Exception("get_post returned more than 1 post")
    return result
    