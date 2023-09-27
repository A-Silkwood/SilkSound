import discord
import discord.http
from discord.ext import commands
import logging
import logging.handlers

import asyncio
from dotenv import dotenv_values
import os

import utils as u


def _debug(message):
    u.logger.debug(f": {message}")


def _info(message):
    u.logger.info(f": {message}")


def _warning(message):
    u.logger.warning(f": {message}")


def _error(message):
    u.logger.error(f": {message}")


def _critical(message):
    u.logger.critical(f": {message}")


# startup bot
def main():
    u.init_logger()

    # check for directory
    if not os.path.exists("logs"):
        os.mkdir("logs")

    # initialize discord.py logger
    disc_handler = logging.handlers.RotatingFileHandler(
        filename=os.path.join(os.getcwd(), "logs", "discord.log"),
        encoding="utf-8",
        maxBytes=32 * 1024 * 1024,  # 32 MiB
        backupCount=5,  # Rotate through 5 files
    )
    dt_fmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(
        "[{asctime}] [{levelname:<8}] {name}: {message}", dt_fmt, style="{"
    )
    disc_handler.setFormatter(formatter)
    disc_logger = logging.getLogger("discord")
    disc_logger.setLevel(
        logging.DEBUG if u.config.get("ENV") == "dev" else logging.INFO
    )
    disc_logger.addHandler(disc_handler)

    # initialize bot
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="!", intents=intents)

    # runs when bot is intialized
    @bot.event
    async def on_ready():
        _info(f"We have logged in as {bot.user}")

    # load cogs
    _info(f"Loading extensions")
    for filename in os.listdir(os.path.join(os.getcwd(), "cogs")):
        if filename.endswith(".py"):
            asyncio.run(bot.load_extension(f"cogs.{filename[0:-3]}"))
            _info(f"Loaded {filename[0:-3]}")

    # run bot
    bot.run(u.config.get("BOT_TOKEN"), log_handler=None)


if __name__ == "__main__":
    main()
    del logging
