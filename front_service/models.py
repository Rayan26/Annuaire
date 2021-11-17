from datetime import datetime

from flask_login import UserMixin


class User(UserMixin):
    id: int
    email: str
    password: str
    name: str

    def __init__(self, id, email, password, name):
        self.id = id
        self.email = email
        self.password = password
        self.name = name


def as_user(json):
    return User(json['id'], json['email'], json['password'], json['name'])


def as_datetime(str_date):
    return datetime.strptime(str_date, '%Y-%m-%d %H:%M:%S.%f')


class Post:
    id_post = int
    id_user = int
    content = str
    date = datetime

    def __init__(self, id_post, id_user, content, date):
        self.id_post = id_post
        self.id_user = id_user
        self.content = content
        self.date = as_datetime(date)  # '2021-05-26 09:40:25.949411'


def as_post(json):
    return Post(json['id_post'], json['id_user'], json['content'], json['date'])


# Feed
class Name:
    id_name = int
    id_user = int
    name = str

    def __init__(self, id_name, id_user, name):
        self.id_name = id_name
        self.id_user = id_user
        self.name = name


def as_name(json):
    return Name(json['id_name'], json['id_user'], json['name'])
