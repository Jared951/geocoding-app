from flask import Flask, render_template, request, flash, session, redirect, url_for
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from model import connect_to_db, db, User, Brand, Address
from crud import create_brand, create_user, create_address, remove_brand, update_address
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
        flash("User successfully created")
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
        # Login successful
        login_user(user)
        flash("Logged in successfully")
        return redirect(url_for("home"))
    else:
        # Invalid 
        flash("Invalid email or password")
        return redirect(url_for("login"))

# Logout route
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out")
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

if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True)












"""
Add_brand.html
    Message will flash when brand is successfully added to view_all

View_all.html
    Next to each address update button that allows the user to change the address
    Button next address that uses geopy script to convert addresses into latitude/longitude csv file

1. Get Login working
2. get link to take you to add_brand.html
3. get link to take you to view_all.html
4. links between each page
5. add brands to psql
6. have brands appear on view_all.html
7. delete brands next to each


8. List to show Chalon 
9. Update functionality to satisfy requirement
10. Geocoding 
"""