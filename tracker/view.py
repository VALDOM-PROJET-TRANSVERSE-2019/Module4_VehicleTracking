"""
Routes for Flask app
"""
from flask import Flask, jsonify
from flask_restplus import Api, Resource, reqparse

from tracker import track2

APP = Flask(__name__)
APP.config.from_object('config')
API = Api(app=APP, version='1.0', title='Tracker API')
TRACK = API.namespace('Track', description="Tracker operations")


@TRACK.route('/')
class Tracker(Resource):
    """
    Resource class to generate Swagger for REST API
    """
    @TRACK.doc(params={'list_frame_contour': 'A path', "frame_path": 'A path'})
    def post(self):
        '''
        POST method, request the paths of images and bounding_boxes
        :return: json file
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('list_frame_contour', type=str,
                            required=True, help='Path to bounding boxes')
        parser.add_argument('frame_path', type=str,
                            required=True, help='Path to images')
        args = parser.parse_args()

        message = ""
        status = "success"
        if not args.list_frame_contour:
            status = 'error'
            message += 'missing list_frame_contour ; '
        if not args.frame_path:
            status = 'error'
            message += 'missing frame_path ; '

        output = track2.track(args.frame_path, args.list_frame_contour)

        if status == "error":
            return jsonify({
                'status': status,
                'message': message
            })
        else:
            return output
