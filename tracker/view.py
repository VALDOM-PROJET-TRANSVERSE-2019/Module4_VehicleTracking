"""
Routes for Flask app
"""
from bson import ObjectId
from flask import Flask
from flask_restplus import Api, Resource, reqparse
from pymongo import MongoClient

from tracker import track

APP = Flask(__name__)
APP.config.from_object('config')
API = Api(app=APP, version='1.0', title='Tracker API')
TRACKJSON = API.namespace('Track_from_JSON', description="Tracker GET from JSON")
TRACKMONGOBD = API.namespace('Track_from_MongoDB', description="Tracker GET from MongoDB")


@TRACKJSON.route('/')
class TrackerFromJson(Resource):
    """
    Resource class to generate Swagger for REST API
    """

    @TRACKJSON.doc(params={'list_frame_contour': 'A path', "frame_path": 'A path', 'distance_threshold': 'A float'})
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
        parser.add_argument('distance_threshold', type=float,
                            help='Distance at which a new detectedObject will not be associated with a Vehicle',
                            default=0.2)
        args = parser.parse_args()

        output = track.track(args.frame_path, args.list_frame_contour, args.distance_threshold)
        return output


@TRACKMONGOBD.route('/')
class TrackerFromJson(Resource):
    """
    Resource class to generate Swagger for REST API
    """
    @TRACKMONGOBD.doc(params={"frame_path": 'A path',
                              'MongoDB_Address': 'A server address',
                              "MongoDB_DataBase": 'A database name',
                              "MongoDB_Collection": 'Input Collection name',
                              "MongoDB_Document": 'Document name',
                              'distance_threshold': 'A float'})
    def get(self):
        """
        GET method, request the paths of images and bounding_boxes
        :return: json file
        """
        parser = reqparse.RequestParser()
        parser.add_argument('frame_path', type=str,
                            required=True, help='Path to images')
        parser.add_argument('MongoDB_Address', type=str,
                            required=True, help='A server address \'mongodb://localhost:27017/\'')
        parser.add_argument('MongoDB_DataBase', type=str,
                            required=True, help='A database name')
        parser.add_argument('MongoDB_Collection', type=str,
                            required=True, help='Input Collection name')
        parser.add_argument('MongoDB_Document', type=str,
                            required=True, help='Input Document _id')
        parser.add_argument('distance_threshold', type=float,
                            help='Distance at which a new detectedObject will not be associated with a Vehicle',
                            default=0.2)
        args = parser.parse_args()
        data_base = args.MongoDB_DataBase
        collection = args.MongoDB_Collection
        client = MongoClient(args.MongoDB_Address)
        json = client.data_base[collection].find_one({"_id": ObjectId(args.MongoDB_Document)})
        del json['_id']
        output = track.track(args.frame_path, json, args.distance_threshold)
        return output
