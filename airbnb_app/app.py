"""Main functions and routes for Airbnb app."""

from os import getenv
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug import secure_filename

from .wrangler import wrangle_image

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

    @app.route("/upload")
    def upload():
        return render_template("upload.html", title="Upload")

    @app.route("/upload", methods=["POST"])
    def upload_post():
        if request.method == "POST":
            img = request.files["file"]
            orig_dir = "images/original"+str(secure_filename(img.filename))
            img.save(orig_dir)
            new_dir = "images/resized/"
            wrangle_image(orig_dir, new_dir)

        return redirect(url_for("prediction"))

    @app.route("/prediction")
    def prediction(results=None):
        if results:
            message = "congrats"
        else:
            message = "No results have been calculated yet!!"

        return render_template("prediction.html", title="Prediction",
                                   message=message)

    return app
