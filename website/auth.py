from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import  generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from loguru import logger

auth = Blueprint('auth',__name__)

@auth.route("/sign-up", methods=['POST','GET'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        user = User.query.filter_by(email=email).first()
        
        if user:
            flash('Такой пользователь уже существует', category='error')
        elif len(email) < 4:
            flash("Адрес электронной почты слишком короткий", category='error')
        elif len(firstName) < 2:
            flash("Имя слишком короткое", category='error')
        elif password1!=password2:
            flash("Пароли не совпадают", category='error')
        elif len(password1) < 5:
            flash("Пароль должен быть длинее 5 символов", category='error')
        else:
            new_user = User(email=email,first_name=firstName,password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Аккаунт создан', category='success')
            return redirect(url_for('views.home'))
    return render_template("sign_up.html",user=current_user)

@auth.route("/login", methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email =  request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash("Вы вошли", category = "success")
                return redirect(url_for("views.home"))
            else:
                flash("Неверный пароль", category="error")
        else:
            flash("Такого пользователя не существует", category="error")
        
    return render_template("login.html",user=current_user)

@auth.route("/logout", methods=['POST','GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))