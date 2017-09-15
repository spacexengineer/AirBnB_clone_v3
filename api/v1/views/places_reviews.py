#!/usr/bin/python3
"""RESTful Reviews API"""
from flask import abort, Flask, jsonify, request
from api.v1.views import app_views
from models import storage
from models.base_model import BaseModel
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_all_place_reviews(place_id):
    """show all reviews for a place in json format"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    reviews = []
    for review in storage.all('Review').values():
        if review.place_id == place_id:
            reviews.append(review.to_json())
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    """retrieve review matching id """
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_json())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """delete review matching id"""
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """create a new review"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    kwargs = request.get_json()
    if kwargs is None:
        return ('Not a JSON', 400)
    if 'user_id' not in kwargs:
        return ('Missing user_id', 400)
    if 'text' not in kwargs:
        return ('Missing text', 400)

    new_review = Review(**kwargs)
    new_review.place_id = place_id
    user = storage.get('User', review.user_id)
    if user is None:
        abort(404)
    new_review.save()
    return jsonify(new_review.to_json()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def put_review(review_id):
    """update attribute in review """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    kwargs = request.get_json()
    if kwargs is None:
        return ("Not a JSON", 400)
    for k, v in kwargs.items():
        setattr(review, k, v)
    review.save()
    return (jsonify(review.to_json()), 200)
