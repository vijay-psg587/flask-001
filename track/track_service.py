import json
from typing import Tuple

from . import track_repository
from candidate import candidate_repository
from candidate import candidate_service
from .track_model import TrackSchema
from flask import jsonify, Response
from pymongo.cursor import Cursor

track_schema = TrackSchema()


def get_track_list(track_id=None):
    data = track_repository.get_track_list(track_id)
    if data is None:
        return jsonify({'errors': 'track(s) not found'}), 404
    return track_schema.dumps(data, many=True), 200


def get_current_track_list():
    data = track_repository.get_current_track_list()
    data_dump = track_schema.dumps(data, many=True)
    return data_dump, 200


def get_current_tracks_with_candidates() -> Tuple[Response, int]:
    result = {}
    current_tracks: Cursor = track_repository.get_current_track_list()
    if current_tracks is None:
        return jsonify({'errors': 'no tracks found'}), 404

    for current_track in current_tracks:
        current_track_id: str = str(current_track['_id'])
        res, _ = candidate_service.get_candidate(current_track_id)
        candidates = json.loads(res)
        result[current_track_id] = candidates

    return jsonify(result), 200
