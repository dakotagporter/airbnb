"""Configure databases for AirBnB app."""

from .app import DB


class UserInput(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    amenities = DB.Column(DB.PickleType, nullable=False)
    image = DB.Column(DB.LargeBinary, nullable=False)
