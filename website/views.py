from flask import jsonify, render_template, Blueprint, request, flash, redirect, url_for, session
from flask_login import login_user, login_required, logout_user, current_user
from . import db
from .models import Product, Order, User, Cart, Comment
from flask_sqlalchemy import SQLAlchemy
from loguru import logger

views = Blueprint("views",__name__)

@views.route("/", methods=['GET','POST'])
def home():
    data = Product.query.all()
    if current_user.is_authenticated:
        cart = Cart.query.filter_by(user_id = current_user.id)
        cart_product_ids = [item.product_id for item in cart.all()]
        return render_template("home.html", products=data, user=current_user,cart=cart_product_ids)
    return render_template("home.html", products=data, user=current_user)
    
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
        elif request.form["button"] == "Клавиатуры":
            data = Product.query.filter_by(category="Keyboard")
            return render_template("catalog.html", products=data, user=current_user, title="Клавиатуры")
        elif request.form["button"] == "Мыши":
            data = Product.query.filter_by(category="Mouse")
            return render_template("catalog.html", products=data, user=current_user, title="Мыши")
        elif request.form["button"] == "Мониторы":
            data = Product.query.filter_by(category="Monitor")
            return render_template("catalog.html", products=data, user=current_user, title="Мониторы")
        elif request.form["button"] == "Web-камеры":
            data = Product.query.filter_by(category="Web-Camera")
            return render_template("catalog.html", products=data, user=current_user, title="Web-камеры")
        elif request.form["button"] == "Коврики для мыши":
            data = Product.query.filter_by(category="Pad")
            return render_template("catalog.html", products=data, user=current_user, title="Коврики для мыши")
        elif request.form["button"] == "Кабели":
            data = Product.query.filter_by(category="Cabel")
            return render_template("catalog.html", products=data, user=current_user, title="Кабели")
        elif request.form["button"] == "USB-хабы":
            data = Product.query.filter_by(category="USB-HUB")
            return render_template("catalog.html", products=data, user=current_user, title="USB-хабы")
        elif request.form["button"] == "Очки виртуальной реальности":
            data = Product.query.filter_by(category="VR")
            return render_template("catalog.html", products=data, user=current_user, title="Очки виртуальной реальности")
        elif request.form["button"] == "Беспроводные точки доступа":
            data = Product.query.filter_by(category="Access point")
            return render_template("catalog.html", products=data, user=current_user, title="Беспроводные точки доступа")
        elif request.form["button"] == "Беспроводные маршрутизаторы":
            data = Product.query.filter_by(category="Router")
            return render_template("catalog.html", products=data, user=current_user, title="Беспроводные маршрутизаторы")
        elif request.form["button"] == "Коммутаторы":
            data = Product.query.filter_by(category="Switcher")
            return render_template("catalog.html", products=data, user=current_user, title="Коммутаторы")
        elif request.form["button"] == "Сетевые адаптеры":
            data = Product.query.filter_by(category="Network adapter")
            return render_template("catalog.html", products=data, user=current_user, title="Сетевые адаптеры")
        elif request.form["button"] == "Антены беспроводной связи":
            data = Product.query.filter_by(category="Wireless antenna")
            return render_template("catalog.html", products=data, user=current_user, title="Антены беспроводной связи")
        
    return render_template("catalog.html", user=current_user, title="Каталог")
    
@views.route("/product", methods=['GET','POST'])
def product():
    try:
        product_id = request.form["product"]
        product = Product.query.get(product_id)
        comments = Comment.query.filter_by(product_id = product_id)
    except KeyError:
        product = None

    return render_template("product.html", user=current_user, product=product, comments = comments)
    
@views.route("/search", methods=['POST','GET'])
def search():
    search = request.form.get("search")
    products = Product.query.all()
    matching_products = []
    cart_product_ids = None
    if current_user.is_authenticated:
        cart = Cart.query.filter_by(user_id = current_user.id)
        cart_product_ids = [item.product_id for item in cart.all()]
    for product in products:
        name = product.name
        if search.lower() in name.lower():
            matching_products.append(product)
    return render_template("home.html", user=current_user, products = matching_products, cart=cart_product_ids)

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
    referer_url = request.referrer
    if request.method == 'POST':
        product_id = request.form.get("product")
        cart = Cart(user_id=current_user.id,product_id=product_id)
        db.session.add(cart)
        db.session.commit()
        
    return redirect(referer_url)
    
@views.route("/cartdel", methods=['GET','POST'])
@login_required
def cartdel():
    referer_url = request.referrer
    if request.method == 'POST':
        product_id = request.form.get("product")
        Cart.query.filter_by(product_id=product_id).delete()
        db.session.commit()
    return redirect(referer_url)

@views.route("/cart", methods=['GET','POST'])
@login_required
def cart():
    cart = Cart.query.filter_by(user_id=current_user.id)
    return render_template("cart.html",user=current_user,cart=cart)

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
        elif category not in ("GPU","CPU","Motherboard","RAM","Cooling","SSD","HDD","Frame","Power","Keyboard","Mouse","Monitor","Web-Camera",
                                 "Pad", "Cabel", "USB-HUB", "VR", "Access point", "Router", "Switcher","Network adapter","Wireless antenna"):
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

@views.route('/submit_review', methods=['POST'])
@login_required
def submit_review():
    comment = request.form.get('comment')
    rating = request.form.get('rating')
    product_id = request.form.get('product')
    
    comment = Comment(user_name = current_user.first_name, product_id = product_id, comment = comment, rating = rating)
    
    db.session.add(comment)
    
    product = Product.query.filter_by(id=product_id).first()

    product.reviews = int(product.reviews) + 1
    product.rating = int(product.rating) + int(rating)
    
    db.session.commit()
    
    return render_template("product.html", user=current_user, product=product_id)