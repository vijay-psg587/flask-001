from flask import Blueprint, make_response, request, jsonify
from helpers.custom_decorators import login_required

from . import candidate_service

candidate_details_api = Blueprint("candidate_details_api", "candidate_details_api", url_prefix="/pl-analysis/v1/candidate/details")
candidate_report_api = Blueprint("candidate_report_api", "candidate_report_api", url_prefix="/pl-analysis/v1/candidate/report")


@candidate_details_api.get('')
@login_required
def get_candidate(current_user):
    track_id = request.args.get('track_id')
    if track_id is None:
        return make_response(jsonify([]), 200)
    data, status = candidate_service.get_candidate(track_id)
    response = make_response(data, status)
    response.headers.add_header('Content-Type', 'application/json')
    return response


@candidate_details_api.patch('')
@login_required
def patch(current_user):
    candidate_email: str = request.args.get("candidate_email")
    request_data = request.json
    data, status = candidate_service.patch_candidate(request_data, candidate_email)
    response = make_response(data, status)
    response.headers.add_header('Content-Type', 'application/json')
    return make_response(response, status)


@candidate_report_api.get('')
@login_required
def get_report(current_user):
    track_id = request.args.get('track_id')
    report_date = request.args.get('report_date')
    if track_id and report_date:
        data, status = candidate_service.get_candidate_report(track_id, report_date)
        response = make_response(data, status)
        response.headers.add_header('Content-Type', 'application/json')
        return response
    return make_response(jsonify([]), 200)
