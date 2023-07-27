"""Blogly application."""

import os

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension

from models import connect_db, db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

@app.get('/')
def start():
    """redirect to user list page"""

    return redirect('/users')

@app.get('/users')
def show_users():
    """show user list page"""

    users = User.query.order_by("id").all()
    print("\n\n****","users:", users)
    return render_template('user_list.html',users=users)

@app.get('/users/new')
def display_add_user_form():
    """show the add user form"""

    return render_template('new_user.html')

@app.post('/users/new')
def handle_add_user_form():
    """Creates a db entry with form data and redirects"""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    if image_url == "":
        image_url = None

    user = User(
        first_name=first_name,
        last_name=last_name,
        image_url=image_url
    )
    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.get('/users/<int:user_id>')
def show_user_details(user_id):
    """show user details page"""

    user = User.query.get_or_404(user_id)
    posts = user.posts
    print('\n\n***',"user",user, "posts",user.posts)
    return render_template(
        'user_details.html',
        user=user,
        posts=posts
    )

@app.get('/users/<int:user_id>/edit')
def show_edit_form(user_id):
    """show the user edit form"""

    user = User.query.get_or_404(user_id)
    return render_template("user_edit.html", user=user)

@app.post('/users/<int:user_id>/edit')
def handle_edit_form(user_id):
    """edit the user info and update the record in database"""

    print("running hanle edit form")
    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["image_url"]
    db.session.commit()

    return redirect('/users')

@app.post('/users/<int:user_id>/delete')
def handle_delete_user(user_id):
    """delete the user from database, and redirect to users list"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')


@app.get('/users/<int:user_id>/posts/new')
def show_new_post_form(user_id):
    """Show form to add a post for that user."""

    user = User.query.get_or_404(user_id)
    return render_template(
        'add_post_form.html',
        user=user
    )


@app.post('/users/<int:user_id>/posts/new')
def handle_add_post_form(user_id):
    """ Handle add form; add post and redirect to the user detail page."""
    ...
    title = request.form['title']
    content = request.form['content']
    post = Post(
        title=title,
        content=content,
        user_id=user_id
    )
    db.session.add(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')


@app.get('/posts/<int:post_id>')
def show_post(post_id):
    """Shows a post"""
    ...
    # Show buttons to edit and delete the post.

@app.get('/posts/<int:post_id>/edit')
def show_edit_post_form(post_id):
    """Show form to edit a post, and to cancel (back to user page)."""
    ...

@app.post('/posts/<int:post_id>/edit')
def handle_edit_post_form(post_id):
    """Handle editing of a post. Redirect back to the post view."""
    ...


@app.post('/posts/<int:post_id>/delete')
def delete_post(post_id):
    """Delete the post"""




# TODO add post creation to seed file

# TODO create add post method

# TODO Update user page to show posts and have add post button

# TODO create add post form with cancel/add buttons

# TODO create post detail page with cancel, edit, delete functionality

# TODO create edit post form with cancel button




