import discord
from dotenv import dotenv_values
import logging
import os


def main():
    # load config
    config = dotenv_values(".env")

    # initalize logger
    if not os.path.exists("logs"):
        os.mkdir("logs")
    handler = logging.FileHandler(
        filename=os.path.join(os.getcwd(), "logs", "discord.log"), encoding="utf-8", mode="w"
    )

    # initialize bot
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    # runs when bot is started
    @client.event
    async def on_ready():
        print(f"We have logged in as {client.user}")

    # runs when message is sent to server
    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if message.content.startswith("$hello"):
            await message.channel.send("Hello!")

    # run bot
    client.run(config.get("BOT_TOKEN"))


if __name__ == "__main__":
    main()
