import json

import requests
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# init SQLAlchemy so we can use it later in our models
from front_service.models import as_user

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'main.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        url = "http://auth_service:5001/load_user2"

        payload = json.dumps(
            dict(id_user=user_id)
        )
        headers = {
            'Content-Type': 'application/json'
        }
        r = requests.post(url, headers=headers, data=payload)
        res = r.json()
        if res['result'] != 'nf':
            user = as_user(res["result"])
            return user

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
