import spoonacular as sp
import os
from re import I
from dotenv import find_dotenv, load_dotenv
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user,logout_user,LoginManager,UserMixin,current_user
recipe_nutrients_name = []
recipe_nutrients_amount = []
recipe_nutrients_unit = []
recipe_nutrients_Dailyneeds = []



load_dotenv(find_dotenv())
app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
@app.route("/")
def find_food():
    api = sp.API(os.getenv("API_KEY"))
    food = "chicken"
    

    #find the nutrtion information using id and the amount
    response_for_nutrtition = api.search_recipes_complex(f"{food}" , addRecipeNutrition=True,number=1)
    nutrition_data = response_for_nutrtition.json()
    recipe_image =  nutrition_data ['results'][0]['image']
    recipe_id =  nutrition_data ['results'][0]['id']
    nutrients = nutrition_data['results'][0]["nutrition"]["nutrients"]
  
    for i in range(len(nutrients)):
        recipe_nutrients_name.append((nutrients[i]["name"]))
        recipe_nutrients_amount.append((nutrients[i]["amount"]))
        recipe_nutrients_unit.append((nutrients[i]["unit"]))
        recipe_nutrients_Dailyneeds.append((nutrients[i]["percentOfDailyNeeds"]))




    return (
        recipe_nutrients_name ,
        recipe_nutrients_amount,
        recipe_nutrients_unit ,
        recipe_nutrients_Dailyneeds
    )









find_food()


