from flask import Blueprint, render_template


contact_routes = Blueprint('contact_routes', __name__)


@contact_routes.route("/contact")
def contact():
    return render_template("contact.html", title="Contact Us")
