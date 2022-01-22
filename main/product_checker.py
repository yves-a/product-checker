'''
This is the Product Tracker. This is used to track the price and
quantity of an object
'''
import requests
import json
from datetime import datetime
import time
import random
from discord import Webhook, RequestsWebhookAdapter, Embed
from bs4 import BeautifulSoup as bs
from api_requests import post_product, get_lowest_price
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"
}

webhook_dict = {
    "1": "1",
    "2": "2"

}


def get_product(url, server):
    # Setting the id of the product
    id = url.split("_")[1].split("/")[0]

    # Getting the page information and searching for the price
    r = requests.get(url, headers=headers)
    page_info = r.text
    soup = bs(page_info, "html.parser")
    print(server)
    while True:
        try:
            product_name = soup.find(
                "div", class_="col-sm-6 product_main").h1.text
            price = soup.find(class_="price_color").text[1:]
            quantity = soup.find(class_="instock availability").text.replace(
                " ", "")[11:].replace("available)", "")
            break
        except Exception as e:
            print("Error:", e)
            return

    # Setting up the webhook, allows price checker to be used on multiple servers
    # Checks which server is requesting the price checker then sends to that webhook
    for webs in webhook_dict.keys():
        if webs == str(server):
            current_webhook = webhook_dict[webs]
            print(current_webhook)
    webhook = Webhook.from_url("https://discordapp.com/api/webhooks/" +
                               str(current_webhook), adapter=RequestsWebhookAdapter())

    print(product_name, price, quantity)
    dt_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    post_product(url, product_name, price, id)
    get_price = get_lowest_price(product_name)
    while True:
        try:
            lowest_price = get_price["lowest_price"]
            lowest_price_time = get_price["lowest_price_time"]
            break
        except Exception:
            lowest_price = price
            lowest_price_time = dt_now
            break
    embed = Embed(
    )
    embed.set_author(name="Product Checker")
    embed.add_field(name="Product Name", value=product_name, inline=True)
    embed.add_field(name="Recent Price", value=price, inline=True)
    embed.add_field(name="Recent Price Date", value=dt_now, inline=True)
    embed.add_field(name="Lowest Price", value=lowest_price, inline=True)
    embed.add_field(name="Lowest Price Date",
                    value=lowest_price_time, inline=True)
    embed.add_field(name="Is it currently the lowest price",
                    value=lowest_price == price, inline=True)
    embed.add_field(name="Quantity", value=quantity, inline=True)
    webhook.send(embed=embed)

    return
