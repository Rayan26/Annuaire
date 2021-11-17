from flask_login import UserMixin
from flask_login._compat import unicode

from auth_service import db


# Auth
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(64))

    def as_dict(self):
        return {c.name: unicode(getattr(self, c.name)) for c in self.__table__.columns}
