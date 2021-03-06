import os
from flask import Flask
from flask_login import LoginManager
from flask_mysqldb import MySQL

# init SQLAlchemy so we can use it later in our models
mysql = MySQL()


def create_app():
    app = Flask(__name__)
    app.config['MYSQL_HOST'] = '192.168.30.2'
    app.config['MYSQL_USER'] = 'user'
    app.config['MYSQL_PASSWORD'] = 'password'
    app.config['MYSQL_DB'] = 'annuaire'

    mysql.init_app(app)


    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    from .book import book as book_blueprint
    app.register_blueprint(book_blueprint)

    return app
