"""Main functions and routes for Airbnb app."""

import os
from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

from .wrangler import wrangle_image, predict
from .stuff import AMENITIES
from .models import UserInput

DB = SQLAlchemy()
USERDB = SQLAlchemy()


def create_app():
    """Construct app and it's routes."""
    app = Flask(__name__)

    UPLOAD_FOLDER = "images/original/"
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    app.config["SECRET_KEY"] = 'secret-key-goes-here'
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    DB.init_app(app)

    @app.route("/")
    def root():
        return render_template("base.html", title="Home")

    @app.route("/upload")
    def upload():
        return render_template("upload.html", title="Upload",
                               amenities=AMENITIES)

    @app.route("/upload", methods=["POST"])
    def upload_post():
        """
        Evaluate user input to return estimate.
        """
        if request.method == "POST":
            amens = request.form.get("amenities")
            if not amens:
                flash("Please select at least one amenity")
                return redirect(url_for("upload"))

            img = request.files.get("file", False)
            if not img:
                flash("Please provide an image")
                return redirect(url_for("upload"))
            else:
                filename = secure_filename(img.filename)
                orig_dir = os.path.join(app.config["UPLOAD_FOLDER"],
                                        str(filename))
                img.save(orig_dir)
                new_dir = "images/resized/"
                new_name, image = wrangle_image(orig_dir, new_dir)

            new_input = UserInput(amens, path)
            os.remove(path)

            DB.session.add(new_input)
            DB.session.commit()

        return redirect(url_for("estimate"))

    @app.route("/estimate")
    def estimate(results=None):
        if results:
            amenities = UserInput.query.filter_by(id=id)
            message = f"Your amenities: {amenities}"
        else:
            message = "No results have been calculated yet!!"

        return render_template("estimate.html", title="Estimate",
                               message=message)

    return app
