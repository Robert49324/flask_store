from flask import render_template, Blueprint
from flask_login import current_user

views = Blueprint("views",__name__)

@views.route("/", methods=['GET','POST'])
def home():
    return render_template("home.html", user=current_user)

@views.route("/catalog", methods=['GET','POST'])
def catalog():
    return render_template("catalog.html",user=current_user)


