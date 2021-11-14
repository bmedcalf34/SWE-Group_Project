# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 21:10:10 2021

@author: Maryam Botrus
"""
import flask
from flask import Flask
import requests
from flask import render_template
import spoonacular as sp
import os
from dotenv import find_dotenv, load_dotenv
from flask_login import login_user, current_user, LoginManager
from flask_login.utils import login_required
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)


db_url = os.getenv("DATABASE_URL")
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
# Gets rid of a warning
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = b"I am a secret key!"  # don't defraud my app ok?

db = SQLAlchemy(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __repr__(self):
        return f"<User {self.username}>"

    def get_username(self):
        return self.username



login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_name):
    return User.query.get(user_name)

@app.route("/")
def main_page():
    # serves the main page of the application
    return render_template("index.html")


"""
tabulates food costs
"""


@app.route("/calculator")
def food_costs():
    return render_template("calculator.html")


"""
 provides nutritional information on food options
 consider building api logic in a seperate class 
"""


@app.route("/nutrition")
def nutrition():
    load_dotenv(find_dotenv())
    # nutrition of food
    nutrients_name = []
    nutrients_amount = []
    nutrients_unit = []
    api = sp.API(os.getenv("API_KEY"))
    food = "chicken"
    # find the ingredient id
    response = api.autocomplete_ingredient_search(
        f"{food}", number=1, metaInformation=True
    )
    data = response.json()

    food_id = data[0]["id"]
    # find the nutrtion information using id and the amount
    response_for_nutrtition = api.get_food_information(f"{food_id}", amount=1)
    nutrition_data = response_for_nutrtition.json()
    nutrients = nutrition_data["nutrition"]["nutrients"]

    # loop through and append nutrients data into
    for i in range(len(nutrients)):
        nutrients_name.append((nutrients[i]["name"]))
        nutrients_amount.append((nutrients[i]["amount"]))
        nutrients_unit.append((nutrients[i]["unit"]))

    return render_template(
        "nutrition.html",
        data=data[0],
        nutrient_name=nutrients_name,
        nutrients_amount=nutrients_amount,
        nutrients_unit=nutrients_unit,
        len=len(nutrients),
    )


@app.route("/recipes")
def recipes():
    return render_template("recipes.html")


@app.route("/diet_selection")
def diets():
    return render_template("diet_selection.html")


@app.route("/signup")
def signup():
    return flask.render_template("signup.html")


@app.route("/signup", methods=["POST"])
def signup_post():
    username = flask.request.form.get("username")
    password = flask.request.form.get("password")
    user = User.query.filter_by(username=username).first()
    if user:
        pass
    else:
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

    return flask.redirect(flask.url_for("index"))


@app.route("/login")
def login():
    return flask.render_template("login.html")


@app.route("/login", methods=["POST"])
def login_post():
    username = flask.request.form.get("username")
    password = flask.request.form.get("password")
    user = User.query.filter_by(username=username).first()
    Database_password = user.password
    if password == Database_password:
        login_user(user)
        return flask.redirect(flask.url_for("bp.nutrition"))

    else:
        return flask.jsonify({"status": 401, "reason": "Username or Password Error"})

"""
allows the user to search for different meal or food options
"""


@app.route("/meals")
def meal_search():
    return render_template("meal_search.html")


if __name__ == "__main__":
    app.run()
