# FlaskProjectFolder/api/__init__.py

from flask import jsonify, make_response

# Root Route Api
from app import app


@app.route('/')
def index():
    data = {
        "list of available endpoints": [

            {
                "login":
                    {"function": "to login your releaseskill account",
                    "endpoint": "/auth/login",
                    "method": "['GET','POST']",
                    "usage": "use basic auth such as username and password",
                    "payload" : "no"}

            },
            {
                "register":{
                    "function": "to create a new releaseskill account",
                    "endpoint": "/auth/register",
                    "method": "['POST']",
                    "usage": "make sure you post the json payload with these keys (username,password,name,email,gender,"
                             "phone_number)",
                    "payload" : "yes"
                }
            }

        ]
    }
    return jsonify({"message": "Welcome to releaseskil Restfull-API",
                    "services": data})
