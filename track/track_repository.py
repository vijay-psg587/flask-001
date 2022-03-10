import datetime

from pymongo.cursor import Cursor

from utils import mongo_client
from bson import ObjectId

DB = mongo_client().PIA_DB.trackT


def get_track_list(track_id=None):
    custom_filter = {}
    # we can have a kwargs, and we can use that as a whole for custom filters(might implement it later)
    if track_id is not None:
        custom_filter['_id'] = ObjectId(track_id)
    return DB.find(custom_filter)


def get_current_track_list():
    today = datetime.datetime.today()
    today = today.strftime('%Y-%m-%d')
    return DB.find({
        'start_date': {
            '$lte': today
        },
        'end_date': {
            '$gte': today
        }
    })


def get_track_by_name(name: str):
    return DB.find({"track_name": name})
