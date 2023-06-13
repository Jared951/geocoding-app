import csv
import io
from flask import Flask, render_template, request, flash, redirect, url_for, make_response
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from model import connect_to_db, db, User, Brand, Address
from crud import create_brand, create_user, create_address, remove_brand
from geocoding import geocode_address
from jinja2 import StrictUndefined


app = Flask(__name__)
app.secret_key = "secret key"
app.jinja_env.undefined = StrictUndefined

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Home page
@app.route("/")
def home():
    return render_template("home.html")

# Route for user registration
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = create_user(email, password)
        return redirect(url_for("home"))
    else:
        return render_template("home")

# Login page
@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    user = User.query.filter_by(email=email).first()

    if user and user.password == password:
        login_user(user)
        return redirect(url_for("home"))
    else:
        return redirect(url_for("login"))

# Logout route
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

# Route for adding a brand
@app.route("/add_brand")
@login_required  
def add_brand():
    return render_template("add_brand.html")

# Route for viewing all brands 
@app.route('/view_all')
@login_required
def view_all():
    user = current_user
    user_brands = Brand.query.filter_by(user_id=user.id).all()

    for brand in user_brands:
        brand.addresses = Address.query.filter_by(brand_id=brand.id).all()

    return render_template("view_all.html", brands=user_brands)
 
# Route for creating brand and addresses
@app.route("/add_brand", methods=["GET", "POST"])
@login_required
def add_brand_and_addresses():
    if request.method == "POST":
        brand_name = request.form.get("brand_name")
        addresses = request.form.getlist("address")

        user_id = current_user.id
        brand = create_brand(brand_name=brand_name, user_id=user_id)

        for address in addresses:
            create_address(brand_id=brand.id, address_name=address)

        flash("Brand added successfully!")
    return render_template("add_brand.html")

# Route to delete brand
@app.route("/delete_brand/<int:brand_id>", methods=["POST"])
@login_required
def delete_brand(brand_id):
    if remove_brand(brand_id):
        flash("Brand deleted successfully!")
    else:
        flash("Brand not found.")

    return redirect(url_for("view_all"))

# Route to download geocoordinates
@app.route("/download_geocoordinates/<int:brand_id>", methods=["GET"])
@login_required
def download_geocoordinates(brand_id):
    brand = Brand.query.get(brand_id)
    if brand:
        addresses = Address.query.filter_by(brand_id=brand.id).all()
        geocoordinates = []
        for address in addresses:
            coordinates = geocode_address(address.address_name)
            if coordinates:
                address.latitude = coordinates[0]
                address.longitude = coordinates[1]
                geocoordinates.append(coordinates)

        db.session.commit()

        # Create a CSV file
        csv_data = [["Latitude", "Longitude"]] + geocoordinates
        csv_file = "geocoordinates.csv"

        # Prepare the CSV file for download
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerows(csv_data)

        response = make_response(output.getvalue())
        response.headers["Content-Disposition"] = f"attachment; filename={csv_file}"
        response.headers["Content-Type"] = "text/csv"

        return response
    else:
        flash("Brand not found.")

    return redirect(url_for("view_all"))

# Route to geocode addresses
@app.route("/geocode_addresses/<int:brand_id>", methods=["POST"])
@login_required
def geocode_addresses(brand_id):
    brand = Brand.query.get(brand_id)
    if brand:
        addresses = Address.query.filter_by(brand_id=brand.id).all()
        for address in addresses:
            geocoordinates = geocode_address(address.address_name)
            if geocoordinates:
                address.latitude = geocoordinates[0]
                address.longitude = geocoordinates[1]
                db.session.commit()
        flash("Addresses geocoded successfully!")
    else:
        flash("Please Retry")

    return redirect(url_for("download_geocoordinates", brand_id=brand_id))

if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True)