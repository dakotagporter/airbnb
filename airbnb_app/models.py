"""Configure databases for AirBnB app."""
from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


class UserInput(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    amenities = DB.Column(DB.PickleType, nullable=False)
    image = DB.Column(DB.LargeBinary, nullable=False)
