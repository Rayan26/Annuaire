import json

import requests
from flask import Blueprint, request, make_response
from werkzeug.security import generate_password_hash, check_password_hash

from auth_service import db
from .models import User

auth = Blueprint('auth', __name__)
URL_FEED = "http://feed_service:5002"
headers = {
    'Content-Type': 'application/json'
}


@auth.route('/load_user2', methods=['POST'])
def load_user2():
        d = request.json
        user = User.query.get(d["id_user"])
        if user:
            payload = user.as_dict()
            return make_response(
                {"result": payload},
                200
            )

        return make_response(
            {"result": "nf"},
            200
        )


@auth.route('/login', methods=['POST'])
def login_post():
    json_request = request.json

    user = User.query.filter_by(email=json_request['email']).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, json_request['password']):
        return make_response(
            {"result": "error", "data": "Please check your login details and try again."},
            404
        )

    # if the above check passes, then we know the user has the right credentials
    return make_response(
        {"result": "ok", "data": user.as_dict()},
        200
    )


@auth.route('/signup', methods=['POST'])
def signup_post():
    json_request = request.json

    user = User.query.filter_by(
        email=json_request['email']).first()  # if this returns a user, then the email already exists in database

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        return make_response(
            {"result": "error", "data": "Email already taken."},
            404
        )

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=json_request['email'], name=json_request['name'],
                    password=generate_password_hash(json_request['password'], method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    body = json.dumps(dict(
        id_user=new_user.id,
        name=json_request['name']
    ))
    requests.post(URL_FEED + "/name", headers=headers, data=body)

    return make_response(
        {"result": "ok"},
        200
    )


@auth.route('/password', methods=['POST'])
def chg_pass():
    json_request = request.json

    user = User.query.filter_by(email=json_request['email']).first()
    user.password = generate_password_hash(json_request['new_mdp'], method='sha256')
    db.session.commit()

    return make_response(
        {"result": "ok", "data": "Password changed successfully."},
        200
    )
