from tracker import app

if __name__ == "__main__":
    app.run(host=app.config["FLASK_HOST_ADDRESS"], port=app.config["FLASK_PORT"])
