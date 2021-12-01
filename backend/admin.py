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
