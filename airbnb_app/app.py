"""Main functions and routes for Airbnb app."""

import os
from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

from .wrangler import wrangle_image

DB = SQLAlchemy()


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
        return render_template("upload.html", title="Upload")

    @app.route("/upload", methods=["POST"])
    def upload_post():
        """
        Evaluate user input to return estimate.
        """
        if request.method == "POST":
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

                filesystem_test = ''
                for file in os.scandir(app.config['UPLOAD_FOLDER']):
                    filesystem_test = filesystem_test + file.name
                return filesystem_test

                ##### TODO -- heroku has no filesystem. need to save images in database!
                # wrangle_image(orig_dir, new_dir)

        return redirect(url_for("estimate"))

    @app.route("/estimate")
    def prediction(results=None):
        if results:
            message = "congrats"
        else:
            message = "No results have been calculated yet!!"

        return render_template("estimate.html", title="Estimate",
                               message=message)

    return app
