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
def show_homepage():

    return redirect('/users')

@app.get('/users')
def show_users():
    users = User.query.all()
    print("\n\n****","users:", users)
    return render_template('user_list.html',users = users)

@app.get('/users/new')
def add_user_form():

    return render_template('new_user.html')

@app.post('/users/new')
def handle_add_user_form():
    """Creates a db entry with form data and redirects"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    if image_url == "":
        image_url = None

    user = User(first_name=first_name,last_name=last_name,image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.get('/users/<user_id>')
def show_user_details(user_id):
    user = User.query.get(user_id)
    return render_template(
        'user_details.html',
        user=user
    )