import streamlit as st
import sqlite3
from datetime import datetime
import os
import webbrowser
import matplotlib.pyplot as plt
import numpy as np

# Database Setup


def create_tables():
    conn = sqlite3.connect("educational_platform.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT,
                    role TEXT CHECK(role IN ('admin', 'teacher', 'student'))
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS posts (
                    post_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    title TEXT,
                    content TEXT,
                    file_path TEXT,
                    file_type TEXT,
                    date_posted TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(user_id)
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS comments (
                    comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    post_id INTEGER,
                    user_id INTEGER,
                    comment_text TEXT,
                    date_commented TEXT,
                    FOREIGN KEY(post_id) REFERENCES posts(post_id),
                    FOREIGN KEY(user_id) REFERENCES users(user_id)
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS classes (
                    class_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    class_title TEXT,
                    class_date TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(user_id)
                )''')
    conn.commit()
    conn.close()

# Function to register a new user


def register_user(username, password, role):
    conn = sqlite3.connect("educational_platform.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                  (username, password, role))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

# Function to authenticate user


def authenticate_user(username, password):
    conn = sqlite3.connect("educational_platform.db")
    c = conn.cursor()
    c.execute("SELECT user_id, role FROM users WHERE username = ? AND password = ?",
              (username, password))
    user = c.fetchone()
    conn.close()
    return user

# Function to create a post


def create_post(user_id, title, content, file_path, file_type):
    conn = sqlite3.connect("educational_platform.db")
    c = conn.cursor()
    date_posted = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute("INSERT INTO posts (user_id, title, content, file_path, file_type, date_posted) VALUES (?, ?, ?, ?, ?, ?)",
              (user_id, title, content, file_path, file_type, date_posted))
    conn.commit()
    conn.close()

# Function to fetch all posts


def fetch_posts():
    conn = sqlite3.connect("educational_platform.db")
    c = conn.cursor()
    c.execute("SELECT posts.post_id, users.username, posts.title, posts.content, posts.file_path, posts.file_type, posts.date_posted FROM posts JOIN users ON posts.user_id = users.user_id ORDER BY posts.date_posted DESC")
    posts = c.fetchall()
    conn.close()
    return posts

# Function to fetch comments for a post


def fetch_comments(post_id):
    conn = sqlite3.connect("educational_platform.db")
    c = conn.cursor()
    c.execute("SELECT users.username, comments.comment_text, comments.date_commented FROM comments JOIN users ON comments.user_id = users.user_id WHERE post_id = ? ORDER BY comments.date_commented ASC", (post_id,))
    comments = c.fetchall()
    conn.close()
    return comments

# Function to add a comment


def add_comment(post_id, user_id, comment_text):
    conn = sqlite3.connect("educational_platform.db")
    c = conn.cursor()
    date_commented = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute("INSERT INTO comments (post_id, user_id, comment_text, date_commented) VALUES (?, ?, ?, ?)",
              (post_id, user_id, comment_text, date_commented))
    conn.commit()
    conn.close()

# Function to delete a post


def delete_post(post_id):
    conn = sqlite3.connect("educational_platform.db")
    c = conn.cursor()
    c.execute("DELETE FROM posts WHERE post_id = ?", (post_id,))
    conn.commit()
    conn.close()

# Function to add a class to the calendar


def add_class(user_id, class_title, class_date):
    conn = sqlite3.connect("educational_platform.db")
    c = conn.cursor()
    c.execute("INSERT INTO classes (user_id, class_title, class_date) VALUES (?, ?, ?)",
              (user_id, class_title, class_date))
    conn.commit()
    conn.close()

# Function to fetch all classes


def fetch_classes():
    conn = sqlite3.connect("educational_platform.db")
    c = conn.cursor()
    c.execute("SELECT users.username, classes.class_title, classes.class_date FROM classes JOIN users ON classes.user_id = users.user_id ORDER BY classes.class_date ASC")
    classes = c.fetchall()
    conn.close()
    return classes

# Function to open YouTube search results


def open_youtube_search(query):
    base_url = "https://www.youtube.com/results?search_query="
    search_url = base_url + query.replace(" ", "+")
    webbrowser.open(search_url)


def open_google_search(query):
    base_url = "https://www.google.com/search?q="
    search_url = base_url + query.replace(" ", "+")
    webbrowser.open(search_url)

# Function to open Wikipedia search results


def open_wikipedia_search(query):
    base_url = "https://en.wikipedia.org/wiki/Special:Search?search="
    search_url = base_url + query.replace(" ", "+")
    webbrowser.open(search_url)

# Function to open Stack Overflow search results


def open_stackoverflow_search(query):
    base_url = "https://stackoverflow.com/search?q="
    search_url = base_url + query.replace(" ", "+")
    webbrowser.open(search_url)


# Streamlit UI
st.set_page_config(page_title="Educational Platform",
                   page_icon="📚", layout="wide")

create_tables()

# Custom CSS for white background and styling
# st.markdown(
#     """
#     <style>
#     .css-1aumxhk {background-color: white;}
#     .block-container {padding: 2rem; background-color: white;}
#     .css-18e3th9 {font-size: 20px;}
#     .css-1v3fvcr {background-color: #f0f0f0; border-radius: 10px; padding: 10px;}
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# Session state
if "user" not in st.session_state:
    st.session_state.user = None
    st.session_state.page = "login"

# Redirect to login after logout


def redirect_to_login():
    st.session_state.user = None
    st.session_state.page = "login"
    st.experimental_set_query_params(page="login")


if st.session_state.user is None and st.session_state.page == "login":
    st.sidebar.header("Login / Register")

    # Register Section
    st.sidebar.subheader("Register")
    reg_username = st.sidebar.text_input("Username (for registration)")
    reg_password = st.sidebar.text_input(
        "Password (for registration)", type="password")
    reg_role = st.sidebar.selectbox("Role", ["admin", "teacher", "student"])
    if st.sidebar.button("Register"):
        if register_user(reg_username, reg_password, reg_role):
            st.sidebar.success("Registration successful! Please log in.")
        else:
            st.sidebar.error("Username already exists.")

    # Login Section
    st.sidebar.subheader("Login")
    login_username = st.sidebar.text_input("Username (for login)")
    login_password = st.sidebar.text_input(
        "Password (for login)", type="password")
    if st.sidebar.button("Login"):
        user = authenticate_user(login_username, login_password)
        if user:
            st.session_state.user = {
                "user_id": user[0], "username": login_username, "role": user[1]}
            st.session_state.page = "home"
            st.experimental_set_query_params(page="home")
            st.sidebar.success(f"Welcome, {login_username}!")
        else:
            st.sidebar.error("Invalid credentials.")
else:
    st.sidebar.subheader(f"Welcome, {st.session_state.user['username']}!")
    menu = st.sidebar.radio("Navigation", ["Posts", "Calendar", "Search Tutorials",
                            "Statistics", "Admin" if st.session_state.user['role'] == "admin" else "Logout"])

    if menu == "Logout":
        redirect_to_login()
        st.sidebar.info("You have been logged out.")

    # Search Tutorial Page
    if menu == "Search Tutorials":
        st.subheader("Search Resources")
        tutorial_query = st.text_input("Enter topic:")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button("Search on YouTube"):
                if tutorial_query:
                    open_youtube_search(tutorial_query)
                    st.success("Redirecting to YouTube for tutorial videos!")
                else:
                    st.error("Please enter a topic to search.")

        with col2:
            if st.button("Search on Google"):
                if tutorial_query:
                    open_google_search(tutorial_query)
                    st.success("Redirecting to Google search results!")
                else:
                    st.error("Please enter a topic to search.")

        with col3:
            if st.button("Search on Wikipedia"):
                if tutorial_query:
                    open_wikipedia_search(tutorial_query)
                    st.success("Redirecting to Wikipedia search results!")
                else:
                    st.error("Please enter a topic to search.")

        with col4:
            if st.button("Search on Stack Overflow"):
                if tutorial_query:
                    open_stackoverflow_search(tutorial_query)
                    st.success("Redirecting to Stack Overflow search results!")
                else:
                    st.error("Please enter a topic to search.")

    # Statistics Page
    if menu == "Statistics":
        st.subheader("Statistics and Chart Information")
        st.write("Learn about different types of charts and see examples:")

        # Histogram Example
        st.write("### Histogram")
        data = np.random.randn(1000)
        fig, ax = plt.subplots()
        ax.hist(data, bins=30, color='skyblue', edgecolor='black')
        ax.set_title("Histogram Example")
        ax.set_xlabel("Value")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)

        # Bar Chart Example
        st.write("### Bar Chart")
        categories = ['A', 'B', 'C', 'D']
        values = [23, 45, 56, 78]
        fig, ax = plt.subplots()
        ax.bar(categories, values, color='lightcoral')
        ax.set_title("Bar Chart Example")
        ax.set_xlabel("Categories")
        ax.set_ylabel("Values")
        st.pyplot(fig)

        # Pie Chart Example
        st.write("### Pie Chart")
        labels = ['Category 1', 'Category 2', 'Category 3']
        sizes = [30, 45, 25]
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90,
               colors=['#ff9999', '#66b3ff', '#99ff99'])
        ax.set_title("Pie Chart Example")
        st.pyplot(fig)

    # Admin page
    if menu == "Admin" and st.session_state.user['role'] == "admin":
        st.subheader("Admin Dashboard")
        st.write("Manage all posts and classes")

        st.subheader("All Posts")
        posts = fetch_posts()
        for post_id, username, title, content, file_path, file_type, date_posted in posts:
            with st.expander(f"{title} by {username} ({date_posted})"):
                st.write(content)
                if file_path:
                    with open(file_path, "rb") as f:
                        file_data = f.read()
                    st.download_button(
                        "Download File", data=file_data, file_name=file_path.split('/')[-1])
                if st.button(f"Delete Post (ID: {post_id})", key=f"delete_post_{post_id}"):
                    delete_post(post_id)
                    st.success("Post deleted successfully!")
                    st.experimental_rerun()

        st.subheader("All Classes")
        classes = fetch_classes()
        for teacher, class_title, class_date in classes:
            st.write(f"Class: {class_title} by {teacher} on {class_date}")

    if st.session_state.user is not None and menu not in ["Admin", "Search Tutorials", "Statistics"]:
        st.title("Educational Platform 📚")

        if menu == "Posts":
            if st.session_state.user["role"] == "teacher":
                st.subheader("Create a Post")
                post_title = st.text_input("Post Title")
                post_content = st.text_area("Post Content")
                uploaded_file = st.file_uploader("Upload File (optional)", type=[
                                                 "pdf", "png", "jpg", "jpeg", "docx", "xlsx"])

                file_path = ""
                file_type = ""
                if uploaded_file is not None:
                    file_type = uploaded_file.type
                    file_path = f"uploads/{datetime.now().strftime('%Y%m%d%H%M%S')}_{
                        uploaded_file.name}"
                    os.makedirs("uploads", exist_ok=True)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                if st.button("Post"):
                    if post_title and post_content:
                        create_post(
                            st.session_state.user["user_id"], post_title, post_content, file_path, file_type)
                        st.success("Post created successfully!")
                    else:
                        st.error("Please fill in both the title and content.")

            st.subheader("All Posts")
            posts = fetch_posts()
            if posts:
                for post_id, username, title, content, file_path, file_type, date_posted in posts:
                    with st.expander(f"{title} (by {username} on {date_posted})"):
                        st.markdown(f"**{content}**")
                        if file_path:
                            with open(file_path, "rb") as f:
                                file_data = f.read()
                            st.download_button(
                                "Download File", data=file_data, file_name=file_path.split('/')[-1])

                        st.subheader("Comments")
                        comments = fetch_comments(post_id)
                        for commenter, comment_text, date_commented in comments:
                            st.markdown(
                                f"- **{commenter}**: {comment_text} (*{date_commented}*)")

                        if st.session_state.user["role"] == "student":
                            comment_text = st.text_input(
                                f"Add a comment (Post ID: {post_id})", key=f"comment_{post_id}")
                            if st.button(f"Submit Comment ({post_id})", key=f"submit_comment_{post_id}"):
                                if comment_text:
                                    add_comment(
                                        post_id, st.session_state.user["user_id"], comment_text)
                                    st.success("Comment added successfully!")
                                else:
                                    st.error("Please enter a comment.")

                        if st.session_state.user["role"] == "teacher" and st.session_state.user["username"] == username:
                            if st.button(f"Delete Post ({title})", key=f"del_{post_id}"):
                                delete_post(post_id)
                                st.success("Post deleted successfully!")
            else:
                st.info("No posts available yet.")

        elif menu == "Calendar":
            if st.session_state.user["role"] == "teacher":
                st.subheader("Add Class to Calendar")
                class_title = st.text_input("Class Title")
                class_date = st.date_input("Class Date")
                if st.button("Add Class"):
                    add_class(
                        st.session_state.user["user_id"], class_title, class_date.strftime('%Y-%m-%d'))
                    st.success("Class added to calendar!")

            st.subheader("Class Calendar")
            classes = fetch_classes()
            if classes:
                for teacher, class_title, class_date in classes:
                    st.markdown(
                        f"- **{class_title}** by {teacher} on {class_date}")
            else:
                st.info("No classes scheduled yet.")
    else:
        st.info("Please log in to view or create posts and calendar entries.")
