import flask
from flask import Flask
from jinja2.utils import F
import requests
from flask import render_template, redirect, url_for, session, request, flash
from werkzeug.wrappers import response
from forms import LoginForm, SignUpForm
from flask_login import (
    login_user,
    LoginManager,
    login_required,
    logout_user,
    current_user,
)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import requests

import dotenv
import os

dotenv.load_dotenv(dotenv.find_dotenv())

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://tkcnzovilkzgtf:4d1dcec2326c9a42213301e189a72612ef59074fe67b30de25149d423330b7ef@ec2-34-198-189-252.compute-1.amazonaws.com:5432/df3psrklb8o3jp"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "impossiblekey"
db = SQLAlchemy(app)
from models import *

api_key = os.environ.get("api_key")
api_key2 = os.environ.get("api_key2")


# set up flask login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
@login_required
def main_page():
    # serves the main page of the application
    return render_template("index.html", user=session["user"])


@app.route("/testing")
def testing():
    users = User.query.all()
    for user in users:
        print(user.username)
    return "Worked"


# Login Page
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Query the username of the user
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                session["user"] = {"username": user.username, "id": user.id}
                return redirect(url_for("main_page"))
            else:
                flash("Password was wrong")
                return redirect(url_for("login"))
        else:
            flash("Username was wrong")
            return redirect(url_for("login"))
    return render_template("login.html", form=form)


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


# Sign Up Page
@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        # check if username is valid
        existing_username = User.query.filter_by(username=form.username.data).first()
        if existing_username is None:
            hashed_password = generate_password_hash(form.password.data)
            # create new user
            user = User(form.username.data, hashed_password)
            # add it to session of db
            db.session.add(user)
            # commit the change
            db.session.commit()
            return redirect(url_for("login"))
        else:
            flash("Username is not available")
            return redirect(url_for("sign_up"))
    return render_template("sign_up.html", form=form)


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
    return render_template("nutrition.html")


@app.route("/my_recipes", methods=["GET", "POST"])
@login_required
def my_recipes():
    # get recipes by user id
    food_recipes = FoodRecipe.query.filter_by(user_id=session["user"]["id"]).all()
    return render_template("my_recipes.html", food_recipes=food_recipes)


@app.route("/recipes", methods=["GET", "POST"])
@login_required
def recipes():
    if request.method == "POST":
        s_input = request.form.get("search")
        if request.form.get("filter_by") == "Filter by":
            # not filtered by anything, then just do a normal search
            # get the information from the api
            response = requests.get(
                f"https://api.spoonacular.com/recipes/complexSearch?apiKey={api_key2}&query={s_input}&addRecipeNutrition=True&number=9"
            ).json()
        else:
            # get the filtering option
            filter_option = request.form.get("filter_by")
            minVal = request.form.get("minVal")
            maxVal = request.form.get("maxVal")
            response = requests.get(
                f"https://api.spoonacular.com/recipes/complexSearch?apiKey={api_key2}&query={s_input}&addRecipeNutrition=True&min{filter_option}={minVal}&max{filter_option}={maxVal}&number=9"
            ).json()

        if len(response["results"]) == 0:
            return redirect(url_for("main_page"))
        # get title, id, and imageURL
        recipes = []
        for result in response["results"]:
            title = result["title"]
            recipe_id = result["id"]
            image = result["image"]
            for nutrient in result["nutrition"]["nutrients"]:
                if nutrient["name"] == "Calories":
                    calories = int(nutrient["amount"])
                elif nutrient["name"] == "Carbohydrates":
                    carbs = int(nutrient["amount"])
                elif nutrient["name"] == "Fat":
                    fat = int(nutrient["amount"])
                elif nutrient["name"] == "Protein":
                    protein = int(nutrient["amount"])
            recipe = FoodRecipe(
                title=title,
                user_id=session["user"]["id"],
                recipe_id=recipe_id,
                image=image,
                calories=calories,
                fat=fat,
                carbs=carbs,
                protein=protein,
            )
            recipes.append(recipe)
    return render_template("recipes.html", recipes=recipes, search=s_input)


@app.route(
    "/recipe/<string:title>/<path:image>/<int:calories>/<int:carbs>/<int:fat>/<int:protein>/<int:recipe_id>/<string:user_id>",
    methods=["GET", "POST"],
)
@login_required
def recipe(title, image, calories, carbs, fat, protein, recipe_id, user_id):
    recipe_object = {
        "title": title,
        "image": image,
        "calories": calories,
        "carbs": carbs,
        "fat": fat,
        "protein": protein,
        "recipe_id": recipe_id,
        "user_id": user_id,
    }
    # check if the recipe is on the database
    fav = True
    food_recipes = FoodRecipe.query.filter_by(user_id=session["user"]["id"]).all()
    for recipe in food_recipes:
        if recipe.title == title:
            fav = False
            return render_template("recipe.html", recipe_object=recipe_object, fav=fav)
    return render_template("recipe.html", recipe_object=recipe_object, fav=fav)


@app.route(
    "/favorite/<string:title>/<path:image>/<int:calories>/<int:carbs>/<int:fat>/<int:protein>/<int:recipe_id>/<int:user_id>",
    methods=["GET", "POST"],
)
def favorite(title, image, calories, carbs, fat, protein, recipe_id, user_id):
    # put info in databas
    recipe = FoodRecipe(
        title=title,
        image=image,
        calories=calories,
        carbs=carbs,
        fat=fat,
        protein=protein,
        recipe_id=recipe_id,
        user_id=user_id,
    )
    db.session.add(recipe)
    db.session.commit()
    # return to main page
    return redirect(url_for("my_recipes"))


@app.route("/unfavorite/<int:recipe_id>", methods=["GET", "POST"])
def unfavorite(recipe_id):
    # put info in databas
    recipe = FoodRecipe.query.filter_by(recipe_id=recipe_id).delete()
    db.session.commit()
    # return to main page
    return redirect(url_for("my_recipes"))


@app.route("/diet_selection")
def diets():
    return render_template("diet_selection.html")


"""
allows the user to search for different meal or food options
"""


@app.route("/meals")
def meal_search():
    return render_template("meal_search.html")


if __name__ == "__main__":
    app.run()
