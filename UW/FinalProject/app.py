import streamlit as st
import sqlite3
import pandas as pd
import hashlib
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from datetime import datetime
import os

# Database Connection
conn = sqlite3.connect('data.db')
cur = conn.cursor()

# Utility Functions


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password, hashed):
    return hashed == hashlib.sha256(password.encode()).hexdigest()

# Table Creation


def create_tables():
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            email TEXT
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS blogs(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author_id INTEGER,
            title TEXT,
            article TEXT,
            post_date DATE,
            FOREIGN KEY (author_id) REFERENCES users(id)
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS comments(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            blog_id INTEGER,
            user_id INTEGER,
            comment TEXT,
            post_date DATE,
            FOREIGN KEY (blog_id) REFERENCES blogs(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS likes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            blog_id INTEGER,
            user_id INTEGER,
            FOREIGN KEY (blog_id) REFERENCES blogs(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS tags(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            blog_id INTEGER,
            tag TEXT,
            FOREIGN KEY (blog_id) REFERENCES blogs(id)
        )
    ''')
    conn.commit()

# Authentication Functions


def register_user(username, password, email):
    hashed_password = hash_password(password)
    cur.execute('INSERT INTO users(username, password, email) VALUES (?, ?, ?)',
                (username, hashed_password, email))
    conn.commit()


def login_user(username, password):
    cur.execute('SELECT password FROM users WHERE username = ?', (username,))
    data = cur.fetchone()
    if data and verify_password(password, data[0]):
        return True
    return False


def get_user_id(username):
    cur.execute('SELECT id FROM users WHERE username = ?', (username,))
    data = cur.fetchone()
    return data[0] if data else None

# Blog Functions


def add_blog(author_id, title, article, post_date):
    cur.execute('INSERT INTO blogs(author_id, title, article, post_date) VALUES (?, ?, ?, ?)',
                (author_id, title, article, post_date))
    conn.commit()


def view_all_blogs():
    cur.execute('''
        SELECT blogs.id, users.username, blogs.title, blogs.article, blogs.post_date
        FROM blogs
        JOIN users ON blogs.author_id = users.id
    ''')
    return cur.fetchall()


def delete_blog(blog_id):
    # Delete related comments and likes first
    cur.execute('DELETE FROM comments WHERE blog_id = ?', (blog_id,))
    cur.execute('DELETE FROM likes WHERE blog_id = ?', (blog_id,))
    cur.execute('DELETE FROM tags WHERE blog_id = ?', (blog_id,))
    # Delete the blog itself
    cur.execute('DELETE FROM blogs WHERE id = ?', (blog_id,))
    conn.commit()


def add_comment(blog_id, user_id, comment, post_date):
    cur.execute('INSERT INTO comments(blog_id, user_id, comment, post_date) VALUES (?, ?, ?, ?)',
                (blog_id, user_id, comment, post_date))
    conn.commit()


def get_comments(blog_id):
    cur.execute('''
        SELECT comments.comment, users.username, comments.post_date
        FROM comments
        JOIN users ON comments.user_id = users.id
        WHERE comments.blog_id = ?
    ''', (blog_id,))
    return cur.fetchall()


def add_like(blog_id, user_id):
    cur.execute('INSERT INTO likes(blog_id, user_id) VALUES (?, ?)',
                (blog_id, user_id))
    conn.commit()


def count_likes(blog_id):
    cur.execute('SELECT COUNT(*) FROM likes WHERE blog_id = ?', (blog_id,))
    return cur.fetchone()[0]

# Streamlit App


def main():
    create_tables()
    st.set_page_config(page_title="Blogging App", layout="wide")
    st.title("Blogging App with Enhanced Features")

    # Sidebar Navigation
    menu = ["Home", "View Blogs", "Add Blog",
            "Manage Blogs", "Comments & Likes"]
    auth_menu = ["Login", "Register", "Logout"]

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.user_id = None

    auth_choice = st.sidebar.radio("Authentication", auth_menu)

    if auth_choice == "Login":
        st.sidebar.subheader("Login")
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Login"):
            if login_user(username, password):
                st.success(f"Welcome {username}!")
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.user_id = get_user_id(username)
            else:
                st.error("Invalid username or password")

    elif auth_choice == "Register":
        st.sidebar.subheader("Register")
        username = st.sidebar.text_input("Username")
        email = st.sidebar.text_input("Email")
        password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Register"):
            try:
                register_user(username, password, email)
                st.success("Registration Successful!")
            except sqlite3.IntegrityError:
                st.error("Username already exists. Please choose a different one.")

    elif auth_choice == "Logout":
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.user_id = None
        st.sidebar.success("Logged out successfully")

    # Main App
    if st.session_state.logged_in:
        choice = st.sidebar.radio("Main Menu", menu)

        if choice == "Home":
            st.image(os.path.join(os.getcwd(), "post.png"),
                     use_container_width=False)

        elif choice == "View Blogs":
            st.subheader("All Blogs")
            blogs = view_all_blogs()
            for blog in blogs:
                st.write(f"**Title:** {blog[2]}")
                st.write(f"**Author:** {blog[1]}")
                st.write(f"**Date:** {blog[4]}")
                st.write(f"**Content:** {blog[3]}")

                comments = get_comments(blog[0])
                st.write("**Comments:**")
                for comment in comments:
                    st.write(f"- {comment[1]}: {comment[0]} ({comment[2]})")

                likes = count_likes(blog[0])
                st.write(f"**Likes:** {likes}")

                # Add comment section
                if st.text_input(f"Add a comment to blog {blog[2]}"):
                    user_comment = st.text_area("Your comment")
                    if st.button("Post Comment", key=f"comment_{blog[0]}"):
                        add_comment(blog[0], st.session_state.user_id,
                                    user_comment, datetime.now().date())
                        st.success("Comment added successfully!")

                # Add like functionality
                if st.button("Like", key=f"like_{blog[0]}"):
                    add_like(blog[0], st.session_state.user_id)
                    st.success("Blog liked successfully!")

                st.markdown("---")

        elif choice == "Add Blog":
            st.subheader("Add a New Blog")
            title = st.text_input("Blog Title")
            article = st.text_area("Blog Content", height=300)
            post_date = st.date_input("Post Date", value=datetime.now().date())
            if st.button("Submit"):
                add_blog(st.session_state.user_id, title, article, post_date)
                st.success("Blog added successfully!")

        elif choice == "Manage Blogs":
            st.subheader("Manage Blogs")
            blogs = view_all_blogs()
            blog_titles = {blog[2]: blog[0]
                           for blog in blogs if blog[1] == st.session_state.username}
            selected_blog = st.selectbox(
                "Select Blog to Delete", list(blog_titles.keys()))
            if st.button("Delete"):
                delete_blog(blog_titles[selected_blog])
                st.success("Blog deleted successfully!")

        elif choice == "Comments & Likes":
            st.subheader("Manage Comments & Likes")
            blogs = view_all_blogs()
            for blog in blogs:
                if blog[1] == st.session_state.username:
                    st.write(f"**Title:** {blog[2]}")
                    comments = get_comments(blog[0])
                    st.write("**Comments:**")
                    for comment in comments:
                        st.write(
                            f"- {comment[1]}: {comment[0]} ({comment[2]})")
                    likes = count_likes(blog[0])
                    st.write(f"**Total Likes:** {likes}")
                    st.markdown("---")
    else:
        st.warning("Please log in to access the app.")


if __name__ == "__main__":
    main()
