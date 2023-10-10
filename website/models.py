from . import db
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(150), unique = True)
    description = db.Column(db.String(1000))
    price = db.Column(db.Integer)
    category = db.Column(db.Enum("GPU","CPU","Motherboard","RAM","Cooling","SSD","HDD","Frame","Power"))
    picture = db.Column(db.String(1000))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    
class Basket():
    user_id = db.column(db.Integer)
    product_id = db.column(db.Integer)
    
class Order():
    address = db.Column(db.String(150))
    comment = db.Column(db.String(150))
    payment = db.Column(db.String(150))