from .models import User
from flask import jsonify, request
from flask import Blueprint
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    set_access_cookies,
    set_refresh_cookies,
    create_refresh_token,
    get_jwt_identity,
    unset_jwt_cookies,
    jwt_refresh_token_required)
from flask_graphql import GraphQLView
from argon2 import PasswordHasher
from .schema import schema
from.extensions import db, jwtmanager

blueprint = Blueprint('general', __name__)

# Create a function that will be called whenever create_access_token
# is used. It will take whatever object is passed into the
# create_access_token method, and lets us define what custom claims
# should be added to the access token.
@jwtmanager.user_claims_loader
def add_claims_to_access_token(user):
    return {'role': str(user.role)}

# Create a function that will be called whenever create_access_token
# is used. It will take whatever object is passed into the
# create_access_token method, and lets us define what the identity
# of the access token should be.
@jwtmanager.user_identity_loader
def user_identity_lookup(user):
    return user.email


@blueprint.route('/token/auth', methods=['POST'])
def login_view():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    email = request.json.get('email', None)
    password = request.json.get('pass', None)
    if not email:
        return jsonify({"msg": "Missing email parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    result = User.query.filter_by(email=email).first()
    if result:
        ph = PasswordHasher()
        if ph.verify(result.password, password):
            access_token = create_access_token(identity=result)
            return jsonify(access_token=access_token), 200

    return jsonify({"msg": "Bad email or password"}), 401

# @blueprint.route('/token/auth', methods=['POST'])
# def login():
#     if not request.is_json:
#         return jsonify({"msg": "Missing JSON in request"}), 400

#     email = request.json.get('email', None)
#     password = request.json.get('pass', None)
#     result = User.query.filter_by(email=email).first()
#     if result:
#         ph = PasswordHasher()
#         if ph.verify(result.password, password):
#             # Create the tokens we will be sending back to the user
#             access_token = create_access_token(identity=result)
#             refresh_token = create_refresh_token(identity=result)

#             # Set the JWTs and the CSRF double submit protection cookies
#             # in this response
#             resp = jsonify({'login': True})
#             set_access_cookies(resp, access_token)
#             set_refresh_cookies(resp, refresh_token)
#             resp.set_cookie('loggedIn', 'True')
#             return resp, 200

#     return jsonify({"msg": "Bad email or password"}), 401


@blueprint.route('/token/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    # Create the new access token
    email = get_jwt_identity()
    result = User.query.filter_by(email=email).first()
    access_token = create_access_token(identity=result)

    # Set the access JWT and CSRF double submit protection cookies
    # in this response
    resp = jsonify({'refresh': True})
    set_access_cookies(resp, access_token)
    return resp, 200


# Because the JWTs are stored in an httponly cookie now, we cannot
# log the user out by simply deleting the cookie in the frontend.
# We need the backend to send us a response to delete the cookies
# in order to logout. unset_jwt_cookies is a helper function to
# do just that.
@blueprint.route('/token/remove', methods=['POST'])
def logout():
    resp = jsonify({'logout': True})
    unset_jwt_cookies(resp)
    # remove cookie
    resp.set_cookie('loggedIn', expires=0)
    return resp, 200


@blueprint.route('/api/example', methods=['GET'])
@jwt_required
def protected():
    email = get_jwt_identity()
    return jsonify({'hello': 'from {}'.format(email)}), 200


graphql_view = blueprint.route('/graphql')(jwt_required(GraphQLView.as_view('graphql', schema=schema.schema, context={'session': db.session},
                                                                            graphiql=True)))
