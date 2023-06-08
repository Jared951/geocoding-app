from model import db, User, Brand, Address

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

def create_address(brand_id, address_name, latitude, longitude):
    address = Address(address_name=address_name, brand_id=brand_id, latitude=0, longitude=0)
    db.session.add(address)
    db.session.commit()
    return address

def delete_brand(brand_id):
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

def update_address(address_id, address_name):
    address = Address.query.get(address_id)
    if address:
        address.address_name = address_name
        db.session.commit()
        return True
    return False

def read_brands(user_id):
    brands = Brand.query.filter_by(user_id=user_id).all()
    return brands