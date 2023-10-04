from flask import render_template, Blueprint, request, flash, redirect, url_for
from flask_login import current_user
from . import db
from .models import Product, User
from flask_sqlalchemy import SQLAlchemy

views = Blueprint("views",__name__)

@views.route("/", methods=['GET','POST'])
def home():
    data = Product.query.all()
    return render_template("home.html", products=data, user=current_user)

@views.route("/catalog", methods=['GET','POST'])
def catalog():
    return render_template("catalog.html",user=current_user)

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