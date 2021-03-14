import datetime
import uuid
from functools import wraps

import jwt
from flask import request, jsonify, make_response, Blueprint
from werkzeug.security import check_password_hash, generate_password_hash

from FlaskProjectFolder import db, app
from FlaskProjectFolder.models.user import User

auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@auth_blueprint.route('/')
def auth_blueprint_index():
    return jsonify({"message": "Welcome to the auth endpoints"})


@auth_blueprint.route('/register', methods=['POST'])
def create_user():
    data = request.get_json()
    try:
        username = data['username']
    except KeyError:
        return jsonify({"message": "the username field must be filled"}), 406
    try:
        password = data['password']
    except KeyError:
        return jsonify({"message": "the password field must be filled"}), 406
    try:
        name = data['name']
    except KeyError:
        return jsonify({"message": "the name field must be filled"}), 406
    try:
        gender = data['gender']
    except KeyError:
        return jsonify({"message": "the gender field must be filled"}), 406
    try:
        email = data['email']
    except KeyError:
        return jsonify({"message": "the email field must be filled"}), 406
    try:
        phone_number = data['phone_number']
    except KeyError:
        return jsonify({"message": "the phone number field must be filled"}), 406

    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'the username is already used!'}), 406

    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'the email is already used!'}), 406

    hashed_password = generate_password_hash(password, method='md5')
    public_id = str(uuid.uuid4())
    new_user = User(public_id=public_id, username=username, password=hashed_password, name=name, gender=gender,
                    email=email,
                    phone_number=phone_number)
    db.session.add(new_user)
    db.session.commit()

    user = User.query.filter_by(public_id=public_id).first()
    user_data = {'public_id': user.public_id, 'name': user.name, 'username': user.username, 'gender': user.gender,
                 'email': user.email,
                 'phone_number': user.phone_number, 'date_registered': user.date_registered}

    return jsonify({'message': 'New user created!',
                    'detail_user': user_data}), 201


@auth_blueprint.route('/login')
def login_user():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response(jsonify({'message': 'please fill the username field and the password field correctly'}),
                             401,
                             {'WWW-Authenticate': 'Basic realm="Login required!"'})
    user = User.query.filter_by(username=auth.username).first()
    if not user:
        return make_response(jsonify({'message': 'wrong username!, please check your username first !.'}), 401,
                             {'WWW-Authenticate': 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode(
            {'public_id': user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
            app.config['SECRET_KEY'])

        return jsonify({'token': token.decode('UTF-8')})
    else:
        return make_response(jsonify({'message': 'wrong password!, please check your password again !.'}), 401,
                             {'WWW-Authenticate': 'Basic realm="Login required!"'})

# @app.route('/user/<public_id>', methods=['GET'])
# @token_required
# def get_one_user(current_user, public_id):
#     user = tbl_user.query.filter_by(public_id=public_id).first()
#
#     if not user:
#         return make_response(jsonify({'message': 'No user found!'}), 404)
#
#     if current_user.public_id != public_id:
#         return make_response(jsonify({'message': 'Cannot perform that function!'}), 403)
#
#     user_data = {'public_id': user.public_id, 'name': user.name, 'username': user.username, 'gender': user.gender,
#                  'email': user.email
#         , 'phone_number': user.phone_number, 'date_registered': user.date_registered}
#
#     return make_response(jsonify({'user': user_data}), 202)
