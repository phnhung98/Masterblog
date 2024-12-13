#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 22:58:50 2024

@author: nhung
"""

from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


def get_posts():
    blog_posts = {}
    with open("data.json", "r") as fileobj:
        blog_posts = json.loads(fileobj.read())
    return blog_posts


def save_posts(posts):
    with open('data.json', 'w') as fileobj:
        json.dump(posts, fileobj, indent=4)


def get_next_id():
    # Get the next ID for a new post
    try:
        with open('data.json', 'r') as f:
            posts = json.load(f)
        return max(post['id'] for post in posts) + 1
    except (FileNotFoundError, ValueError):
        return 1


def fetch_post_by_id(post_id, posts):
    """ Find the post with the id `post_id`.
    If there is no post with this id, return None. """
    post = next((post for post in posts if post['id'] == post_id), None)
    return post


@app.route('/')
def index():
    blog_posts = get_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        content = request.form['content']
        # Create a new blog post
        new_post = {
            "id": get_next_id(),
            "title": title,
            "author": author,
            "content": content
        }

        posts = get_posts()
        posts.append(new_post)

        save_posts(posts)

        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    posts = get_posts()
    # posts = [post for post in posts if post['id'] != post_id]

    post = fetch_post_by_id(post_id, posts)
    if post is None:
        # Post not found
        return "Post not found", 404
    print(post)
    posts.remove(post)

    save_posts(posts)
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    posts = get_posts()

    # Find the post with the given ID
    post = fetch_post_by_id(post_id, posts)
    print(f'This is debug post {post}')

    if not post:
        return "Post not found", 404

    if request.method == 'POST':
        # Update the post with new data
        print(request.form)
        post['title'] = request.form['title']
        post['author'] = request.form['author']
        post['content'] = request.form['content']

        # Save the updated posts back to the JSON file
        with open('blog_posts.json', 'w') as f:
            json.dump(posts, f, indent=4)

        # Redirect back to the index page
        return redirect(url_for('index'))

    # Render the update form with the current post data
    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)