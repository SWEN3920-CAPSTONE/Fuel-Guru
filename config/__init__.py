from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_wtf import CSRFProtect
from flask_migrate import Migrate

from .config import Config

app = Flask('FuelGuru')
app.config.from_object(Config)

db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)


# these imports will likely be replaced by routes

from model.gasstation import *
from model.posts import *
from model.users import *

db.create_all()