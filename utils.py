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
    html = markdown2.markdown(text,  extras=[
            "fenced-code-blocks",
            "tables",
            "footnotes",
            "strike",
            "smarty-pants",
            "highlightjs",
            "breaks"
        ])
    print(html)
    return html


title = 'Discovering the Enchanting Streets of Paris'
subtitle = 'From Iconic Landmarks to Hidden Gems'
image = 'https://images.unsplash.com/photo-1502602898657-3e91760cbb34'
date = '2024-10-13 14:30:00'
content = """
## From Iconic Landmarks to Hidden Gems

*Written on October 13, 2024*

Paris, the City of Light, is renowned for its iconic landmarks, world-class museums, and charming neighborhoods. Whether you're visiting for the first time or returning to discover more of its secrets, there's always something new to explore. In this post, I’ll share my favorite places from my latest trip.

---

### 1. **Eiffel Tower** - The Heart of Paris

![Eiffel Tower](https://images.unsplash.com/photo-1568651768688-c21a3c3b154b)

No trip to Paris is complete without a visit to the Eiffel Tower. Standing tall at 324 meters, this architectural marvel offers breathtaking views of the city. I recommend visiting at night when the tower sparkles for five minutes every hour.

> **Pro Tip**: Skip the long lines by booking your tickets online in advance.

[Learn more about visiting the Eiffel Tower](https://www.toureiffel.paris/en).

---

### 2. **Le Marais** - A Historical Neighborhood Full of Charm

![Le Marais](https://images.unsplash.com/photo-1565631976670-fb1cdebfcf22)

Le Marais is a district that perfectly blends history, art, and modern life. As you stroll through its narrow streets, you’ll find trendy boutiques, art galleries, and charming cafes. The architecture, with its preserved medieval buildings, adds to the neighborhood's unique appeal.

> **Must-Visit**: Stop by the Place des Vosges, one of the oldest squares in Paris, for a peaceful moment amid the hustle and bustle.

---

### 3. **The Louvre** - Home to Masterpieces

![The Louvre](https://images.unsplash.com/photo-1517423440428-a5a00ad493e8)

The Louvre is not only the largest art museum in the world but also a historic monument. With over 38,000 pieces of art, including the Mona Lisa and the Venus de Milo, you can spend hours wandering through its galleries.

> **Tip**: Download the museum's app for a guided tour to enhance your visit.

[Plan your visit to The Louvre](https://www.louvre.fr/en).

---

### 4. **Montmartre** - Artistic Inspiration at Every Corner

![Montmartre](https://images.unsplash.com/photo-1513465785642-5a3f41ea3c90)

Perched on a hill in northern Paris, Montmartre is known for its artistic history and bohemian vibe. At the top of the hill, the stunning Sacré-Cœur Basilica offers a panoramic view of Paris. The streets of Montmartre are filled with local artists, making it the perfect place to pick up a unique souvenir.

> **Did You Know?**: Many famous artists, including Picasso and Van Gogh, lived and worked in Montmartre during the late 19th century.

---

### Final Thoughts

Paris is a city that captures the hearts of visitors with its blend of beauty, history, and culture. From its towering landmarks to its quaint streets, there's always something new to uncover. I hope this post inspires you to visit Paris and experience its magic for yourself.

For more travel guides, [visit my blog here](https://example.com/my-travel-blog).

---

*Thank you for reading! Feel free to share your thoughts in the comments.*

"""