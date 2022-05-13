from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_mail import Mail

from .config import Config

app = Flask('config')
app.config.from_object(Config)

db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)
cors = CORS(app)
jwtm = JWTManager(app)
mail = Mail(app)

from controller.routes.admin_routes import *
from controller.routes.auth_routes import *
from controller.routes.gasstation_routes import *
from controller.routes.post_routes import *
from controller.routes.routes import *
from controller.routes.user_routes import *

db.create_all()
