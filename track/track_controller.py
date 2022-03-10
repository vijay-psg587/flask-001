from flask import Blueprint, jsonify, make_response, request
from flask_cors import CORS
from helpers.custom_decorators import login_required
from . import track_service

track_api = Blueprint('track_api', 'track_api', url_prefix='/api/track')

CORS(track_api)


@track_api.get('')
@login_required
def get_track(user):
    role = user.get('role', None)
    current_track = request.args.get('current')  # current track means: today's tracks

    if role.get('name') == 'Track_Admin':
        if current_track:
            response, status = track_service.get_current_track_list()
        else:
            response, status = track_service.get_track_list()
    elif role.get('name') == 'Track_Admin':
        response, status = track_service.get_track_list()
    elif role.get('name') == 'Track_Evaluator':
        response, status = track_service.get_track_list(track_id=user.get('track_id'))
    else:
        response, status = jsonify({'errors': 'invalid role'}), 400

    response = make_response(response, status)
    response.headers.add_header('Content-Type', 'application/json')
    return response


@track_api.get('/current')
@login_required
def get_tracks_with_candidate(user):
    response, status = track_service.get_current_tracks_with_candidates()
    return make_response(response, status)
