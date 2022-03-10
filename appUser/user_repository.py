from utils import mongo_client

DB = mongo_client().PIA_DB.userT


def find_user_by_email(email: str) -> dict:
    return DB.find_one({'email': {'$regex': email, '$options': 'i'}})


def save(user):
    return DB.insert_one(user)
