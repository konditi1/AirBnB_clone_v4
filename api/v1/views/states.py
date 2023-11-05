#!/usr/bin/python3
""" states view """
from flask import make_response, jsonify, abort, request
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route("/states/<state_id>", strict_slashes=False, methods=["GET"])
@app_views.route("/states", strict_slashes=False, methods=["GET"])
def get_states(state_id=None):
    """ get all state objects """
    state_objs = storage.all(State)

    if state_id:
        for state_obj in state_objs:
            if state_obj.split(".")[1] == state_id:
                return jsonify(state_objs[state_obj].to_dict())
        abort(404)

    state_list = []

    for state_obj in state_objs:
        state_list.append(state_objs[state_obj].to_dict())

    return jsonify(state_list)


@app_views.route("/states/<state_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_states(state_id):
    """ delete state objects """
    state_objs = storage.all(State)

    for state_obj in state_objs:
        if state_obj.split(".")[1] == state_id:
            state_objs[state_obj].delete()
            storage.save()
            return jsonify({})
    abort(404)


@app_views.route("/states", strict_slashes=False, methods=["POST"])
def post_states():
    """ create new state objects """
    if request.mimetype == "application/json":
        json_data = request.get_json()
        if "name" in json_data:
            state = State(**json_data)
            state.save()
            return make_response(jsonify(state.to_dict()), 201)
        else:
            abort(400, "Missing name")
    else:
        abort(400, "Not a JSON")


@app_views.route("/states/<state_id>", strict_slashes=False, methods=["PUT"])
def put_states(state_id):
    """ update state objects """
    id = "State.{}".format(state_id)

    if id in storage.all():
        state = storage.all()[id]

        if request.mimetype == "application/json":
            json_data = request.get_json()

            for item in json_data:
                setattr(state, item, json_data[item])

            state.save()
            return make_response(jsonify(state.to_dict()), 200)
        else:
            abort(400, "Not a JSON")
    else:
        abort(404)
