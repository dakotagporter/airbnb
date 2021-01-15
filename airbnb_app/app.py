"""Main functions and routes for Airbnb app."""

import os
from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename

from .wrangler import wrangle_image, predict
from .stuff import AMENITIES
from .models import DB, User, Property


def create_app():
    """Construct app and it's routes."""
    app = Flask(__name__)

    UPLOAD_FOLDER = "images/original/"
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    app.config["SECRET_KEY"] = 'secret-key-goes-here'
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DATABASE_URL')
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
            email = request.form.get("email")
            if not email:
                flash("Please provide an email address")
                return redirect(url_for("upload"))

            name = request.form.get("name")
            if not name:
                flash("Please provide a name for your property")
                return redirect(url_for("upload"))

            amens = request.form.getlist("amenities")
            if not amens:
                flash("Please select at least one amenity")
                return redirect(url_for("upload"))

            desc = request.form.get("description")
            if not desc:
                flash("Please provide a description for your property")
                return redirect(url_for("upload"))

            img = request.files.get("file", False)
            if not img:
                flash("Please provide an image")
                return redirect(url_for("upload"))
            else:
                filename = secure_filename(img.filename)
                orig_dir = os.path.join(app.config["UPLOAD_FOLDER"],
                                        str(filename))
                new_dir = "images/resized/"
                img.save(orig_dir)

                path = wrangle_image(orig_dir, new_dir)

            price = predict(path, desc, amens)

            DB.create_all()
            user = (User.query.get(email)) or User(id=email)
            DB.session.add(user)

            new_input = Property(user_id=email,
                                 name=name,
                                 amenities=amens,
                                 description=desc,
                                 image=path,
                                 price=price)

            DB.session.add(new_input)

            DB.session.commit()

        return render_template("upload.html", price=price)

    @app.route("/estimate")
    def estimate():
        return render_template("estimate.html", title="Estimate")

    @app.route("/estimate", methods=["POST"])
    def estimate_post():
        email = request.form.get("search")
        user = User.query.get(email)
        property = request.form.get("property")
        if request.method == "POST" and user:
            # email = request.form.get("search")
            # property_select = request.form.get("property")
            # user = User.query.get(email)

            if user:
                properties = user.property
                if len(properties) > 1:
                    names = []
                    for property in properties:
                        names.append(property.name)
                    return render_template("estimate.html", title="Estimate",
                                           properties=names)
            else:
                flash("Email does not exist")
                return redirect(url_for("estimate"))

        if request.method == "POST" and property:
            if property:

                return render_template("estimate.html", title="Estimate", price=properties,
                               amenities="")

    return app
