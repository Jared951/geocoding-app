from flask import Flask, render_template, request, flash, session, redirect

from model import connect_to_db, db

import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "secret key"
app.jinja_env.undefined = StrictUndefined

# this html home page with login and create user, once a user logins in they will be redirected to the add_brand.html page
@app.route("/")
def home():
    return render_template("home.html")

# this html page will give the option for a user to input a brand name into one string with inputs below to add addresses that are also one string. Once a user has typed all of the inputs in it will have a button that adds it to the db and users profile. Once they click the button and the information is added it will flash a message on the page that the info was successfully added
@app.route("/add_brand.html")
def add_brand():
    return render_template("add_brand.html")


@app.route("/view_all.html")
def view_all():
    return render_template("view_all.html")

if __name__=="__main__":
    app.run(debug=True)