#!/usr/bin/python3
""" places view """
from flask import make_response, jsonify, abort, request
from models import storage
from models.place import Place
from api.v1.views import app_views


@app_views.route("/cities/<city_id>/places",
                 strict_slashes=False, methods=["GET"])
def get_city_places(city_id):
    """ get all city places objects """
    id = "City.{}".format(city_id)
    if id in storage.all():
        place_objs = storage.all(Place)
        place_list = []

        for place_obj in place_objs:
            if place_objs[place_obj].city_id == city_id:
                place_list.append(place_objs[place_obj].to_dict())

        return jsonify(place_list)

    abort(404)


@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=["GET"])
def get_places(place_id):
    """ get all place objects """
    place_objs = storage.all(Place)

    for place_obj in place_objs:
        if place_obj.split(".")[1] == place_id:
            return jsonify(place_objs[place_obj].to_dict())
    abort(404)


@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_places(place_id):
    """ delete place objects """
    place_objs = storage.all(Place)

    for place_obj in place_objs:
        if place_obj.split(".")[1] == place_id:
            place_objs[place_obj].delete()
            storage.save()
            return jsonify({})
    abort(404)


@app_views.route("/cities/<city_id>/places", strict_slashes=False,
                 methods=["POST"])
def post_places(city_id):
    """ create new place objects """
    id = "City.{}".format(city_id)
    if id in storage.all():
        if request.mimetype == "application/json":
            json_data = request.get_json()
            if "user_id" in json_data:
                if "User.{}".format(json_data["user_id"]) in storage.all():
                    if "name" in json_data:
                        json_data["city_id"] = city_id
                        place = Place(**json_data)
                        place.save()
                        return make_response(jsonify(place.to_dict()), 201)
                    else:
                        abort(400, "Missing name")
                else:
                    abort(404)
            else:
                abort(400, "Missing user_id")
        else:
            abort(400, "Not a JSON")
    abort(404)


@app_views.route("/places/<place_id>", strict_slashes=False, methods=["PUT"])
def put_places(place_id):
    """ update place objects """
    id = "Place.{}".format(place_id)

    if id in storage.all():
        place = storage.all()[id]

        if request.mimetype == "application/json":
            json_data = request.get_json()

            for item in json_data:
                setattr(place, item, json_data[item])

            place.save()
            return make_response(jsonify(place.to_dict()), 200)
        else:
            abort(400, "Not a JSON")
    else:
        abort(404)
