import json
import time
from datetime import datetime
import bson
from bson import json_util
from marshmallow import ValidationError

from candidate.candidate_repository import get_candidate_by_email
from candidate.candidate_service import patch_candidate
from .pia_data_model import PiaDataResponseSchema
from .pia_data_repository import PiaDataRepository
from track import track_repository

pia_data_controller = PiaDataResponseSchema(many=False)


def _validate(candidate):
    try:
        validated_data = pia_data_controller.load(candidate, partial=True)
        return validated_data
    except ValidationError as err:
        return err


class PiaDataService:
    def __init__(self, pia_repository: PiaDataRepository):  # candidate_repository
        self.pia_repository = pia_repository

    def get_pia_data(self):
        return self.pia_repository.get_pia_data(), 200

    def get_pia_user_track_data(self, user_id, track_id, report_date, filename, reference_user_name):
        try:
            pia_report = dict(self.pia_repository.get_pia_user_track_data(bson.objectid.ObjectId(user_id),
                                                                          bson.objectid.ObjectId(track_id),
                                                                          report_date)[0])[
                'pia_report']
            print(pia_report)
            if filename and reference_user_name:
                record = pia_report[filename.replace('\\\\', '\\')]
                copied_record = [val for val in record if
                                 val['reference_file'] == reference_user_name.replace('\\\\', '\\')]
                return {
                           'copy_percent': copied_record[0]['percentage_of_copy'],
                           'copied_file_name': copied_record[0]['reference_file'],
                           'html_test_file': copied_record[0]['test_file_copied_lines'],
                           'html_reference_file': copied_record[0]['reference_file_copied_lines'],
                       }, 200
            return_value = []
            for key, value in pia_report.items():
                copied_users = [{'id': val['reference_file'], 'name': val['copied_user'],
                                 'percentage_of_copy': val['percentage_of_copy']}
                                for val in value if 'reference_file' in val]
                if value:
                    return_value.append({
                        'file_name': key,
                        'copied_users': copied_users,
                        'html_test_file': value[0]['test_file_copied_lines']
                    })
            return return_value, 200
        except:
            return 'Not found', 404

    def post_put_pia_data(self, request):
        # TODO: add startDate__gte=start_date for mvp 2
        today_date = datetime.today().strftime('%Y-%m-%d')
        track_id = dict(track_repository.get_track_by_name(request['track_name'].title() + ' Track')[0])['_id']

        candidate_update_data = {
            'track_repos': {
                str(track_id): {
                    today_date: {
                        'total_copy_percentage': request['total_copy_percentage']
                    }
                }
            }
        }
        user_id, status = patch_candidate(candidate_update_data,
                                          request['usrName'].upper() + '@deloitte.com'.upper(), 'copy-detect-tool')
        if status == 200:
            try:
                user_id = dict(get_candidate_by_email(request['usrName'].upper() + '@deloitte.com'.upper()))['_id']
            except:
                return "User not found", 500
        else:
            return "User not found", 500

        pia_present = self.pia_repository.get_pia_user_track_data(bson.objectid.ObjectId(user_id),
                                                                  bson.objectid.ObjectId(track_id),
                                                                  today_date)
        data = {
            'track_name': request['track_name'].upper(),
            'created_at': float("{:.2f}".format(time.time())),
            'updated_at': float("{:.2f}".format(time.time())),
            'created_by': 'copy-detect-tool',
            'updated_by': 'copy-detect-tool',
            'track_id': track_id,
            'usr_ctx': user_id,
            'pia_report': request['piaReport'],
            'report_date': today_date
        }
        validated_data = _validate(data)
        if isinstance(validated_data, ValidationError):
            return json_util.dumps({"errors": validated_data.messages}), 422

        try:
            pia_data = dict(pia_present[0])
            pia_id = pia_data['_id']
            return str(self.pia_repository.patch_pia_data(pia_id, data)), 200
        except:
            return str(self.pia_repository.post_pia_data(data)), 201
