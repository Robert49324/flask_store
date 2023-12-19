from . import db
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(150), unique = True)
    description = db.Column(db.String(1000))
    price = db.Column(db.Integer)
    category = db.Column(db.Enum("GPU","CPU","Motherboard","RAM","Cooling","SSD","HDD","Frame","Power","Keyboard","Mouse","Monitor","Web-Camera",
                                 "Pad", "Cabel", "USB-HUB", "VR", "Access point", "Router", "Switcher","Network adapter","Wireless antenna"))
    picture = db.Column(db.String(1000))
    rating = db.Column(db.Integer, default=0)
    reviews = db.Column(db.Integer, default=0)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer,db.ForeignKey('product.id'))
    product = db.relationship('Product')
    
class Order(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    product_id = db.Column(db.Integer,db.ForeignKey('product.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    status = db.Column(db.Boolean, default=False)
    address = db.Column(db.String(150))
    comment = db.Column(db.String(150))
    payment = db.Column(db.String(150))
    
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    product_id = db.Column(db.Integer,db.ForeignKey('product.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    comment = db.Column(db.String(4000))
    rating = db.Column(db.Integer, default=0)