from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_ge.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app, resources={r"/*": {"origins": "*"}}, methods=["GET", "POST", "DELETE"])
app.config['SECRET_KEY'] = 'teste'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'fazer_login'

migrate = Migrate(app, db)

from projeto.models import Usuario

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

from projeto import routes