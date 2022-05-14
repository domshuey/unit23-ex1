"""Models for Blogly."""
from collections import UserString
from email.policy import default
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'

    @classmethod
    def full_name(cls, first_name, last_name):
        user_full_name = f"{first_name} + ' ' + {last_name}"
        return user_full_name

    

    id = db.Column(db.Integer,
                    primary_key = True,
                    autoincrement = True)
    first_name = db.Column(db.String(10),
                            nullable = False)
    last_name = db.Column(db.String(15),
                            nullable = False)
    image_url = db.Column(db.String(100),
                            default = 'https://www.pngitem.com/pimgs/m/504-5040528_empty-profile-picture-png-transparent-png.png')
    
    full_name = f'{first_name} {last_name}'



class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref='posts')