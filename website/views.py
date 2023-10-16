from flask import render_template, Blueprint, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from . import db
from .models import Product, Order, User, Cart
from flask_sqlalchemy import SQLAlchemy

views = Blueprint("views",__name__)

@views.route("/", methods=['GET','POST'])
def home():
    data = Product.query.all()
    cart = Cart.query.filter_by(user_id = current_user.id)
    cart_product_ids = [item.product_id for item in cart.all()]
    return render_template("home.html", products=data, user=current_user,cart=cart_product_ids)
    
@views.route("/catalog", methods=['GET','POST'])
def catalog():
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
    return render_template("catalog.html", user=current_user, title="Каталог")
    
@views.route("/product", methods=['GET','POST'])
def product():
    try:
        product_id = request.form["product"]
        product = Product.query.get(product_id)
    except KeyError:
        product = None

    return render_template("product.html", user=current_user, product=product)
    
@views.route("/search", methods=['POST','GET'])
def search():
    search = request.form.get("search")
    products = Product.query.all()
    matching_products = []
    for product in products:
        name = product.name
        if search.lower() in name.lower():
            matching_products.append(product)
    return render_template("home.html", user=current_user, products = matching_products)

@views.route("/buy", methods=['GET','POST'])
@login_required
def buy():
    product = Product.query.get(request.form["product"])
    return render_template("buy.html", user=current_user, product=product)

@views.route("/confirm", methods=['GET','POST'])
@login_required
def confirm():
    address = request.form.get('address')
    comment = request.form.get('comment')
    payment = request.form.get('payment')
    
    prod = Product.query.filter_by(id=request.form["product"]).first()
    new_order = Order(product_id = prod.id, user_id=current_user.id, address=address,comment=comment,payment=payment)
    db.session.add(new_order)
    db.session.commit()
    
    flash("Заказ оформлен!", category="success")
    return redirect(url_for("views.home"))

@views.route("/cartadd", methods=['GET','POST'])
@login_required
def cartadd():
    if request.method == 'POST':
        product_id = request.form.get("product")
        Cart.query.filter_by(product_id=product_id).delete()
        db.session.commit()
    return redirect(url_for("views.home"))

@views.route("/cartdel", methods=['GET','POST'])
@login_required
def cartdel():
    if request.method == 'POST':
        product_id = request.form.get("product")
        cart = Cart(user_id=current_user.id,product_id=product_id)
        db.session.add(cart)
        db.session.commit()
    return redirect(url_for("views.home"))

@views.route("/cart", methods=['GET','POST'])
@login_required
def cart():
    return render_template("cart.html",user=current_user)

@views.route("/admin", methods=['GET','POST'])
@login_required
def admin():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        category = request.form.get('category')
        price = request.form.get('price')
        picture = request.form.get('picture')

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
            new_product = Product(name=name,description=description,category=category,price=price, picture=picture)
            db.session.add(new_product)
            db.session.commit()
            flash('Товар добавлен', category='success')
            return redirect(url_for('views.admin'))
    orders = Order.query.all()
    return render_template("admin.html",user=current_user, orders=orders )

@views.route("/complete", methods=['GET','POST'])
def complete():
    product_id = request.form.get("order")
    order = Order.query.filter_by(id=request.form["order"]).first()
    order.status = True
    db.session.commit()
    return redirect(url_for("views.admin"))