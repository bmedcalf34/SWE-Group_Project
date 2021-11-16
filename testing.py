import requests
from requests import api
from pprint import pprint

api_key = ""
"""
s_input = input("What do you want to search? ")
response = requests.get(f"https://api.spoonacular.com/food/ingredients/autocomplete?apiKey={api_key}&query={s_input}&number=1&metaInformation=True").json()
print(response[0])
"""

response_for_nutrtition = requests.get(
    f"https://api.spoonacular.com/food/ingredients/9266/information?apiKey={api_key}&amount=1"
)
nutrition_data = response_for_nutrtition.json()
print(nutrition_data["nutrition"]["nutrients"])
