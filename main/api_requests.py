"""
Handles the requests from the discord bot to the API, to allow the database to
properly function.
"""
import requests
BASE = ""


def post_product(url, product_name, price, id):
    # Adds the product to the database
    response = requests.put(
        BASE + "product/" + str(product_name), {"id": 1, "product_name": "this_is_a_product", "url": "google.ca",  "recent_price": "$50"})
    print(response)


def get_lowest_price(product_name):
    # Gets the lowest price of the product from the database
    response = requests.get(BASE + "product/" + str(product_name))
    print(response.json())
