import json

import requests
from flask import Flask
from flask_login import LoginManager

# init SQLAlchemy so we can use it later in our models
from frontend.models import as_user


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key-goes-here'

    app.static_folder = 'static'

    login_manager = LoginManager()
    login_manager.login_view = 'main.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        url = "http://backend:5001/load_user2"

        payload = json.dumps(
            dict(user_id=user_id)
        )
        headers = {
            'Content-Type': 'application/json'
        }
        r = requests.post(url, headers=headers, data=payload)
        res = r.json()
        if res['status'] != 'error':
            user = as_user(res["data"])
            return user

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
