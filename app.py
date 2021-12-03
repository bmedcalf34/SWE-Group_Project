# -*- coding: utf-8 -*-

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
import re

import dotenv
import os

dotenv.load_dotenv(dotenv.find_dotenv())

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://xgcammbkemszyj:a7797f19f09992f5e06e23b3f332166f4aad917f60100af1f886bc67e9da35b2@ec2-3-95-130-249.compute-1.amazonaws.com:5432/d9iffv0k9vu7d0"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "impossiblekey"
db = SQLAlchemy(app)

from models import *

api_key2 = os.environ.get("api_key")
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
    recipes = FoodRecipe.query.all()
    for recipe in recipes:
        print(recipe.instructions)
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


@app.route("/my_recipes", methods=["GET", "POST"])
@login_required
def my_recipes():
    # get recipes by user id
    food_recipes = FoodRecipe.query.filter_by(user_id=session["user"]["id"]).all()
    return render_template("my_recipes.html", food_recipes=food_recipes)


@app.route("/to_do", methods=["GET", "POST"])
@login_required
def to_do():
    food_recipes = FoodRecipe.query.filter_by(user_id=session["user"]["id"]).all()
    return render_template("to_do.html", food_recipes=food_recipes)


@app.route("/recipes", methods=["GET", "POST"])
@login_required
def recipes():
    if request.method == "POST":
        s_input = request.form.get("search")
        if (
            request.form.get("filter_by") == "Filter by"
            and request.form.get("diet") == "Diet"
        ):
            # not filtered by anything, then just do a normal search
            # get the information from the api
            response = requests.get(
                f"https://api.spoonacular.com/recipes/complexSearch?apiKey={api_key2}&query={s_input}&addRecipeNutrition=True&fillIngredients=True&instructionsRequired=True&number=9"
            ).json()
        else:
            # get the filtering option
            diet = request.form.get("diet")
            filter_option = request.form.get("filter_by")
            minVal = request.form.get("minVal")
            maxVal = request.form.get("maxVal")
            if diet == "Diet":
                # if both are given
                if minVal and maxVal:
                    response = requests.get(
                        f"https://api.spoonacular.com/recipes/complexSearch?apiKey={api_key2}&query={s_input}&addRecipeNutrition=True&min{filter_option}={minVal}&max{filter_option}={maxVal}&fillIngredients=True&instructionsRequired=True&number=9"
                    ).json()
                # if min Value is given and max value is not given
                elif minVal:
                    response = requests.get(
                        f"https://api.spoonacular.com/recipes/complexSearch?apiKey={api_key2}&query={s_input}&addRecipeNutrition=True&min{filter_option}={minVal}&fillIngredients=True&instructionsRequired=True&number=9"
                    ).json()
                # if max value is given and min value is not given
                elif maxVal:
                    response = requests.get(
                        f"https://api.spoonacular.com/recipes/complexSearch?apiKey={api_key2}&query={s_input}&addRecipeNutrition=True&max{filter_option}={maxVal}&fillIngredients=True&instructionsRequired=True&number=9"
                    ).json()
                else:
                    response = requests.get(
                        f"https://api.spoonacular.com/recipes/complexSearch?apiKey={api_key2}&query={s_input}&addRecipeNutrition=True&fillIngredients=True&instructionsRequired=True&number=9"
                    ).json()
            else:
                # if both are given
                if minVal and maxVal:
                    response = requests.get(
                        f"https://api.spoonacular.com/recipes/complexSearch?apiKey={api_key2}&query={s_input}&diet={diet}&addRecipeNutrition=True&min{filter_option}={minVal}&max{filter_option}={maxVal}&fillIngredients=True&instructionsRequired=True&number=9"
                    ).json()
                # if min Value is given and max value is not given
                elif minVal:
                    response = requests.get(
                        f"https://api.spoonacular.com/recipes/complexSearch?apiKey={api_key2}&query={s_input}&diet={diet}&addRecipeNutrition=True&min{filter_option}={minVal}&fillIngredients=True&instructionsRequired=True&number=9"
                    ).json()
                # if max value is given and min value is not given
                elif maxVal:
                    response = requests.get(
                        f"https://api.spoonacular.com/recipes/complexSearch?apiKey={api_key2}&query={s_input}&diet={diet}&addRecipeNutrition=True&max{filter_option}={maxVal}&fillIngredients=True&instructionsRequired=True&number=9"
                    ).json()
                else:
                    response = requests.get(
                        f"https://api.spoonacular.com/recipes/complexSearch?apiKey={api_key2}&query={s_input}&diet={diet}&addRecipeNutrition=True&fillIngredients=True&instructionsRequired=True&number=9"
                    ).json()
        if len(response["results"]) == 0:
            return redirect(url_for("main_page"))
        # get title, id, and imageURL
        recipes_obj = []
        for result in response["results"]:
            title = result["title"]
            image = result["image"]
            recipe_id = result["id"]
            recipe = {"title": title, "image": image, "recipe_id": recipe_id}
            recipes_obj.append(recipe)
    return render_template("recipes.html", recipes=recipes_obj, search=s_input)


@app.route("/recipe/<int:recipe_id>", methods=["GET", "POST"])
@login_required
def recipe(recipe_id):
    response = requests.get(
        f"https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={api_key2}&includeNutrition=True"
    )
    result = response.json()
    if not result["title"]:
        return redirect(url_for("main_page"))

    title = result["title"]
    recipe_id = result["id"]
    image = result["image"]
    summary = result["summary"].split("<a")
    summary = summary[0].replace("<b>", "").replace("</b>", "")
    summary_l = summary.split(".")
    summary = ""
    for i in range(6):
        summary += summary_l[i] + "."
    # get nutrients
    for nutrient in result["nutrition"]["nutrients"]:
        if nutrient["name"] == "Calories":
            calories = int(nutrient["amount"])
        elif nutrient["name"] == "Carbohydrates":
            carbs = int(nutrient["amount"])
        elif nutrient["name"] == "Fat":
            fat = int(nutrient["amount"])
        elif nutrient["name"] == "Protein":
            protein = int(nutrient["amount"])

    # get ingredients
    extIngredients = result["extendedIngredients"]
    ingredients = []
    for extIng in extIngredients:
        measures = extIng["measures"]["metric"]
        ingredient = f"{extIng['amount']} {measures['unitShort']} - {extIng['name'].capitalize()}"
        ingredients.append(ingredient)

    # get instructions
    analyzedIns = result["analyzedInstructions"]
    instructions = []
    for aIns in analyzedIns:
        steps = aIns["steps"]
        for step in steps:
            instruction = f"{str(step['number'])}. {str(step['step'])}"
            instructions.append(instruction)
    print(instructions)
    recipe_dict = {
        "title": title,
        "image": image,
        "summary": summary,
        "recipe_id": recipe_id,
        "ingredients": ingredients,
        "instructions": instructions,
        "calories": calories,
        "carbs": carbs,
        "protein": protein,
        "fat": fat,
    }
    fav = True
    food_recipes = FoodRecipe.query.filter_by(user_id=session["user"]["id"]).all()
    for recipe in food_recipes:
        if recipe.recipe_id == recipe_id:
            fav = False
            return render_template("recipe.html", recipe=recipe_dict, fav=fav)
    return render_template("recipe.html", recipe=recipe_dict, fav=fav)


@app.route(
    "/favorite/<string:title>/<path:image>/<int:recipe_id>", methods=["GET", "POST"]
)
def favorite(title, image, recipe_id):
    recipe = FoodRecipe(
        user_id=session["user"]["id"], title=title, image=image, recipe_id=recipe_id
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


@app.route(
    "/add_to_do/<string:title>/<path:image>/<int:recipe_id>", methods=["GET", "POST"]
)
def add_to_do(title, image, recipe_id):
    recipe_to_do = FoodRecipe(
        user_id=session["user"]["id"],
        title=title,
        image=image,
        recipe_id=recipe_id,
    )
    db.session.add(recipe_to_do)
    db.session.commit()
    # return to main page
    return redirect(url_for("to_do"))


@app.route("/remove_to_do/<int:recipe_id>", methods=["GET", "POST"])
def remove_to_do(recipe_id):
    # put info in databas
    recipe_to_do = FoodRecipe.query.filter_by(recipe_id=recipe_id).delete()
    db.session.commit()
    # return to main page
    return redirect(url_for("to_do"))


@app.route("/nutrition", methods=["GET", "POST"])
def nutrition():
    # return render_template("nutrition.html")
    nutrients_name = []
    nutrients_amount = []
    nutrients_unit = []
    # temp_var = SP_KEY
    # api = sp.API(temp_var)

    # default food settings

    food = "chicken"
    amount = 1

    if request.method == "POST":
        food = request.form["ingredients"]
        amount = request.form["amount"]

    # find the ingredient id
    # response = api.autocomplete_ingredient_search(f"{food}", number=1,metaInformation =True)
    response = requests.get(
        f"https://api.spoonacular.com/food/ingredients/autocomplete?apiKey={api_key2}&query={food}&number=1&metaInformation=True"
    )

    # print(response)
    data = response.json()
    print("Food type")
    # print(food)
    print(data)

    try:
        food_id = data[0]["id"]
        food_image = data[0]["image"]
    except:
        food = "chicken"
        amount = 1
        # response = api.autocomplete_ingredient_search(f"{food}", number=1,metaInformation =True)
        response = requests.get(
            f"https://api.spoonacular.com/food/ingredients/autocomplete?apiKey={api_key2}&query={food}&number=1&metaInformation=True"
        )
        data = response.json()
        food_id = data[0]["id"]
        food_image = data[0]["image"]
    if amount == "":
        amount = 1

    print(food_image)
    # find the nutrtion information using id and the amount
    # response_for_nutrtition = api.get_food_information(f"{food_id}",amount)
    response_for_nutrtition = requests.get(
        f"https://api.spoonacular.com/food/ingredients/{food_id}/information?apiKey={api_key2}&amount={amount}"
    )
    nutrition_data = response_for_nutrtition.json()
    nutrients = nutrition_data["nutrition"]["nutrients"]
    food_url = "https://spoonacular.com/cdn/ingredients_100x100/" + food_image

    # loop through and append nutrients data into
    for i in range(len(nutrients)):
        nutrients_name.append((nutrients[i]["name"]))
        nutrients_amount.append((nutrients[i]["amount"]))
        nutrients_unit.append((nutrients[i]["unit"]))

    # debug output
    print(nutrients)

    return render_template(
        "nutrition.html",
        data=data[0],
        nutrient_name=nutrients_name,
        nutrients_amount=nutrients_amount,
        nutrients_unit=nutrients_unit,
        len=len(nutrients),
        food_url=food_url,
    )


# meal planner
@app.route("/get_meal_plan", methods=["GET", "POST"])
def get_meal_plan():
    if request.method == "POST":
        return render_template("meal_plan.html")
    return render_template("get_meal_plan.html")


@app.route("/meal_plan", methods=["GET", "POST"])
def render_meal_plan():
    if request.method == "POST":
        print("We are posting here")

        timeFrame = "week"
        targetCalories = request.form.get("targetCalories")
        exclude = request.form.get("exclude")
        diet = request.form.get("diet")
        # if all search conditions are given
        if diet and exclude and targetCalories:
            response = requests.get(
                f"https://api.spoonacular.com/mealplanner/generate?apiKey={api_key2}&timeFrame={timeFrame}&targetCalories={targetCalories}&diet={diet}&exclude={exclude}"
            ).json()
        # if diet and exclude is given and target Calories is not given
        elif diet and exclude:
            response = requests.get(
                f"https://api.spoonacular.com/mealplanner/generate?apiKey={api_key2}&timeFrame={timeFrame}&diet={diet}&exclude={exclude}"
            ).json()
        # if diet and targetCalories is given and exclude is not given
        elif diet and targetCalories:
            response = requests.get(
                f"https://api.spoonacular.com/mealplanner/generate?apiKey={api_key2}&timeFrame={timeFrame}&targetCalories={targetCalories}&diet={diet}"
            ).json()
        # if exclude and targetCalories is given and diet is not given
        elif exclude and targetCalories:
            response = requests.get(
                f"https://api.spoonacular.com/mealplanner/generate?apiKey={api_key2}&timeFrame={timeFrame}&targetCalories={targetCalories}&exclude={exclude}"
            ).json()
        # if diet is given and exclude and targetCalories is not given
        elif diet:
            response = requests.get(
                f"https://api.spoonacular.com/mealplanner/generate?apiKey={api_key2}&timeFrame={timeFrame}&diet={diet}"
            ).json()
        # if exclude is given and diet and targetCalories is not given
        elif exclude:
            response = requests.get(
                f"https://api.spoonacular.com/mealplanner/generate?apiKey={api_key2}&timeFrame={timeFrame}&exclude={exclude}"
            ).json()
        # if targetCalories is given and diet and exclude is not given
        elif targetCalories:
            response = requests.get(
                f"https://api.spoonacular.com/mealplanner/generate?apiKey={api_key2}&timeFrame={timeFrame}&targetCalories={targetCalories}"
            ).json()
        else:
            # nothing is given in input
            response = requests.get(
                f"https://api.spoonacular.com/mealplanner/generate?apiKey={api_key2}&timeFrame={timeFrame}"
            ).json()

        # for meal plan week
        mealplans = []
        for week in response["week"]:
            day = week
            print(day)
            nutrient = response["week"][f"{day}"]["nutrients"]
            for meal in response["week"][f"{day}"]["meals"]:
                # get meals per day fo the week
                title = meal["title"]
                recipe_id = meal["id"]
                sourceUrl = meal["sourceUrl"]
                readyInMinutes = meal["readyInMinutes"]
                servings = meal["servings"]
                # nutrients for the three meal per day
                calories = nutrient["calories"]
                carbs = nutrient["carbohydrates"]
                fat = nutrient["fat"]
                protein = nutrient["protein"]
                mealplan = MealPlan(
                    title=title,
                    user_id=session["user"]["id"],
                    recipe_id=recipe_id,
                    calories=calories,
                    fat=fat,
                    carbs=carbs,
                    protein=protein,
                    day=day,
                    sourceUrl=sourceUrl,
                    readyInMinutes=readyInMinutes,
                    servings=servings,
                )
                mealplans.append(mealplan)
        print(mealplan.title)
        return render_template(
            "meal_plan.html", mealplans=mealplans, week=response["week"]
        )
    else:
        return render_template("meal_plan.html")


@app.route("/diet_selection")
def diet_selection():
    render_recipes = False
    return render_template("diet_selection.html", render_recipes=render_recipes)


@app.route("/diet_selection_carbs")
def diet_selection_carbs():
    render_recipes = True
    render_options = 1
    return render_template(
        "diet_selection.html",
        render_recipes=render_recipes,
        render_options=render_options,
    )


@app.route("/diet_selection_meat")
def diet_selection_meat():
    render_recipes = True
    render_options = 2
    return render_template(
        "diet_selection.html",
        render_recipes=render_recipes,
        render_options=render_options,
    )


@app.route("/diet_selection_liquid")
def diet_selection_liquid():
    render_recipes = True
    render_options = 3
    return render_template(
        "diet_selection.html",
        render_recipes=render_recipes,
        render_options=render_options,
    )


@app.route("/diet_selection_loss")
def diet_selection_loss():
    render_recipes = True
    render_options = 4
    return render_template(
        "diet_selection.html",
        render_recipes=render_recipes,
        render_options=render_options,
    )


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")


"""
allows the user to search for different meal or food options
"""


@app.route("/meals")
def meal_search():
    return render_template("meal_search.html")


if __name__ == "__main__":
    app.run()
