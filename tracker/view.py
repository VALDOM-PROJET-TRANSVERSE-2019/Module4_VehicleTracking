"""
Routes for Flask app
"""

from flask import Flask, request, jsonify
from flask_restplus import Api, Resource

from tracker import track2

app = Flask(__name__)
app.config.from_object('config')
api = Api(app=app, version='1.0', title='Tracker API')
ns_track = api.namespace('Track', description="Tracker operations")


@ns_track.route('/')
class Tracker(Resource):
    @ns_track.doc(params={'list_frame_contour': 'A path', "frame_path": 'A path'})
    def post(self):
        list_frame_contour = request.args.get('list_frame_contour', None)
        frame_path = request.args.get('frame_path', None)

        message = ""
        status = "success"
        if not list_frame_contour:
            status = 'error'
            message += 'missing list_frame_contour ; '
        if not frame_path:
            status = 'error'
            message += 'missing frame_path ; '

        output = track2.track(frame_path, list_frame_contour)

        if status == "error":
            return jsonify({
                'status': status,
                'message': message
            })
        else:
            return output

