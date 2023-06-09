import os
import model
from flask import Flask

os.system("dropdb -U jared seed-database")
os.system("createdb -U jared seed-database")

# You need a Flask app
app = Flask(__name__)

model.connect_to_db(app)

with app.app_context():
    model.db.create_all()

    new_user_1 = model.User(email="jack@example.com", password="test")
    new_user_2 = model.User(email="hankhill@example.com", password="propane")

    model.db.session.add_all([new_user_1, new_user_2])
    model.db.session.commit()
    print("Successfully added dummy users")

    new_brand = model.Brand(brand_name="vans", user_id=1)
    model.db.session.add(new_brand)
    model.db.session.commit()
    print("Successfully added dummy brand")

    new_address = model.Address(address_name="123 Spooner St.", latitude=37.889, longitude=147.999, brand_id=1)
    model.db.session.add(new_address)
    model.db.session.commit()
    print("Successfully added dummy address")

    print("Completed seed_database file")
