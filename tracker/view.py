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
    def get(self):
        """
        GET method, request the paths of images and bounding_boxes
        :return: json file
        """
        parser = reqparse.RequestParser()
        parser.add_argument('list_frame_contour', type=str,
                            required=True, help='Bounding boxes (json)')
        parser.add_argument('frame_path', type=str,
                            required=True, help='Path to images')
        args = parser.parse_args()

        output = track2.track(args.frame_path, args.list_frame_contour)
        return output
