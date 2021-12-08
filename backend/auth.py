import json

import requests
from flask import Blueprint, request, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user
from flask_login import logout_user, login_required, current_user

from backend import mysql

auth = Blueprint('auth', __name__)

headers = {
    'Content-Type': 'application/json'
}


@auth.route('/load_user2', methods=['POST'])
def load_user2():
    json_request = request.json
    cursor = mysql.connection.cursor()
    sql = "SELECT * FROM user WHERE id = %s"
    print(json_request)
    cursor.execute(sql, [json_request['user_id']])
    columns = cursor.description
    result = [{columns[index][0]: column for index, column in enumerate(value)} for value in cursor.fetchall()]
    print(result[0]['email'])

    if result:
        payload = result[0]
        return make_response(
            {"status": "ok", "data": payload},
            200
        )

    return make_response(
        {"status": "error", "data": "User not found"},
        200
    )


@auth.route('/login', methods=['POST'])
def login_post():
    json_request = request.json

    cursor = mysql.connection.cursor()
    sql = 'SELECT * FROM user WHERE email = %s'
    cursor.execute(sql, [json_request['email']])
    columns = cursor.description
    result = [{columns[index][0]: column for index, column in enumerate(value)} for value in cursor.fetchall()]
    print(result)

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not result or not check_password_hash(result[0]['password'], json_request['password']):
        return make_response(
            {"status": "error", "data": "Please check your login details and try again."},
            404
        )

    # if the above check passes, then we know the user has the right credentials
    return make_response(
        {"status": "ok", "data": result},
        200
    )
