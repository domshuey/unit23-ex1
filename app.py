"""Blogly application."""
from flask import Flask, redirect, request, render_template
from flask_sqlalchemy import SQLAlchemy
from psycopg2 import connect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()


@app.route('/')
def list_users():
    return redirect('/users')

@app.route('/users')
def show_all_users():
    users = User.query.all()
    return render_template('home.html', users = users)

@app.route('/users/new')
def show_new_user_form():
    users = User.query.all()
    return render_template('home_new.html', users = users)

@app.route('/users/new', methods=['POST'])
def add_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    new_user = User(first_name = first_name, last_name = last_name, image_url = image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_details(user_id):
    user = User.query.get(user_id)
    return render_template('user_details.html', user = user)

@app.route('/users/<int:user_id>/edit')
def show_edit_form(user_id):
    user = User.query.get(user_id)
    return render_template('edit_user.html', user = user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    user = User.query.get(user_id)
    edit_first_name = request.form['first_name']
    edit_last_name = request.form['last_name']
    edit_image_url = request.form['image_url']

    user.first_name = edit_first_name
    user.last_name = edit_last_name
    user.image_url = edit_image_url

    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')