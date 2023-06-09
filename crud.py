from model import db, User, Brand, Address
# from geocoding import geocode_address

def create_user(email, password):
    user = User(email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return user

def create_brand(brand_name, user_id):
    brand = Brand(brand_name=brand_name, user_id=user_id)
    db.session.add(brand)
    db.session.commit()
    return brand

"""
def create_address(brand_id, address_name):
    geocoordinating = geocode_address(address_name)
    latitude = geocoordinating[0]
    longitude = geocoordinating[1]
    address = Address(address_name=address_name, brand_id=brand_id, latitude=latitude, longitude=longitude)
    db.session.add(address)
    db.session.commit()
    return address
"""

def create_address(brand_id, address_name, latitude=0.0, longitude=0.0):
    address = Address(address_name=address_name, brand_id=brand_id, latitude=latitude, longitude=longitude)
    db.session.add(address)
    db.session.commit()
    return address

def remove_brand(brand_id):
    brand = Brand.query.get(brand_id)
    if brand:
        db.session.delete(brand)
        db.session.commit()
        return True
    return False

def delete_address(address_id):
    address = Address.query.get(address_id)
    if address:
        db.session.delete(address)
        db.session.commit()
        return True
    return False

def update_address(address_id, new_address):
    address = Address.query.get(address_id)
    if address:
        address.address_name = new_address
        db.session.commit()
        return True
    return False

def read_brands(user_id):
    brands = Brand.query.filter_by(user_id=user_id).all()
    return brands