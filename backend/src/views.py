from flask import jsonify, request, Response, Blueprint
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
from .models import User
from .schema import schema
from .extensions import db, jwtmanager

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


@blueprint.route('/token/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    # Create the new access token
    email = get_jwt_identity()
    result = User.query.filter_by(email=email).first()
    access_token = create_access_token(identity=result)

    return jsonify(access_token=access_token), 200


graphql_view = blueprint.route('/graphql')(jwt_required(GraphQLView.as_view('graphql', schema=schema.schema, context={'session': db.session},
                                                                            graphiql=True)))
