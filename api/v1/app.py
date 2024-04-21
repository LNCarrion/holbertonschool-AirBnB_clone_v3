#!/usr/bin/python3
""" flask app that integrates with AirBnB """
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown(exc):
    """ app teardown """
    storage.close()

@app.errorhandler(Exception)
def handle_404_error(err):
    """ handles 404 error """
    return jsonify({"error": "Not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
