"""
Routes for Flask app
"""
from bson import ObjectId
from flask import Flask, abort
from flask_restplus import Api, Resource, reqparse
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

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

    @TRACKJSON.doc(params={'list_frame_contour': 'A path', "frame_path": 'A path',
                           'distance_threshold': 'A float'})
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
class TrackerFromMongodb(Resource):
    """
    Resource class to generate Swagger for REST API
    """
    @TRACKMONGOBD.doc(params={"frame_path": 'A path',
                              'MongoDB_Address': 'A server address \'mongodb://localhost:27017/',
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

        try:
            max_sev_sel_delay = 2
            client = MongoClient(args.MongoDB_Address, serverSelectionTimeoutMS=max_sev_sel_delay)
            client.server_info()
        except ServerSelectionTimeoutError:
            abort(400, "Please enter a valid mongoDB address")
        except ValueError:
            abort(400, "Please enter a valid port address")



        if args.MongoDB_DataBase in client.list_database_names():
            data_base = client.get_database(args.MongoDB_DataBase)
        else:
            abort(400, "Please enter a valid database name")

        if args.MongoDB_Collection in data_base.list_collection_names():
            collection = data_base.get_collection(args.MongoDB_Collection)
        else:
            abort(400, "Please enter a valid collection name")

        json = collection.find_one({"_id": ObjectId(args.MongoDB_Document)})
        if json is None:
            abort(400, "No document found")
        else:
            del json['_id']
        output = track.track(args.frame_path, json, args.distance_threshold)
        return output
