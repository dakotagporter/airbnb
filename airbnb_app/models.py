"""Configure databases for AirBnB app."""
from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


class User(DB.Model):
    id = DB.Column(DB.String(100), unique=True, nullable=False,
                   primary_key=True)

    def __repr__(self):
        return "<User {}>".format(self.id)


class Property(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    user_id = DB.Column(DB.String(100), DB.ForeignKey('user.id'),
                        nullable=False)
    name = DB.Column(DB.String(100), nullable=False)
    amenities = DB.Column(DB.PickleType, nullable=False)
    description = DB.Column(DB.String(1000), nullable=False)
    image = DB.Column(DB.String(300), nullable=False)
    price = DB.Column(DB.String(100), nullable=False)

    user = DB.relationship('User', backref="property")

    def __repr__(self):
        return "<Property {}>".format(self.name)
