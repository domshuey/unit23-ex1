"""Models for Blogly."""
from collections import UserString
from email.policy import default
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'

    # @classmethod
    # def full_name(cls, first_name, last_name):
    #     user_full_name = f"{first_name} + ' ' + {last_name}"
    #     return user_full_name


    def __repr__(self):
        u = self
        return(f'<User {u.id}: {u.first_name} {u.last_name}>')

    id = db.Column(db.Integer,
                    primary_key = True,
                    autoincrement = True)
    first_name = db.Column(db.String(10),
                            nullable = False)
    last_name = db.Column(db.String(15),
                            nullable = False)
    image_url = db.Column(db.String(100),
                            default = 'https://www.pngitem.com/pimgs/m/504-5040528_empty-profile-picture-png-transparent-png.png')
    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'



class Post(db.Model):
    __tablename__ = 'posts'

    def __repr__(self):
        p = self
        return (f'<Post {p.id}: {p.title} - {p.content} Created_at: {p.created_at} by {p.user_id}')

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    user = db.relationship('User', backref='posts')
    

    @property
    def friendly_date(self):
        """Return nicely-formatted date."""

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")


class Tag(db.Model):

    __tablename__ = 'tags'

    def __repr__(self):
        t = self
        return (f'<Tag ID: {t.id} - Tag Name: {t.name}')

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    posts = db.relationship('Post', secondary='post_tags', backref='tag')


class Post_tag(db.Model):

    __tablename__ = 'post_tags'

    def __repr__(self):
        p = self
        return(f'<Post ID: {p.post_id} - Tag ID: {p.tag_id}')

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True, nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True, nullable=False)

    user = db.relationship('User', secondary='posts', backref='post_tag')


