# Python blog
#### Video Demo: https://youtu.be/Uw-Cv8i8g6Y
#### Description:

This project set out with the aim of building a lightweight but comprehensive blog platform which could be used and adapted for many purposes (in my project I set it out as a travel blog). It allows the user to browse through various posts on the website, search for posts, view details of the website, and contact editors/admin.
For admin users, they can seamlessly create new blog posts, writing them in an easy and intuitive and widely used syntax - markdown, as well as uploading .md or .txt files.
In addition to this, they can view all blog posts and delete and edit them as they wish. All of this, of course, is protected with a login system.
Code overview:

For this project, I used Flask as the backend to create the API and to serve the webpages for the website, whereas for the frontend I used JavaScript (e.g., for validating form data and getting search results from the API). I also used SQL (specifically SQLite3) for the databases to store both user accounts and blog posts.
HTML and CSS, along with the Bootstrap framework, were used for webpage design.
#### Python:

Python, as before mentioned, was used for the API (set out in the api.py file) and the main website (comprised of the app.py, auth.py, and admin.py files). As well as this, the utility.py file stores utility functions such as functions to fetch data from the databases and to send emails to admin accounts.
#### JavaScript:

There are 8 JavaScript files, all with different purposes. The validation JavaScript files are used in conjunction with Bootstrap’s form validation to give the user real-time feedback on form input and prevent incorrect data from being inputted (however, data is also validated server-side).
Unsaved.js is used to prompt the user to save their work when they try to leave a webpage, and theme.js facilitates the change between dark and light themes of the webpages, saving it between different endpoints through the use of Flask sessions.
HTML:

Used for the layout of webpages with Bootstrap, meaning that webpages are dynamic and adapt to the device's screen size.
#### Features:

Homepage: Displays the latest blog posts with an image, title, and date, meaning users have quick access to the latest articles.

Search functionality: My project leverages SQL's full-text search functionality to allow users to search for blog posts based on words in the title, subtitle, and article body.

Blog post pages: Each blog post features a main image, title, subtitle, date, and main content, which is very adaptable due to the use of markdown.

Dark mode: The website includes a toggle to switch between light, dark, and auto mode for improved user experience (default set to auto).

Mobile-friendly: Responsive to different-sized screens due to the use of Bootstrap.

#### Installation:

- git clone https://github.com/coder-72/CS50-final-
- Set up venv: source venv/bin/activate

#### Usage:

- Run python app.py
- Go to http://localhost:5000, which should be the homepage.
- You can:
    - Browse through posts
    - Edit posts (username: admin, password: admin)
    - Delete posts
    - Create new posts

#### Testing:

I've tested this website through extensive use, attempting to fill all use cases and edge cases, correcting errors as I go.
Credits:
- Developer: coder-72
- ChatGPT: Used in debugging HTML and creating article content
- Inspiration: Bootstrap, CS50, Flask documentation

#### Support:
- Email: 72.jake.ward@gmail.com
- GitHub: coder-72