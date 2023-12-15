from flask import Blueprint, render_template, flash, redirect, current_app, url_for, session, request #, jsonify

from web_app.routes.wrappers import authenticated_route

about_routes = Blueprint("about_routes", __name__)

@about_routes.route("/about")
def about():
    return render_template('about.html')


