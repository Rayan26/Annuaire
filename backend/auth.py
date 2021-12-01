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


@auth.route('/signup', methods=['POST'])
def signup_post():
    json_request = request.json

    cursor = mysql.connection.cursor()
    sql = "SELECT id FROM user WHERE email = %s"

    cursor.execute(sql, [json_request['email']])
    columns = cursor.description
    result = [{columns[index][0]: column for index, column in enumerate(value)} for value in cursor.fetchall()]
    print(result)
    if result:  # if a user is found, we want to redirect back to signup page so user can try again
        return make_response(
            {"status": "error", "data": "Email already taken."},
            404
        )

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    sql = 'INSERT INTO user (email, password, name, phone, role, job, location) VALUES (%s, %s, %s, %s, %s, %s, %s)'

    # add the new user to the database
    cursor.execute(sql, (json_request['email'],
                         generate_password_hash(json_request['password'],
                                                method='sha256'),
                         json_request['name'],
                         json_request['phone'],
                         "USER" if 'role' not in json_request else json_request['role'],
                         json_request['job'],
                         json_request['location']))
    columns = cursor.description
    mysql.connection.commit()

    result = [{columns[index][0]: column for index, column in enumerate(value)} for value in cursor.fetchall()]
    body = json.dumps(dict(
        id_user=result,
        name=json_request['name']
    ))
    # requests.post(URL_FEED + "/name", headers=headers, data=body)
    print(result)
    print(columns)
    return make_response(
        {"status": "ok", "data": result},
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


@auth.route('/updateUser', methods=['POST'])
def updateUser():
    json_request = request.json
    cursor = mysql.connection.cursor()
    print(json_request['new_mdp'])

    if json_request['new_mdp']:
        sql = 'UPDATE user SET user.password = %s WHERE id = %s'
        cursor.execute(sql, (generate_password_hash(json_request['new_mdp'], method='sha256'), json_request['id']))
        columns = cursor.description
        result = [{columns[index][0]: column for index, column in enumerate(value)} for value in cursor.fetchall()]
        print(result)
        print("ok")
        mysql.connection.commit()

    if json_request['role']:
        sql = 'UPDATE user SET user.role = %s WHERE id = %s'
        cursor.execute(sql, (json_request['role'], json_request['id']))
        columns = cursor.description
        result = [{columns[index][0]: column for index, column in enumerate(value)} for value in cursor.fetchall()]
        print(result)
        print("okok")
        mysql.connection.commit()

    return make_response(
        {"result": "ok", "data": "Password changed successfully."},
        200
    )
