#!/usr/bin/python3
""" reviews view """
from flask import make_response, jsonify, abort, request
from models import storage
from models.review import Review
from api.v1.views import app_views


@app_views.route("/places/<place_id>/reviews",
                 strict_slashes=False, methods=["GET"])
def get_place_reviews(place_id):
    """ get all place reviews objects """
    id = "Place.{}".format(place_id)
    if id in storage.all():
        review_objs = storage.all(Review)
        review_list = []

        for review_obj in review_objs:
            if review_objs[review_obj].place_id == place_id:
                review_list.append(review_objs[review_obj].to_dict())

        return jsonify(review_list)

    abort(404)


@app_views.route("/reviews/<review_id>", strict_slashes=False,
                 methods=["GET"])
def get_reviews(review_id):
    """ get all review objects """
    review_objs = storage.all(Review)

    for review_obj in review_objs:
        if review_obj.split(".")[1] == review_id:
            return jsonify(review_objs[review_obj].to_dict())
    abort(404)


@app_views.route("/reviews/<review_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_reviews(review_id):
    """ delete review objects """
    review_objs = storage.all(Review)

    for review_obj in review_objs:
        if review_obj.split(".")[1] == review_id:
            review_objs[review_obj].delete()
            storage.save()
            return jsonify({})
    abort(404)


@app_views.route("/places/<place_id>/reviews", strict_slashes=False,
                 methods=["POST"])
def post_reviews(place_id):
    """ create new review objects """
    id = "Place.{}".format(place_id)
    if id in storage.all():
        if request.mimetype == "application/json":
            json_data = request.get_json()
            if "user_id" in json_data:
                if "User.{}".format(json_data["user_id"]) in storage.all():
                    if "text" in json_data:
                        json_data["place_id"] = place_id
                        review = Review(**json_data)
                        review.save()
                        return make_response(jsonify(review.to_dict()), 201)
                    else:
                        abort(400, "Missing text")
                else:
                    abort(404)
            else:
                abort(400, "Missing user_id")
        else:
            abort(400, "Not a JSON")
    abort(404)


@app_views.route("/reviews/<review_id>", strict_slashes=False, methods=["PUT"])
def put_reviews(review_id):
    """ update review objects """
    id = "Review.{}".format(review_id)

    if id in storage.all():
        review = storage.all()[id]

        if request.mimetype == "application/json":
            json_data = request.get_json()

            for item in json_data:
                setattr(review, item, json_data[item])

            review.save()
            return make_response(jsonify(review.to_dict()), 200)
        else:
            abort(400, "Not a JSON")
    else:
        abort(404)
