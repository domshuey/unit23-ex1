"""Blogly application."""
from tabnanny import process_tokens
from time import process_time_ns
from flask import Flask, redirect, request, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from psycopg2 import connect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, Post_tag


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
    posts = Post.query.all()
    tags = Tag.query.all()
    return render_template('home.html', users = users, posts=posts, tags=tags)

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
    posts = Post.query.filter(Post.user_id == user_id).all()
    return render_template('user_details.html', user = user, posts=posts)

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

    flash(f'User {user.full_name} has been edited.')
    
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/posts/new')
def show_form(user_id):
    user = User.query.get(user_id)
    return render_template('add_post.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=['post'])
def add_post(user_id):
    user = User.query.get(user_id)
    title = request.form['title']
    content = request.form['content']

    new_post = Post(title=title, content=content, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()

    return render_template('user_details.html', user=user)

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.query.get(post_id)
    return render_template('post_detail.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def show_edit_post_form(post_id):
    post = Post.query.get(post_id)
    tags = Tag.query.all()
    return render_template('edit_post.html', post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=['post'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    
    tag_ids = [int(num) for num in request.form.getlist('tags')]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    
    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):
    post = Post.query.get(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect('/users/<post_id.users.id>')

@app.route('/tags')
def show_tags():
    tags = Tag.query.all()

    return render_template('tags.html', tags=tags)

@app.route('/tags/new')
def add_tag():
    return render_template('newTag.html')

@app.route('/tags/new', methods=['post'])
def create_tag():
    tag = request.form['name']
    new_tag = Tag(name=tag)

    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    tag = Tag.query.get(tag_id)
    posts = tag.post
    return render_template('showTag.html', tag=tag, posts=posts)

@app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):
    tag = Tag.query.get(tag_id)
    return render_template('editTag.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=['post'])
def process_edit_tag(tag_id):
    tag = Tag.query.get(tag_id)
    new_name = request.form['name']
    tag.name = new_name

    db.session.add(tag)
    db.session.commit()

    return redirect('/tags/<int:tag_id>')

@app.route('/tags/<int:tag_id>/delete')
def delete_tag(tag_id):
    tag = Tag.query.get(tag_id)

    db.session.delete(tag)
    db.session.commit()

    return redirect('/tags')