# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 21:10:10 2021

@author: Maryam Botrus
"""
import flask
from flask import Flask, request
import requests
from flask import render_template
import os
import time
import spoonacular as sp



if os.sys.platform == "win32":
    time.clock = time.time
else:
    _timer = time.time
from flask_sqlalchemy import SQLAlchemy

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
SP_KEY = []
try:
    DATABASE_URL = os.getenv("DATABASE_URL")
    SP_KEY = os.getenv("API_KEY")
except:
    print("Unable to Resolve Client keys")
# fixes windows specific parsing error for environment files
try:
    if DATABASE_URL == None or SP_KEY == None:
        f = open(".env", "r")
        temp = f.read()
        DATABASE_URL = temp.splitlines()[0].split(" ")[2][1:-1]
        SP_KEY = temp.splitlines()[1].split(" ")[2][1:-1]
        f.close()
except:
    print("No env file found")

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
# Gets rid of a warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


'''
Data Base Import 
'''
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<Person %r>' % self.username

@app.route("/")
def main_page():
    # serves the main page of the application
    return render_template("index.html")


@app.route("/calculator")
def food_costs():
    return render_template("calculator.html")


 #provides nutritional information on food options
 #consider building api logic in a seperate class 
@app.route("/nutrition", methods=["GET", "POST"])
def nutrition():
    #return render_template("nutrition.html")
    nutrients_name = []
    nutrients_amount = []
    nutrients_unit = []
    temp_var = SP_KEY
    api = sp.API(temp_var)
    
    food = "chicken"
    amount = 1
        
    if request.method == "POST":
        food = request.form["ingredients"]
        amount = request.form["amount"]
    
    # find the ingredient id 
    response = api.autocomplete_ingredient_search(f"{food}", number=1,metaInformation =True)
    print(response)
    data = response.json()
    print('Food type')
    print(food)
    print(data)
    try:
        food_id = data[0]["id"]
        food_image = data[0]["image"]
    except:
         food = "chicken"
         amount = 1
         response = api.autocomplete_ingredient_search(f"{food}", number=1,metaInformation =True)
         data = response.json()
         food_id = data[0]["id"]
         food_image = data[0]["image"]
    if amount == '':
        amount = 1
    #find the nutrtion information using id and the amount
    response_for_nutrtition = api.get_food_information(f"{food_id}",amount)
    nutrition_data = response_for_nutrtition.json()
    nutrients = nutrition_data['nutrition']['nutrients']


    #loop through and append nutrients data into 
    for i in range(len(nutrients)):
        nutrients_name.append((nutrients[i]['name']))
        nutrients_amount.append((nutrients[i]['amount']))
        nutrients_unit.append((nutrients[i]['unit']))

    print(nutrients)

    return render_template("nutrition.html",
                data = data[0],
                nutrient_name = nutrients_name,
                nutrients_amount = nutrients_amount,
                nutrients_unit = nutrients_unit,
                len = len(nutrients),
     )

@app.route("/recipes", methods=["GET", "POST"])
def recipes():
    print('Recipes served')
    return render_template("recipes.html")

@app.route("/diet_selection")
def diets():
    return render_template("diet_selection.html")



#allows the user to search for different meal or food options
@app.route("/meals")
def meal_search():
    return render_template("meal_search.html")

if __name__ == "__main__":
    app.run()