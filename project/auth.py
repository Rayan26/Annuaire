from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user
from flask_login import logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from . import db
from .models import User, Name

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))  # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.index'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(
        email=email).first()  # if this returns a user, then the email already exists in database

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    n = Name(id_user=new_user.id, name=name)
    db.session.add(n)
    db.session.commit()
    # body = {"id_user": new_user.id, "name": name}
    # headers = {
    #     'Content-Type': 'application/json'
    # }
    # r = requests.post("http://127.0.0.1:5000/name", headers=headers, data=body)
    # res = r.json()
    # print(res)

    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/password', methods=['GET', 'POST'])
@login_required
def chg_pass():
    if request.method == 'POST':
        mdp = request.form.get('mdp')
        new_mdp = request.form.get('new_mdp')
        new_mdp2 = request.form.get('new_mdp2')

        if not check_password_hash(current_user.password, mdp):
            flash('Veuillez entrer votre mot de passe actuel', 'psw-missing')
            return redirect(url_for('auth.chg_pass'))

        user = User.query.filter_by(email=current_user.email).first()
        if new_mdp == new_mdp2:
            user.password = generate_password_hash(new_mdp, method='sha256')
            db.session.commit()
        else:
            flash('Nouveau mot de passe non identiques', 'psw-nsame')
            return redirect(url_for('auth.chg_pass'))

        flash('Succès du changement de mot de passe', 'psw-success')
        return redirect(url_for('main.index'))

    return render_template('mdp.html')
