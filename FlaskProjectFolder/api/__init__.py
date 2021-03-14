# FlaskProjectFolder/api/__init__.py

from flask import jsonify

# Root Route Api
from app import app


@app.route('/')
def index():
    return jsonify({"message": "Welcome to releaseskil Restfull-API"})
