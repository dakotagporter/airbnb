"""Main functions and routes for Airbnb app."""

from os import getenv
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


def create_app():
    """Construct app and it's routes."""
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    DB.init_app(app)

    @app.route("/")
    def root():
        return render_template("base.html", title="Home")

    @app.route("/prediction")
    def prediction(results=None):
        if results:
            message = "congrats"
        else:
            message = "No results have been calculated yet!!"

        return render_template("prediction.html", title="Prediction",
                                   message=message)

    return app
