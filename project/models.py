from flask_login import UserMixin

from . import db


# Auth
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(64))


# Feed
class Follow(db.Model):
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    id_following = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)


# Feed
class Post(db.Model):
    id_post = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.String(256))
    date = db.Column(db.DateTime)  # https://docs.python.org/3/library/datetime.html#datetime.datetime


# Feed
class Name(db.Model):
    id_name = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(64))
