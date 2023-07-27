"""Blogly application."""

import os

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension

from models import connect_db, db, User

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
    return render_template(
        'user_details.html',
        user=user
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



