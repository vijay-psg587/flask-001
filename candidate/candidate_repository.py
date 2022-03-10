from pymongo import ReturnDocument

from utils import mongo_client
from .candidate_model import CandidateResponseSchema

DB = mongo_client().PIA_DB.candidatesT
candidate_schema = CandidateResponseSchema(many=True)


def get_candidates_by_track_id(track_id):
    cursor = DB.find({'tracks': {'$elemMatch': {'$eq': track_id}}})
    return list(cursor)


def get_candidate_by_email(candidate_email: str):
    cursor = DB.find_one({'email': {'$regex': candidate_email, '$options': 'i'}})
    return cursor


def update(candidate_to_update):
    cursor = DB.find_one_and_update({'email': candidate_to_update['email']},
                                    {'$set': candidate_to_update}, return_document=ReturnDocument.AFTER)
    return cursor
