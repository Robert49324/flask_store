from flask import render_template, Blueprint, request, flash, redirect, url_for
from flask_login import current_user
from . import db
from .models import Product, User
from flask_sqlalchemy import SQLAlchemy

views = Blueprint("views",__name__)

@views.route("/", methods=['GET','POST'])
def home():
    if request.method == 'POST':
        if request.form["button"] == "Видеокарты":
            data = Product.query.filter_by(category="GPU")
            return render_template("catalog.html",products=data, user=current_user,title="Видеокарты")
        elif request.form["button"] == "Процессоры":
            data = Product.query.filter_by(category="CPU")
            return render_template("catalog.html",products=data, user=current_user,title="Процессоры")
        elif request.form["button"] == "Материнские платы":
            data = Product.query.filter_by(category="Motherboard")
            return render_template("catalog.html",products=data, user=current_user,title="Материнские платы")
        elif request.form["button"] == "Оперативная память":
            data = Product.query.filter_by(category="RAM")
            return render_template("catalog.html",products=data, user=current_user,title="Оперативная память")
        elif request.form["button"] == "Системы охлаждения":
            data = Product.query.filter_by(category="Cooling")
            return render_template("catalog.html",products=data, user=current_user,title="Системы охлаждения")
        elif request.form["button"] == "SSD":
            data = Product.query.filter_by(category="SSD")
            return render_template("catalog.html",products=data, user=current_user,title="SSD")
        elif request.form["button"] == "Жесткие диски":
            data = Product.query.filter_by(category="HDD")
            return render_template("catalog.html",products=data, user=current_user,title="Жесткие диски")
        elif request.form["button"] == "Корпуса":
            data = Product.query.filter_by(category="Frame")
            return render_template("catalog.html",products=data, user=current_user,title="Корпуса")
        elif request.form["button"] == "Блоки питания":
            data = Product.query.filter_by(category="Power")
            return render_template("catalog.html",products=data, user=current_user,title="Блоки питания")
    data = Product.query.all()
    return render_template("home.html", products=data, user=current_user)

@views.route("/catalog", methods=['GET','POST'])
def catalog():
    return render_template("catalog.html")
    
@views.route("/cart", methods=['GET','POST'])
def cart():
    return render_template("cart.html",user=current_user)

@views.route("/admin", methods=['GET','POST'])
def admin():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        category = request.form.get('category')
        price = request.form.get('price')

        user = Product.query.filter_by(name=name).first()
        
        if user:
            flash('Такой товар уже существует', category='error')
        elif len(name) < 4:
            flash("Слишком короткое название", category='error')
        elif len(description) < 2:
            flash("Слишком короткое описание", category='error')
        elif category not in ("GPU","CPU","Motherboard","RAM","Cooling","SSD","HDD","Frame","Power"):
            flash("Неверная категория", category="error")
        elif int(price) <= 0:
            flash("Слишком низкая цена", category="error")
        elif len(description) > 1000:
            flash("Слишком длинное описание", category="error")
        else:
            new_product = Product(name=name,description=description,category=category,price=price)
            db.session.add(new_product)
            db.session.commit()
            flash('Товар добавлен', category='success')
            return redirect(url_for('views.admin'))
    return render_template("admin.html",user=current_user)