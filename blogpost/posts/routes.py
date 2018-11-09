from flask import request, jsonify, Blueprint
from pymongo import ReturnDocument, DESCENDING
from bson.objectid import ObjectId, InvalidId
from flask_jwt_extended import jwt_required
from blogpost import mongo
from blogpost.posts.utils import to_dict, id_to_str

posts = Blueprint('posts', __name__)


@posts.route('/post', methods=['GET'])
def get_all_posts():
    output = []
    for q in mongo.db.posts.find().sort('date_posted', DESCENDING):
        output.append(id_to_str(q))
    return jsonify({'result': output})


@posts.route('/post/<string:post_id>', methods=['GET'])
def get_post(post_id):
    try:
        q = mongo.db.posts.find_one_or_404({'_id': ObjectId(post_id)})
    except (InvalidId, TypeError):
        return jsonify({'message': 'Requested post_id is Invalid'}), 404
    return jsonify({'result': id_to_str(q)})


@posts.route('/post', methods=['POST'])
@jwt_required
def add_post():
    post_id = mongo.db.posts.insert(to_dict(request))
    new_post = mongo.db.posts.find_one({'_id': post_id})
    return jsonify({'result': id_to_str(new_post)}), 201


@posts.route('/post/<string:post_id>', methods=['PUT'])
@jwt_required
def update_post(post_id):
    try:
        post = mongo.db.posts.find_one_and_update({'_id': ObjectId(post_id)},
                                                  {'$set': to_dict(request)},
                                                  return_document=ReturnDocument.AFTER)
    except (InvalidId, TypeError):
        return jsonify({'message': 'Requested post_id is Invalid'}), 404
    return jsonify({'result': id_to_str(post)})


@posts.route('/post/<string:post_id>', methods=['DELETE'])
@jwt_required
def delete_post(post_id):
    try:
        post = mongo.db.posts.find_one_and_delete({'_id': ObjectId(post_id)})
    except (InvalidId, TypeError):
        return jsonify({'message': 'Requested post_id is Invalid'}), 404
    return jsonify({'message': 'Post deletion successful'})
