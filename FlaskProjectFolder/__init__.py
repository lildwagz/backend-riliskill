# FlaskProjectFolder/__init__.py
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = "\x7f\x083\x88[\xe1\x13vM\nc\xec\xee\xad\xe8\x81o\x8a|\xc03\x96\xc1\x9b"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/db_courses'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False
db = SQLAlchemy(app)
from FlaskProjectFolder.api.auth.controller import auth_blueprint

app.register_blueprint(auth_blueprint)





