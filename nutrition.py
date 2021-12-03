from flask import Flask, request
from flask import render_template
import spoonacular as sp
from dotenv import find_dotenv, load_dotenv
import os

load_dotenv(find_dotenv())
try:
    SP_KEY = os.getenv("API_KEY")
except:
    print("Unable to Resolve Client keys")


def nutrition(food):
    # return render_template("nutrition.html")
    nutrients_name = []
    nutrients_amount = []
    nutrients_unit = []
    api = sp.API(os.getenv("API_KEY"))

    food = "chicken"
    amount = 1

    # find the ingredient id
    response = api.autocomplete_ingredient_search(
        f"{food}", number=1, metaInformation=True
    )
    print(response)
    data = response.json()
    print("Food type")
    print(food)
    print(data)
    try:
        food_id = data[0]["id"]
        food_image = data[0]["image"]
    except:
        food = "chicken"
        amount = 1
        response = api.autocomplete_ingredient_search(
            f"{food}", number=1, metaInformation=True
        )
        data = response.json()
        food_id = data[0]["id"]

    if amount == "":
        amount = 1
    # find the nutrtion information using id and the amount
    response_for_nutrtition = api.get_food_information(f"{food_id}", amount)
    nutrition_data = response_for_nutrtition.json()
    nutrients = nutrition_data["nutrition"]["nutrients"]

    print(food_image)
    # loop through and append nutrients data into
    for i in range(len(nutrients)):
        nutrients_name.append((nutrients[i]["name"]))
        nutrients_amount.append((nutrients[i]["amount"]))
        nutrients_unit.append((nutrients[i]["unit"]))

    return (
        nutrients_name,
        nutrients_amount,
        nutrients_unit,
        data[0],
    )


nutrition()
