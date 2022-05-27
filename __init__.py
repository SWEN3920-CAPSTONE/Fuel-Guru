import os

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .config import Config

app:Flask = Flask('config', template_folder=os.path.abspath('controller/templates'))
app.config.from_object(Config)


if Config.TESTING:
    app.testing=True
    

db:SQLAlchemy = SQLAlchemy(app)
ma:Marshmallow = Marshmallow(app)
migrate = Migrate(app, db)
#csrf = CSRFProtect(app)
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

with app.app_context():
    init_gastations()
    
if len(db.session.query(UserType).all()) == 0 and app.testing == False:
    # run seed if db is empty
    import seed
