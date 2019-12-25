from .models import User
from flask import jsonify, request
from flask import Blueprint
from flask_jwt_extended import create_access_token, jwt_required
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


@blueprint.route('/login', methods=['POST'])
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
            # Identity can be any data that is json serializable
            access_token = create_access_token(identity=result)
            return jsonify(access_token=access_token), 200

    return jsonify({"msg": "Bad email or password"}), 401

'''
https://flask-jwt-extended.readthedocs.io/en/stable/tokens_from_complex_object/
@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    ret = {
        'current_identity': get_jwt_identity(),  # test
        'current_roles': get_jwt_claims()['roles']  # ['foo', 'bar']
    }
    return jsonify(ret), 200
'''
graphql_view = blueprint.route('/graphql')(GraphQLView.as_view('graphql', schema=schema, context={'session': db.session},
                                                               graphiql=True))
