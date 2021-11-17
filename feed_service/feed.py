from flask import Blueprint, request, make_response
from sqlalchemy import and_

from feed_service import db
from .models import Follow, Name
from .models import Post

feed = Blueprint('feed', __name__)


@feed.route('/name', methods=['POST'])
def name():
    # Reçoit les infos d'un nouveau nom
    d = request.json
    name_ = d['name']
    id_user = d['id_user']
    n = Name(id_user=id_user, name=name_)

    db.session.add(n)
    db.session.commit()

    return make_response(
        {"result": "ok"},
        200
    )


@feed.route('/feed/message', methods=['POST'])
def feed_post():
    json_request = request.json

    from datetime import datetime
    new_post = Post(id_user=json_request['id_user'],
                    content=json_request['content'], date=datetime.now())

    db.session.add(new_post)
    db.session.commit()

    return make_response(
        {"result": "ok"},
        200
    )


@feed.route('/feed/follow', methods=['POST'])
def feed_follow():
    json_request = request.json
    id_user = json_request['id_user']
    follow_name = json_request['follow_name']
    user_to_follow = Name.query.filter_by(name=follow_name).first()

    # User n'existe pas
    if not user_to_follow:
        return make_response(
            {"result": "error",
             "msg": "Cette personne ne possède pas de compte"
             },
            400
        )

    # C'est toi
    if user_to_follow.id_user == id_user:
        return make_response(
            {"result": "error", "msg": "Mais c\'est vous ça ! 😂"},
            400
        )

    # User déjà suivi
    following = Follow.query.filter_by(id_user=id_user).all()
    if any(user_to_follow.id == x.id_following for x in following):
        return make_response(
            {"result": "error", "msg": "Vous suivez déjà cette personne"},
            400
        )

    new_follow = Follow(id_user=id_user, id_following=user_to_follow.id_user)
    db.session.add(new_follow)
    db.session.commit()
    return make_response(
        {"result": "ok"},
        200
    )


@feed.route('/feed/unfollow', methods=['POST'])
def feed_unfollow():
    json_request = request.json
    id_user = json_request['id_user']
    name_to_unfollow = json_request['unf_name']

    user_to_unfollow = Name.query.filter_by(name=name_to_unfollow).first()
    if not user_to_unfollow:
        return make_response(
            {"result": "error"},
            404
        )

    foll = Follow.query.filter(
        and_(Follow.id_user == id_user, Follow.id_following == user_to_unfollow.id_user)
    ).first()
    if foll:
        db.session.delete(foll)
        db.session.commit()
        return make_response(
            {"result": "ok"},
            200
        )
    else:
        return make_response(
            {"result": "error"},
            404
        )


@feed.route('/feed_page', methods=['GET'])
def feed_page():
    json_request = request.json
    id_user = json_request['id_user']

    sub = db.session.query(Follow.id_following).filter_by(id_user=id_user).subquery()
    posts_user_follow = db.session.query(Post, Name) \
        .join(Name, Name.id_user == Post.id_user) \
        .filter(Post.id_user.in_(sub)) \
        .order_by(Post.date.desc()) \
        .all()
    posts_user = db.session.query(Post, Name) \
        .join(Name, Name.id_user == Post.id_user) \
        .filter(Post.id_user.in_([id_user])) \
        .order_by(Post.date.desc()) \
        .all()
    posts_user += posts_user_follow
    posts_user = sorted(posts_user, key=lambda x: x.Post.date, reverse=True)
    print(posts_user)
    caca = []
    for p in posts_user:
        po = p.Post.as_dict()
        na = p.Name.as_dict()
        caca += [(po, na)]

    subq = db.session.query(Follow.id_following).filter_by(id_user=id_user).subquery()
    contacts = db.session.query(Name) \
        .filter(Name.id_user.in_(subq)) \
        .order_by(Name.name.asc()) \
        .all()
    print(contacts)
    cont = [x.as_dict() for x in contacts]

    return make_response(
        {"result": "ok", "posts_user": caca, "contacts": cont},
        200
    )
