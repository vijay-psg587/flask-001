from flask import Flask
from flask_cors import CORS

from appUser.user_controller import app_user_api
from candidate.candidate_controller import candidate_details_api, candidate_report_api
from pia_data.pia_data_controller import pia_data
from track.track_controller import track_api

app = Flask(__name__)
CORS(app)
app.register_blueprint(app_user_api)
app.register_blueprint(track_api)
app.register_blueprint(candidate_details_api)
app.register_blueprint(candidate_report_api)
app.register_blueprint(pia_data)
app.run(debug=True)


def create_app():
    CORS(app)
    app.register_blueprint(app_user_api)
    app.register_blueprint(track_api)
    app.register_blueprint(candidate_details_api)
    app.register_blueprint(candidate_report_api)
    app.register_blueprint(pia_data)
    app.run(debug=True)


if __name__ == '__main__':
    create_app()
