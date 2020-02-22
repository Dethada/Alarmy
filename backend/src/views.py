from flask import jsonify, request, Blueprint, abort
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_claims, get_jwt_identity
from flask_graphql import GraphQLView
from argon2 import PasswordHasher
from .models import User
from .schema import schema
from .extensions import db, jwtmanager, socketio
from .utils import broadcast_mail

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


@blueprint.route('/hooks/alerts', methods=['POST'])
@jwt_required
def alert_hook():
    if get_jwt_claims()['role'] != 'Service':
        abort(403)
    user = User.query.filter_by(email=get_jwt_identity()).first()
    req_data = request.get_json()
    #  msg['subject'], msg['content'], msg.get('img_attachment')
    '''
    {
        "deviceID": "ID",
        "email": {
            "subject": "test",
            "content": "content",
            "img_attachment": "data", # optional
        },
        "msg": "abcd"
    }
    '''
    broadcast_mail(req_data['deviceID'], req_data['email'])
    socketio.emit('alert', req_data['msg'], room=user.device_id)
    return 'Ok'


@blueprint.route('/hooks/data', methods=['POST'])
@jwt_required
def new_data():
    # if get_jwt_claims()['role'] != 'Service':
    #     abort(403)
    user = User.query.filter_by(email=get_jwt_identity()).first()
    socketio.emit('newValues', '', room=user.device_id)
    return 'Ok'


graphql_view = blueprint.route('/graphql')(jwt_required(GraphQLView.as_view('graphql', schema=schema.schema, context={'session': db.session},
                                                                            graphiql=True)))
