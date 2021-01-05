"""Main functions and routes for Airbnb app."""

import os
from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

from .wrangler import wrangle_image

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
        AMENITIES = ['Wifi',
                     'Smoke alarm',
                     'Essentials',
                     'Heating',
                     'Air conditioning',
                     'Kitchen',
                     'Hangers',
                     'TV',
                     'Iron',
                     'Washer',
                     'Dryer',
                     'Shampoo',
                     'Carbon monoxide alarm',
                     'Hair dryer',
                     'Laptop-friendly workspace',
                     'Hot water',
                     'Fire extinguisher',
                     'Refrigerator',
                     'Microwave',
                     'Dishes and silverware',
                     'Coffee maker',
                     'Private entrance',
                     'Oven',
                     'Stove',
                     'Bed linens',
                     'Cooking basics',
                     'First aid kit',
                     'Free street parking',
                     'Dishwasher',
                     'Extra pillows and blankets',
                     'Long term stays allowed',
                     'Cable TV',
                     'Free parking on premises',
                     'Patio or balcony',
                     'Luggage dropoff allowed',
                     'Lockbox',
                     'Garden or backyard',
                     'Keypad',
                     'Elevator',
                     'Gym',
                     'Lock on bedroom door',
                     'Bathtub',
                     'BBQ grill',
                     'Indoor fireplace',
                     'Breakfast',
                     'Shower gel',
                     'Paid parking on premises',
                     'Paid parking off premises',
                     'Pool',
                     'Pack \'n Play/travel crib']

        return render_template("upload.html", title="Upload"
                               amenities=AMENITIES)

    @app.route("/upload", methods=["POST"])
    def upload_post():
        """
        Evaluate user input to return estimate.
        """
        if request.method == "POST":
            amens = request.form["amenities"]

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

                wrangle_image(orig_dir, new_dir)

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
