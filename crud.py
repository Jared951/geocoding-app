from model import db, User, Brand, Address
from geocoding import geocode_address

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


def create_address(brand_id, address_name, latitude=0.0, longitude=0.0):
    address = Address(address_name=address_name, brand_id=brand_id, latitude=latitude, longitude=longitude)
    db.session.add(address)
    db.session.commit()
    return address

def remove_brand(brand_id):
    brand = Brand.query.get(brand_id)
    if brand:
        # Delete the addresses associated with the brand
        Address.query.filter_by(brand_id=brand_id).delete()
        
        # Delete the brand itself
        db.session.delete(brand)
        db.session.commit()
        return True
    return False

def create_geocode(brand_id, address_name):
    geocoordinating = geocode_address(address_name)
    latitude = geocoordinating[0] 
    longitude = geocoordinating[1] 

    address = Address(address_name=address_name, brand_id=brand_id, latitude=latitude, longitude=longitude)
    db.session.add(address)
    db.session.commit()
    return address