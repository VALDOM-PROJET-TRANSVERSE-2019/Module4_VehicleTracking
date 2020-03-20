"""
Tracker launcher
"""
from tracker import APP

if __name__ == "__main__":
    APP.run(host=APP.config["FLASK_HOST_ADDRESS"], port=APP.config["FLASK_PORT"])
