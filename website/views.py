from flask import render_template, Blueprint

views = Blueprint("views",__name__)

@views.route("/", methods=['GET','POST'])
def home():
    return render_template("home.html")



