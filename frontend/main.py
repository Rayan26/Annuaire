import json

import requests
from flask import Blueprint, render_template, url_for, request, flash
from flask_login import current_user, login_required, logout_user, login_user
from werkzeug.security import check_password_hash
from werkzeug.utils import redirect

from frontend.models import as_user, as_post, as_name

main = Blueprint('main', __name__)

URL_BACK = 'http://192.168.10.2:5001'

headers = {
    'Content-Type': 'application/json'
}


@main.route('/')
def index():
    return render_template('index.html', user=current_user)


@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        data = json.dumps(dict(
            email=email,
            password=password
        ))
        r = requests.post(URL_BACK + '/login', headers=headers, data=data)
        res = r.json()

        if res['status'] == 'error':
            flash(res['data'])
            return redirect(url_for('main.login'))  # if the user doesn't exist or password is wrong, reload the page
        else:
            user = as_user(res['data'][0])
            login_user(user, remember=remember)
            return redirect(url_for('main.index'))

    return render_template('login.html')


@main.route('/signup', methods=['GET', 'POST'])
def signup():
    global data
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        phone = request.form.get('phone')
        job = request.form.get('job')
        location = request.form.get('location')
        role = request.form.get('role')

        if current_user.is_authenticated:
            if current_user.role == 'ADMIN':  # only admin can edit roles
                data = json.dumps(dict(
                    email=email,
                    name=name,
                    password=password,
                    phone=phone,
                    job=job,
                    location=location,
                    role=role
                ))
        else:
            data = json.dumps(dict(
                email=email,
                name=name,
                password=password,
                phone=phone,
                job=job,
                location=location
            ))

        r = requests.post(URL_BACK + '/signup', headers=headers, data=data)
        res = r.json()

        print(res['status'])
        if res['status'] == 'error':
            if current_user.is_authenticated:
                if current_user.role == 'ADMIN':
                    flash(res['data'])
                    return redirect(url_for('main.book'))
            else:
                flash(res['data'])
                return redirect(url_for('main.login'))
        else:
            if current_user.is_authenticated:
                if current_user.role == 'ADMIN':
                    return redirect(url_for('main.book'))
            else:
                return redirect(url_for('main.login'))
    return render_template('signup.html')


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@main.route('/book', methods=['GET', 'POST'])
@login_required
def book():
    if request.method == 'GET':
        r = requests.get(URL_BACK + '/getUsers', headers=headers)
        res = r.json()
        return render_template('book.html', users=res['data'], current_user=current_user)
    if request.method == 'POST':
        data = json.dumps(dict(
            name=request.form.get('name'),
        ))
        r = requests.post(URL_BACK + '/searchUsers', headers=headers, data=data)
        res = r.json()

        return render_template('book.html', users=res['data'], current_user=current_user)


@main.route('/updateUser', methods=['GET', 'POST'])
@login_required
def updateUser():
    if request.method == 'POST':
        mdp = request.form.get('mdp')
        new_mdp = request.form.get('new_mdp')
        new_mdp2 = request.form.get('new_mdp2')
        role = request.form.get('role')
        user_id = request.form.get('user_id')

        if current_user.role != 'ADMIN':  # only admin can change without old_password
            # check if the actual password submit match with true password.
            if not check_password_hash(current_user.password, mdp):
                flash('Mot de passe actuel erroné')
                return redirect(
                    url_for('main.updateUser'))  # if actual password is wrong or new password not equal, reload
            # check if the two password submit are equal.

            if new_mdp != new_mdp2:
                flash('Vous devez utilisé le même mot de passe pour confirmer le changement')
                return redirect(
                    url_for('main.updateUser'))  # if actual password is wrong or new password not equal, reload

            data = json.dumps(dict(
                new_mdp=new_mdp,
                id=current_user.id,
            ))
        else:
            data = json.dumps(dict(
                new_mdp=new_mdp,
                id=user_id,
                role=role
            ))

        r = requests.post(URL_BACK + '/updateUser', headers=headers, data=data)
        if current_user.role != 'ADMIN':
            logout_user()
            return redirect(url_for('main.index'))
        else:
            return redirect(url_for('main.book'))

    return render_template('mdp.html')


@main.route('/remove', methods=['POST'])
@login_required
def remove():
    if current_user.role == 'ADMIN':
        user_id = request.form.get('user_id') if request.form.get('user_id') else current_user.id
        data = json.dumps(dict(
            id=user_id
        ))
    else:
        data = json.dumps(dict(
            id=current_user.id
        ))
    requests.post(URL_BACK + '/remove', headers=headers, data=data)
    if current_user.role != 'ADMIN':
        logout_user()
        return redirect(url_for('main.index'))
    return redirect(url_for('main.book'))



