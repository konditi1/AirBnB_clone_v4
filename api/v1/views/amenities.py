#!/usr/bin/python3
""" amenities view """
from flask import make_response, jsonify, abort, request
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=["GET"])
@app_views.route("/amenities", strict_slashes=False, methods=["GET"])
def get_amenities(amenity_id=None):
    """ get all amenity objects """
    amenity_objs = storage.all(Amenity)

    if amenity_id:
        for amenity_obj in amenity_objs:
            if amenity_obj.split(".")[1] == amenity_id:
                return jsonify(amenity_objs[amenity_obj].to_dict())
        abort(404)

    amenity_list = []

    for amenity_obj in amenity_objs:
        amenity_list.append(amenity_objs[amenity_obj].to_dict())

    return jsonify(amenity_list)


@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_amenities(amenity_id):
    """ delete amenity objects """
    amenity_objs = storage.all(Amenity)

    for amenity_obj in amenity_objs:
        if amenity_obj.split(".")[1] == amenity_id:
            amenity_objs[amenity_obj].delete()
            storage.save()
            return jsonify({})
    abort(404)


@app_views.route("/amenities", strict_slashes=False, methods=["POST"])
def post_amenities():
    """ create new amenity objects """
    if request.mimetype == "application/json":
        json_data = request.get_json()
        if "name" in json_data:
            amenity = Amenity(**json_data)
            amenity.save()
            return make_response(jsonify(amenity.to_dict()), 201)
        else:
            abort(400, "Missing name")
    else:
        abort(400, "Not a JSON")


@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=["PUT"])
def put_amenities(amenity_id):
    """ update amenity objects """
    id = "Amenity.{}".format(amenity_id)

    if id in storage.all():
        amenity = storage.all()[id]

        if request.mimetype == "application/json":
            json_data = request.get_json()

            for item in json_data:
                setattr(amenity, item, json_data[item])

            amenity.save()
            return make_response(jsonify(amenity.to_dict()), 200)
        else:
            abort(400, "Not a JSON")
    else:
        abort(404)
