from flask_login._compat import unicode

from feed_service import db


# Feed
class Follow(db.Model):
    id_user = db.Column(db.Integer, primary_key=True)
    id_following = db.Column(db.Integer, primary_key=True)


# Feed
class Post(db.Model):
    id_post = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer)
    content = db.Column(db.String(256))
    date = db.Column(db.DateTime)  # https://docs.python.org/3/library/datetime.html#datetime.datetime

    def as_dict(self):
        return {c.name: unicode(getattr(self, c.name)) for c in self.__table__.columns}


# Feed
class Name(db.Model):
    id_name = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    id_user = db.Column(db.Integer)
    name = db.Column(db.String(64))

    def as_dict(self):
        return {c.name: unicode(getattr(self, c.name)) for c in self.__table__.columns}
