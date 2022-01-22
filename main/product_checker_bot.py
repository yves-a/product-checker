import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from product_checker import get_product
import threading
from datetime import datetime
client = discord.Client()


# Shows that the bot is ready
@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
@has_permissions(administrator=True)
# Different Commands for the Bot
async def on_message(message):
    if message.author == client:
        return
    server_id = message.guild.id
    msg = message.content
    dt_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # Simple hello message
    if message.content.startswith("$hello"):
        await message.channel.send('Hello!')

    # Starts checking for the product with the given url
    if message.content.startswith("$url"):
        url = msg.split("$url ", 1)[1]

        product_name = url.split("/")[4].replace("-", "").title()
        print(server_id)
        print(id, product_name)
        await message.channel.send("Now  searching for product: " + url)
        product_monitor = threading.Thread(
            target=get_product, args=(url, server_id))
        product_monitor.start()

# TOKEN ADDED HERE
client.run("TOKEN")
