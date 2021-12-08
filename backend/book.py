import json

import requests
from flask import Blueprint, request, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user
from flask_login import logout_user, login_required, current_user

from backend import mysql

book = Blueprint('book', __name__)

headers = {
    'Content-Type': 'application/json'
}


@book.route('/searchUsers', methods=['POST'])
def searchUsers():
    json_request = request.json
    cursor = mysql.connection.cursor()
    sql = "SELECT * FROM user WHERE name REGEXP %s"
    print(sql)
    print(json_request)
    cursor.execute(sql, ["^" + json_request['name']])
    columns = cursor.description
    result = [{columns[index][0]: column for index, column in enumerate(value)} for value in cursor.fetchall()]

    if result:
        payload = result
        return make_response(
            {"status": "ok", "data": payload},
            200
        )

    return make_response(
        {"status": "error", "data": "User not found"},
        200
    )


@book.route('/getUsers', methods=['GET'])
def getUsers():
    cursor = mysql.connection.cursor()
    sql = "SELECT * FROM user"
    cursor.execute(sql)
    columns = cursor.description
    result = [{columns[index][0]: column for index, column in enumerate(value)} for value in cursor.fetchall()]

    if result:
        payload = result
        return make_response(
            {"status": "ok", "data": payload},
            200
        )

    return make_response(
        {"status": "error", "data": "User not found"},
        200
    )
