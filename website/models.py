from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(150), unique = True)
    description = db.Column(db.String(1000))
    category = db.Column(db.enum("GPU","CPU","Motherboard","RAM","Cooling","SSD","HDD","Frame","Power"))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    
class Basket():
    user_id = db.column(db.Integer)
    product_id = db.column(db.Integer)