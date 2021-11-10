# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 21:10:10 2021

@author: Maryam Botrus
"""
import flask
from flask import Flask
import requests
from flask import render_template


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
    return render_template("nutrition.html")

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