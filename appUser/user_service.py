import datetime

import bcrypt
import jwt
from flask import jsonify
from marshmallow import ValidationError

import settings
from . import user_repository
from .user_model import UserSchema, UserLoginSchema

user_schema = UserSchema()
user_login_schema = UserLoginSchema()


def get_auth_key(user):
    validated_data = _validate(user, user_login_schema)

    if isinstance(validated_data, ValidationError):
        return jsonify({"error": validated_data.messages}), 422

    db_user = user_repository.find_user_by_email(validated_data['email'])

    stored_hashed_pwd = db_user.get('password')
    entered_encoded_password = validated_data['password'].encode('utf-8')

    if db_user is None or not bcrypt.checkpw(entered_encoded_password, stored_hashed_pwd):
        return jsonify({'error': 'username or password is invalid'}), 400

    exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=settings.JWT_EXPIRY_IN_MIN)

    payload = {
        'email': db_user['email'],
        'username': db_user['name'],
        'exp': exp
    }

    jwt_token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ENCODING_ALGO)
    return jsonify({'token': jwt_token,
                    'username': db_user['name'],
                    'expires_at': round(exp.timestamp())}), 200


def find_user_by_email(email):
    db_user = user_repository.find_user_by_email(email)
    return db_user


def _validate(user, schema):
    try:
        validated_data = schema.load(user)
        return validated_data
    except ValidationError as err:
        return err


def save(user):
    validated_user = _validate(user, user_schema)

    #  don't know if this is the right way to pass errors or raise errors
    if isinstance(validated_user, ValidationError):
        return jsonify({"errors": validated_user.messages}), 422

    already_existing_user = user_repository.find_user_by_email(validated_user['email'])
    if already_existing_user is not None:
        return jsonify({"errors": 'user already exist with this email ID'}), 422

    plain_password = validated_user['password']
    encoded_password = bytes(plain_password, 'utf-8')
    validated_user['password'] = bcrypt.hashpw(encoded_password, bcrypt.gensalt(14))
    user_repository.save(validated_user)
    return user_schema.dumps(validated_user), 200
