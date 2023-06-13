import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# Create an instance of SQLAlchemy
db = SQLAlchemy()

# User model for creating the 'users' table
class User(db.Model, UserMixin):
    # Set the table name
    __tablename__ = "users"

    # Columns in the 'users' table
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255))

    # Relationship with the 'brands' table
    brands = db.relationship("Brand", backref="user", lazy=False)

    # Constructor method for initializing the user attributes.
    def __init__ (self, email, password):
        self.email = email
        self.password = password

    # Check password
    def check_password(self, password):
        return self.password == password


# Brand model for creating the 'brands' table
class Brand(db.Model):
    # Set the table name
    __tablename__ = "brands"

    # Columns in the 'brands' table
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    brand_name = db.Column(db.String(255), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    # Relationship with the 'addresses' table
    addresses = db.relationship("Address", backref="brand", lazy=False)

    # Constructor method for initializing the brand attributes.
    def __init__(self, brand_name, user_id):
        self.brand_name = brand_name
        self.user_id = user_id


# Address model for creating the 'addresses' table
class Address(db.Model):
    # Set the table name
    __tablename__ = "addresses"

    # Columns in the 'addresses' table
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    address_name = db.Column(db.String(255))
    latitude = db.Column(db.Float())
    longitude = db.Column(db.Float())
    brand_id = db.Column(db.Integer, db.ForeignKey("brands.id"))

    # Constructor method for initializing the address attributes.
    def __init__(self, address_name, latitude, longitude, brand_id):
        self.address_name = address_name
        self.latitude = latitude
        self.longitude = longitude
        self.brand_id = brand_id


# Function to connect the app to the database
def connect_to_db(app):
    # Set the database URI from environment variable
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["POSTGRES_URI"]

    # Disable modification tracking
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Bind the SQLAlchemy instance to the app
    db.app = app # type: ignore
    db.init_app(app)


if __name__ == "__main__":
    from flask import Flask
    # Create a Flask app
    app = Flask(__name__)
    # Connect the app to the database
    connect_to_db(app)
    print("Connected to db...")