import os
from dotenv import find_dotenv, load_dotenv
import spoonacular as sp
from pprint import pprint

load_dotenv(find_dotenv())
api = sp.API(os.getenv("API_KEY"))
query = input("Input an ingredient:")
number = int(input("How many recipes would you like to see?"))

response = api.autocomplete_recipe_search(query=query, number=number)
data = response.json()
for i in range(number):
    # print(data[i]["name"])
    pprint(data[i]["title"])
    pprint(data[i]["id"])
