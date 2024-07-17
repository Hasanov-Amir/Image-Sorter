from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrator = Migrate(db=db)
api = Api()
ma = Marshmallow()
