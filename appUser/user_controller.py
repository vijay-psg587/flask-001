from flask import Blueprint, request, make_response
from flask_cors import CORS

from . import user_service

app_user_api = Blueprint('app_user', 'app_user')
CORS(app_user_api)


# not using auth form request.authorization because we may need to get role in
# future as well
@app_user_api.route("/login", methods=['POST'])
def login():
    json_data = request.get_json()
    response, status = user_service.get_auth_key(json_data)
    response = make_response(response, status)
    response.headers.add_header('Content-Type', 'application/json')
    return response


@app_user_api.route("/register", methods=['POST'])
def register():
    json_data = request.get_json()
    response, status = user_service.save(json_data)
    response = make_response(response, status)
    response.headers.add_header('Content-Type', 'application/json')
    return response
