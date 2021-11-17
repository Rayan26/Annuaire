from flask import Blueprint, render_template, request, flash, make_response
from flask_login import login_required, current_user
from sqlalchemy import and_

from . import db
from .models import Follow, Name
from .models import Post

feed = Blueprint('feed', __name__)


@feed.route('/name', methods=['POST'])
def name():
    # Reçoit les infos d'un nouveau nom
    print(request.json)
    print(request.data)
    try:
        d = request.json['data']
        name = d['name']
        id_user = d['id_user']
        n = Name(id_user=id_user, name=name)

        db.session.add(n)
        db.session.commit()

        return make_response(
            {"result": "ok"},
            200
        )
    except:
        return make_response(
            {"result": "error"},
            404
        )


@feed.route('/feed', methods=['GET', 'POST'])
@login_required
def feed_page():
    if request.method == 'POST':
        if 'post_message' in request.form and request.form.get('post_content'):
            post_content = request.form.get('post_content')
            from datetime import datetime
            new_post = Post(id_user=current_user.id, content=post_content, date=datetime.now())

            db.session.add(new_post)
            db.session.commit()
            flash("Votre post a été envoyé avec succès !", 'post-success')

        if 'post_follow' in request.form and request.form.get('name_follow'):
            id_user = current_user.id
            follow_name = request.form.get('name_follow')

            # Vérifie la présence de l'utilisateur
            user_to_follow = Name.query.filter_by(name=follow_name).first()
            if not user_to_follow:
                flash('Cette personne ne possède pas de compte', 'follow-error')
            elif user_to_follow.id == id_user:
                flash('Mais c\'est vous ça ! 😂', 'follow-error')
            else:
                # Vérifie la relation entre les deux utilisateurs
                following = Follow.query.filter_by(id_user=id_user).all()
                if any(user_to_follow.id == x.id_following for x in following):
                    flash("Vous suivez déjà cette personne", 'follow-error')
                else:
                    new_follow = Follow(id_user=id_user, id_following=user_to_follow.id)
                    db.session.add(new_follow)
                    db.session.commit()
                    flash(f"Vous venez de suivre {follow_name}", 'follow-success')

        if 'unf_name' in request.form and request.form.get('unf_name'):
            name_to_unfollow = request.form.get('unf_name')
            user_to_unfollow = Name.query.filter_by(name=name_to_unfollow).first()
            foll = Follow.query.filter(
                and_(Follow.id_user == current_user.id, Follow.id_following == user_to_unfollow.id)).first()
            db.session.delete(foll)
            db.session.commit()

    sub = db.session.query(Follow.id_following).filter_by(id_user=current_user.id).subquery()
    posts_user_follow = db.session.query(Post, Name) \
        .join(Name, Name.id_user == Post.id_user) \
        .filter(Post.id_user.in_(sub)) \
        .order_by(Post.date.desc()) \
        .all()
    posts_user = db.session.query(Post, Name) \
        .join(Name, Name.id_user == Post.id_user) \
        .filter(Post.id_user.in_([current_user.id])) \
        .order_by(Post.date.desc()) \
        .all()
    posts_user += posts_user_follow
    posts_user = sorted(posts_user, key=lambda x: x.Post.date, reverse=True)

    subq = db.session.query(Follow.id_following).filter_by(id_user=current_user.id).subquery()
    contacts = db.session.query(Name) \
        .filter(Name.id_user.in_(subq)) \
        .order_by(Name.name.asc()) \
        .all()

    return render_template('feed.html', user=current_user, posts_user=posts_user, contacts=contacts)
