from utils import mongo_client
import bson


class PiaDataRepository:
    def __init__(self):
        self.cursor = mongo_client().PIA_DB.piaDataTest

    def get_pia_data(self):
        return self.cursor.find({})

    def get_pia_user_track_data(self, user_id, track_id, report_date):
        return self.cursor.find(
            {"usr_ctx": user_id, 'track_id': track_id,
             'report_date': report_date})

    def post_pia_data(self, request):
        return self.cursor.insert(request)

    def patch_pia_data(self, update_id, request):
        return self.cursor.update_one({'_id': update_id}, {'$set': request}, upsert=False)
