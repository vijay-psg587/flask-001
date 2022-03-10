import traceback
from functools import wraps

import jwt
from flask import request, make_response

import settings
from appUser import user_service
from role import role_service


def login_required(function):
    @wraps(function)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', None)
        if token is None:
            return make_response({'errors': 'Authorization token is missing'}, 400)
        try:
            token = token.split(" ")[-1]
            current_user = jwt.decode(token, settings.JWT_SECRET, algorithms=settings.JWT_ENCODING_ALGO)
            current_user = user_service.find_user_by_email(current_user['email'])
        except Exception:
            traceback.print_exc()
            return make_response({'errors': 'Token is invalid or expired'}, 404)

        # get the role of the user
        role_id = current_user.get('role_id')
        role = role_service.get_role_by_id(role_id)
        current_user['role'] = role

        return function(current_user, *args, **kwargs)

    return decorated
