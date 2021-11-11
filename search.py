import spoonacular as sp
from pprint import pprint

api = sp.API()
# query = input("Enter ingredient:")
# # Parse an ingredient # str | The (natural language) search query. (optional)
# number = 10  # int | The maximum number of items to return (between 1 and 100). Defaults to 10. (optional) (default to 10)# bool | Whether to return more meta information about the ingredients. (optional)
# intolerances = "egg"
# api_response = api.autocomplete_ingredient_search(
#     query=query,
#     number=number,
#     intolerances=intolerances,
# )
# pprint(api_response)
# # response = api.parse_ingredients(ingredient, servings=1)
# # data = response.json()
# # print(data[0]["name"])
response = api.get_a_random_food_joke()
data = response.json()
print(data["text"])
