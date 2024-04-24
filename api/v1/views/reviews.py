#!/usr/bin/python3
"""This is the review controls"""
from flask import Flask, Blueprint, jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User

app = Flask(__name__)
places_reviews_api = Blueprint('places_reviews_api', __name__)


@places_reviews_api.route('/api/v1/places/<place_id>/reviews', methods=['GET'])
def get_place_reviews(place_id):
    """
    Retrieve all reviews for a specific place.

    Args:
        place_id (str): The ID of the place.

    Returns:
        Flask Response: A JSON response containing the reviews for the place.

    Raises:
        404: If the place with the given ID does not exist.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@places_reviews_api.route('/api/v1/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    """
    Retrieve a specific review by its ID.

    Args:
        review_id (str): The ID of the review to retrieve.

    Returns:
        dict: A dictionary representation of the review.

    Raises:
        404: If the review with the specified ID does not exist.
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@places_reviews_api.route('/api/v1/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """
    Delete a review by its ID.

    Args:
        review_id (str): The ID of the review to be deleted.

    Returns:
        tuple: A tuple containing an empty JSON response and a status code of 200.

    Raises:
        404: If the review with the given ID does not exist.
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@places_reviews_api.route('/api/v1/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """
    Create a new review for a place.

    Args:
        place_id (str): The ID of the place.

    Returns:
        tuple: A tuple containing the JSON response and the HTTP status code.

    Raises:
        404: If the place with the given ID does not exist.
        400: If the request is not in JSON format, or if the 'user_id' or 'text' fields are missing.

    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    if 'user_id' not in request.json:
        abort(400, 'Missing user_id')
    if 'text' not in request.json:
        abort(400, 'Missing text')
    user_id = request.json['user_id']
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    data = request.json
    data['place_id'] = place_id
    review = Review(**data)
    review.save()
    return jsonify(review.to_dict()), 201


@places_reviews_api.route('/api/v1/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """
    Update a review by its ID.

    Args:
        review_id (str): The ID of the review to be updated.

    Returns:
        tuple: A tuple containing the JSON representation of the updated review and the HTTP status code.

    Raises:
        404: If the review with the given ID does not exist.
        400: If the request data is not in JSON format.
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    data = request.json
    for key, value in data.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
