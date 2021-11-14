# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 21:10:10 2021

@author: Maryam Botrus
"""
import flask
from flask import Flask
import requests
from flask import render_template
import os
import time



if os.sys.platform == "win32":
    time.clock = time.time
else:
    _timer = time.time
from flask_sqlalchemy import SQLAlchemy

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

try:
    DATABASE_URL = os.getenv("DATABASE_URL")
except:
    print("Unable to Resolve Client keys")
# fixes windows specific parsing error for environment files
try:
    if DATABASE_URL == None:
        f = open(".env", "r")
        temp = f.read()
        DATABASE_URL = temp.splitlines()[0].split(" ")[2][1:-1]
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
@app.route("/nutrition")
def nutrition():
    return render_template("nutrition.html")

@app.route("/recipes")
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