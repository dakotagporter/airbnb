"""Configure databases for AirBnB app."""
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate

DB = SQLAlchemy()
# MIGRATE = Migrate()


class UserInput(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(100))
    amenities = DB.Column(DB.PickleType, nullable=False)
    description = DB.Column(DB.String(1000))
    image = DB.Column(DB.String(300), nullable=False)
