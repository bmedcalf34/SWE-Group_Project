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

app = Flask(__name__)

@app.route("/")
def main_page():
    # serves the main page of the application
    return render_template("index.html")

'''
tabulates food costs
'''
@app.route("/calculator")
def food_costs():
    return render_template("calculator.html")



'''
 provides nutritional information on food options
 consider building api logic in a seperate class 
'''
@app.route("/nutrition")
def nutrition():
    nutrients_name = []
    nutrients_amount = []
    nutrients_unit = []
    api = sp.API("b702fb3e3d514cab9fb4bc3bf380905b")
    food = "chicken"
    # find the ingredient id 
    response = api.autocomplete_ingredient_search(f"{food}", number=1,metaInformation =True)
    data = response.json()
    
    food_id = data[0]["id"]
    food_image = data[0]["image"]
    #find the nutrtion information using id and the amount
    response_for_nutrtition = api.get_food_information(f"{food_id}",amount =1)
    nutrition_data = response_for_nutrtition.json()
    nutrients = nutrition_data['nutrition']['nutrients']
    
    
    #loop through and append nutrients data into 
    for i in range(len(nutrients)):
        nutrients_name.append((nutrients[i]['name']))
        nutrients_amount.append((nutrients[i]['amount']))
        nutrients_unit.append((nutrients[i]['unit']))



    return render_template("nutrition.html",
                data = data[0],
                nutrient_name = nutrients_name,
                nutrients_amount = nutrients_amount,
                nutrients_unit = nutrients_unit,
                len = len(nutrients),
     )

    

@app.route("/recipes")
def recipes():
    return render_template("recipes.html")

@app.route("/diet_selection")
def diets():
    return render_template("diet_selection.html")


'''
allows the user to search for different meal or food options
'''
@app.route("/meals")
def meal_search():
    return render_template("meal_search.html")

if __name__ == "__main__":
    app.run()