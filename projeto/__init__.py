from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app, resources={r"/*": {"origins": "*"}}, methods=["GET", "POST", "DELETE"])
app.config['SECRET_KEY'] = 'teste'

db = SQLAlchemy(app)

migrate = Migrate(app, db)

from projeto import routes