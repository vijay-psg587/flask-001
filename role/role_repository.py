from utils import mongo_client
from bson import ObjectId

DB = mongo_client().PIA_DB.roleT


def get_role_by_id(role_id):
    return DB.find_one({'_id': ObjectId(role_id)})
