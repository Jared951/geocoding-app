import os
# import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# assign SQLAlchemy to the variable db
db = SQLAlchemy()

# class to create users
class User(db.Model):

    # assign table name for Postgres
    __tablename__="users"

    # items in table
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

# class to create brands
class Brand(db.Model):

    # assign table name for Postgres
    __tablename__="brands"

    # items in table
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    brand_name = db.Column(db.String(255), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", nullable=False))

# class to create addresses
class Address(db.Model):

     # assign table name for Postgres
    __tablename__="addresses"

    # items in table
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    address_name = db.Column(db.String(255)) # revist
    latitude = db.Column(db.Float())
    longitude = db.Column(db.Float())
    brand_id = db.Column(db.Integer, db.ForeignKey("brands.id", nullable=False))

# connect to the db
def connect_to_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["POSTGRES_URI"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

if __name__=="__main__":
    from flask import Flask
    app = Flask(__name__)
    connect_to_db(app)
    print("Connected to db...")