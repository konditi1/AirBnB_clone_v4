#!/usr/bin/python3
""" users view """
from flask import make_response, jsonify, abort, request
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route("/users/<user_id>", strict_slashes=False, methods=["GET"])
@app_views.route("/users", strict_slashes=False, methods=["GET"])
def get_users(user_id=None):
    """ get all user objects """
    user_objs = storage.all(User)

    if user_id:
        for user_obj in user_objs:
            if user_obj.split(".")[1] == user_id:
                return jsonify(user_objs[user_obj].to_dict())
        abort(404)

    user_list = []

    for user_obj in user_objs:
        user_list.append(user_objs[user_obj].to_dict())

    return jsonify(user_list)


@app_views.route("/users/<user_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_users(user_id):
    """ delete user objects """
    user_objs = storage.all(User)

    for user_obj in user_objs:
        if user_obj.split(".")[1] == user_id:
            user_objs[user_obj].delete()
            storage.save()
            return jsonify({})
    abort(404)


@app_views.route("/users", strict_slashes=False, methods=["POST"])
def post_users():
    """ create new user objects """
    if request.mimetype == "application/json":
        json_data = request.get_json()
        if "email" in json_data:
            if "password" in json_data:
                user = User(**json_data)
                user.save()
                return make_response(jsonify(user.to_dict()), 201)
            else:
                abort(400, "Missing password")
        else:
            abort(400, "Missing email")
    else:
        abort(400, "Not a JSON")


@app_views.route("/users/<user_id>", strict_slashes=False, methods=["PUT"])
def put_users(user_id):
    """ update user objects """
    id = "User.{}".format(user_id)

    if id in storage.all():
        user = storage.all()[id]

        if request.mimetype == "application/json":
            json_data = request.get_json()

            for item in json_data:
                setattr(user, item, json_data[item])

            user.save()
            return make_response(jsonify(user.to_dict()), 200)
        else:
            abort(400, "Not a JSON")
    else:
        abort(404)
