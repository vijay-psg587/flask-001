from flask import Blueprint, make_response
from flask_cors import CORS
from bson import json_util
from .pia_data_repository import PiaDataRepository
from .pia_data_service import PiaDataService
from flask import request
from helpers.custom_decorators import login_required

pia_data = Blueprint('pia_data', 'pia_data', url_prefix='/api/pia-data')
pia_data_repo = PiaDataRepository()
pia_service = PiaDataService(pia_data_repo)
CORS(pia_data)


@pia_data.get("/")
@login_required
def pia_data_get(current_user):
    if request.args.get('userId') and request.args.get('trackId') and request.args.get('report_date'):
        data, status = pia_service.get_pia_user_track_data(request.args.get('userId'), request.args.get('trackId'),
                                                request.args.get('report_date'), request.args.get('filename'),
                                                request.args.get('referenceUserName'))
        response = make_response(json_util.dumps(data), status)
        response.headers.add_header('Content-Type', 'application/json')
        return response

    data, status = pia_service.get_pia_data()
    response = make_response(json_util.dumps(data), status)
    response.headers.add_header('Content-Type', 'application/json')
    return response


@pia_data.post("/")
@login_required
def pia_data_post(current_user):
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        json = request.json
        data, status = pia_service.post_put_pia_data(json)
        response = make_response(data, status)
        return response

