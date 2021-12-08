import json

import requests
from flask import Blueprint, request, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user
from flask_login import logout_user, login_required, current_user

from backend import mysql

admin = Blueprint('admin', __name__)

headers = {
    'Content-Type': 'application/json'
}


@admin.route('/signup', methods=['POST'])
def signup_post():
    json_request = request.json

    cursor = mysql.connection.cursor()
    sql = "SELECT id FROM user WHERE email = %s"

    cursor.execute(sql, [json_request['email']])
    columns = cursor.description
    result = [{columns[index][0]: column for index, column in enumerate(value)} for value in cursor.fetchall()]

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

    return make_response(
        {"status": "ok", "data": result},
        200
    )


@admin.route('/updateUser', methods=['POST'])
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


@admin.route('/remove', methods=['POST'])
def remove():
    json_request = request.json
    cursor = mysql.connection.cursor()

    sql = 'DELETE FROM user WHERE user.id = %s'
    cursor.execute(sql, [json_request['id']])
    columns = cursor.description
    result = [{columns[index][0]: column for index, column in enumerate(value)} for value in cursor.fetchall()]
    print(result)

    mysql.connection.commit()

    return make_response(
        {"result": "ok", "data": "User removed."},
        200
    )
