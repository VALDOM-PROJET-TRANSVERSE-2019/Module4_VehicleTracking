import os
from flask import Flask, request, jsonify

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/tracking')
    def getTracking():
        list_frame_contour = request.args.get('list_frame_contour',None)
        frame_path = request.args.get('frame_path',None)

        message = ""
        status="success"
        if not list_frame_contour:
            status='error'
            message += 'missing list_frame_contour ; '
        if not frame_path:
            status='error'
            message += 'missing frame_path ; '
        
        
        #id_list = track(list_frame_contour,frame_path)
        id_list = "NOT IMPLEMENTED YET"


        if status=="error":
            return jsonify({
                'status': status, 
                'message': message
                }) 
        else :
            return jsonify({
                'status': status, 
                'id_list': id_list
                }) 
    return app