import os
from dotenv import find_dotenv, load_dotenv
import spoonacular as sp
from pprint import pprint

load_dotenv(find_dotenv())
api = sp.API(os.getenv("API_KEY"))

response = api.get_a_random_food_joke()
data = response.json()
print(data["text"])
