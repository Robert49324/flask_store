from flask import Blueprint, render_template

auth = Blueprint('auth',__name__)

@auth.route("/sign-up", methods=['POST','GET'])
def sign_up():
    return render_template("sign_up.html")

@auth.route("/login", methods=['POST','GET'])
def login():
    return render_template("login.html")