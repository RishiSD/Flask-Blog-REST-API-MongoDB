from flask import jsonify, request, Blueprint
from werkzeug.security import check_password_hash
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    jwt_refresh_token_required,
    set_access_cookies,
    set_refresh_cookies,
    unset_jwt_cookies
)
from blogpost import mongo
from blogpost.users.utils import to_dict

users = Blueprint('users', __name__)


@users.route('/signup', methods=['POST'])
def signup_user():
    if mongo.db.users.find_one({'username': request.json['username']}):
        return jsonify({'message': 'A user with the username already exists'})

    user_id = mongo.db.users.insert(to_dict(request))
    new_user = mongo.db.users.find_one({'_id': user_id})

    if new_user:
        return jsonify({'message': 'User has been successfuly signed up',
                        'signup': True}), 201
    else:
        return jsonify({'message': 'Error in user sign up',
                        'signup': False}), 500


@users.route('/login', methods=['POST'])
def login():
    #print(request.json['username'])
    user = mongo.db.users.find_one({'username': request.json['username']})
    #print(user['username'])
    if user and check_password_hash(user['password'], request.json['password']):
        access_token = create_access_token(identity=str(user['_id']),
                                           fresh=True)
        refresh_token = create_refresh_token(str(user['_id']))
        resp = jsonify({'login': True})
        set_access_cookies(resp, access_token)
        set_refresh_cookies(resp, refresh_token)
        return resp, 200

    return jsonify({'message': 'Invalid credentials',
                    'login': False}), 401


@users.route('/logout', methods=['GET'])
def logout():
    resp = jsonify({'logout': True})
    unset_jwt_cookies(resp)
    return resp, 200


@users.route('/refresh_token', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user, fresh=False)
    resp = jsonify({'refresh': True})
    set_access_cookies(resp, new_token)
    return resp, 200
