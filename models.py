from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password


class FoodRecipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    title = db.Column(db.String(220), nullable=False)
    image = db.Column(db.String(200), nullable=False)
    recipe_id = db.Column(db.Integer)

    def __init__(self, user_id, title, image, recipe_id) -> None:
        # constructor for recipe
        self.user_id = user_id
        self.title = title
        self.image = image
        self.recipe_id = recipe_id

class MealPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    recipe_id = db.Column(db.Integer)
    title = db.Column(db.String(220), nullable=False)
    calories = db.Column(db.Integer)
    carbs = db.Column(db.String(20), nullable=False)
    fat = db.Column(db.String(20), nullable=False)
    protein = db.Column(db.String(20), nullable=False)
    day = db.Column(db.String(20), nullable=False)
    sourceUrl = db.Column(db.String(20), nullable=False)
    readyInMinutes = db.Column(db.Integer)
    servings = db.Column(db.Integer)

    def __init__(self,
        user_id,
        recipe_id,
        title,
        calories,
        fat,
        carbs,
        protein,
        day,
        sourceUrl,
        readyInMinutes,
        servings,
    ) -> None:
        # constructor for recipe
        self.user_id = user_id
        self.recipe_id = recipe_id
        self.title = title
        self.calories = calories
        self.fat = fat
        self.carbs = carbs
        self.protein = protein
        self.day = day
        self.sourceUrl = sourceUrl
        self.readyInMinutes = readyInMinutes
        self.servings = servings
    