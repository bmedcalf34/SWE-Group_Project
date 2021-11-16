import requests
from requests import api
from pprint import pprint
api_key = "660710df9210423ab9d19d84c8cef2a3"
s_input = input("What do you want to search? ")
response = requests.get(f"https://api.spoonacular.com/recipes/complexSearch?apiKey={api_key}&query={s_input}&addRecipeNutrition=True&number=9").json()
print(response)