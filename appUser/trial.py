from pia.utils import mongo_client

DB = mongo_client().PIA_DB.user_test
print(DB.find({'email': {'$regex': 'aDmin3@admin.com', '$options':'i'}})[0])
