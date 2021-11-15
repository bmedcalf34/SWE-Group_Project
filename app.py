import flask
from flask import Flask, request
from flask import render_template
import spoonacular as sp
import os
from dotenv import find_dotenv, load_dotenv
from flask_login import login_user, current_user, LoginManager
from flask_login.utils import login_required
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
import time
from nutrition import nutrition
load_dotenv(find_dotenv())
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
class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"

    def get_username(self):
        return self.username

db.create_all()
db.session.commit()

@app.route("/")
def main_page():
    # serves the main page of the application
    return render_template("index.html",login_name="empty_user",login_status=False)


@app.route("/calculator")
def food_costs():
    return render_template("calculator.html")


 #provides nutritional information on food options
 #consider building api logic in a seperate class 
@app.route("/nutrition", methods=["GET", "POST"])
def nutrition():
   
    
    
    food = "chicken"
    amount = 1
        
    if request.method == "POST":
        food = request.form["ingredients"]
        amount = request.form["amount"]
    

    
    datas = nutrition(food)

    return render_template("nutrition.html",
                data = datas["data[0]"],
                nutrient_name = datas["nutrient_name"],
                nutrients_amount = datas["nutrient_amount"],
                nutrients_unit = datas["nutrient_unit"],
                len = len(datas["nutrient_amount"]),
                
     )

@app.route("/recipes", methods=["GET", "POST"])
def recipes():
    print('Recipes served')
    return render_template("recipes.html")

@app.route("/diet_selection")
def diets():
    return render_template("diet_selection.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/signup", methods=["POST"])
def signup_post():
    
    
    if request.method == "POST":
        username = flask.request.form.get("username")
        password = flask.request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user:
            pass
        else:
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()

    return render_template("index.html",login_name=user.username,login_status=True)


@app.route("/login")
def login():
    return flask.render_template("login.html")


@app.route("/login", methods=["POST"])
def login_post():
    username = flask.request.form.get("username")
    print(username)
    password = flask.request.form.get("password")
    print(password)
    users = User.query.filter_by(username=username).all()
    condition = False
    for user in users:
        print(user.username)
        print(user.password)
        if(user.password==password):
            condition=True
    print(condition)
    if condition:
        return render_template("index.html",login_name=user.username,login_status=True)
    else:
        return flask.jsonify({"status": 401, "reason": "Username or Password Error"})


#allows the user to search for different meal or food options
@app.route("/meals")
def meal_search():
    return render_template("meal_search.html")



'''
App Sign Up Code 
'''

if __name__ == "__main__":
    app.run()