"""Configure databases for AirBnB app."""
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate

DB = SQLAlchemy()
# MIGRATE = Migrate()


class User(DB.Model):
    email = DB.Column(DB.String(100), unique=True, nullable=False,
                      primary_key=True)
    specs = DB.relationship('Property', backref='user')


class Property(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    email_id = DB.Column(DB.String(100), DB.ForeignKey('user.email'))
    name = DB.Column(DB.String(100), nullable=False)
    amenities = DB.Column(DB.PickleType, nullable=False)
    description = DB.Column(DB.String(1000), nullable=False)
    image = DB.Column(DB.String(300), nullable=False)
