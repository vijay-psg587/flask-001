import time
from collections import defaultdict

from flask import jsonify
from marshmallow import ValidationError
from mergedeep import merge

from . import candidate_repository
from .candidate_model import CandidateResponseSchema

candidate_schema = CandidateResponseSchema(many=False)

COPIED_PERCENTAGE: str = 'total_percentage'


def _validate(candidate):
    try:
        validated_data = candidate_schema.load(candidate, partial=True)
        return validated_data
    except ValidationError as err:
        return err


def get_candidate(track_id):
    candidate_data = candidate_repository.get_candidates_by_track_id(track_id)
    response = candidate_schema.dumps(candidate_data, many=True)
    return response, 200


def candidate_comparator(candidate, track_id):
    return float(candidate.get('track_repos')[track_id][COPIED_PERCENTAGE])


def get_grouped_data(sorted_candidates_data, track_id, report_date):
    groups = [(0.0, 20.0), (21.0, 40.0), (41.0, 60.0), (61.0, 80.0), (81.0, 100.0)]  # need to make it dynamic
    """
    TODO:
    (max - min) // 5 will give the numbers to add to min
    """
    result = defaultdict(lambda: [])
    visited = defaultdict(lambda: 0)
    # partial sliding window approach
    for lower, upper in groups:
        candidates = []
        key = '{}-{}'.format(int(lower), int(upper))  # decimal zeroes are not required
        for window_end in range(len(sorted_candidates_data)):
            candidate_repo = sorted_candidates_data[window_end].get('track_repos')
            if not candidate_repo or visited[window_end]:
                continue
            if report_date in candidate_repo[track_id].keys():
                copied_percentage = float(candidate_repo[track_id][report_date][COPIED_PERCENTAGE]) * 100
                if lower <= copied_percentage <= upper:
                    candidates.append(sorted_candidates_data[window_end])
                    visited[window_end] += 1
                    result[key].append(str(sorted_candidates_data[window_end].get('_id')))

    return result


def patch_candidate(request_data, candidate_email):
    validated_data = _validate(request_data)
    if isinstance(validated_data, ValidationError):
        return jsonify({"errors": validated_data.messages}), 422
    if not candidate_email:
        return jsonify({"errors": "Candidate email missing in request query param"}), 400

    candidate_to_update = candidate_repository.get_candidate_by_email(candidate_email)
    if candidate_to_update is None:
        return jsonify({"errors": "No candidate found with email {}".format(candidate_email)}), 400
    updated_track_repo = request_data["track_repos"]
    candidate_to_update_track_repo = candidate_to_update['track_repos']

    candidate_to_update["track_repos"] = merge({}, candidate_to_update_track_repo, updated_track_repo)
    candidate_to_update["created_at"] = float("{:.2f}".format(float(str(candidate_to_update['created_at']))))
    candidate_to_update["updated_at"] = float("{:.2f}".format(time.time()))
    candidate_to_update["updated_by"] = "SQ_INTEGRATION_TOOL"

    response = candidate_repository.update(candidate_to_update)
    return candidate_schema.dumps(response), 200


def get_candidate_report(track_id, report_date):
    candidates_under_same_track = candidate_repository.get_candidates_by_track_id(track_id)
    sorted_candidates = sorted(candidates_under_same_track,
                               key=lambda candidate: candidate_comparator(candidate, track_id))
    result_value = get_grouped_data(sorted_candidates, track_id, report_date)
    return result_value, 200
