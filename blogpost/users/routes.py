from flask import jsonify, request, Blueprint
from werkzeug.security import check_password_hash
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    get_raw_jwt,
    jwt_required,
    jwt_refresh_token_required
)
from blogpost import mongo
from blogpost.users.utils import to_dict
from blogpost.utils import BLACKLIST

users = Blueprint('users', __name__)


@users.route('/signup', methods=['POST'])
def signup_user():
    if mongo.db.users.find_one({'username': request.json['username']}):
        return jsonify({'message': 'A user with the username already exists'})

    user_id = mongo.db.users.insert(to_dict(request))
    new_user = mongo.db.users.find_one({'_id': user_id})

    if new_user:
        return jsonify({'message': 'User has been successfuly signed up'}), 201
    else:
        return jsonify({'message': 'Error in user sign up'}), 500


@users.route('/login', methods=['POST'])
def login():
    user = mongo.db.users.find_one({'username': request.json['username']})

    if user and check_password_hash(user['password'], request.json['password']):
        access_token = create_access_token(identity=str(user['_id']),
                                           fresh=True)
        refresh_token = create_refresh_token(str(user['_id']))
        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 200

    return jsonify({'message': 'Invalid credentials'}), 401


@users.route('/logout', methods=['POST'])
@jwt_required
def logout():
    jti = get_raw_jwt()['jti']
    BLACKLIST.add(jti)
    return jsonify({'message': 'Successfuly logged out'})


@users.route('/refresh_token', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user, fresh=False)
    return jsonify({'access_token': new_token}), 200
