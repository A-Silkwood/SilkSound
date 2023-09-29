import asyncio
import discord
import discord.http
from discord.ext import commands
from dotenv import dotenv_values
import logging
import logging.handlers
import os
from stringcase import titlecase

import utils as u


def _fdata(data: dict = {}):
    # no data to format
    if len(data) == 0:
        return ""

    # add each key pair to string
    data_str = ": ["
    for key, val in data.items():
        data_str = f"{data_str} {titlecase(key)} ({val})"

    return data_str + " ]"


def debug(msg: str, data: dict = {}):
    u.logger.debug(f": {msg}{_fdata(data)}")


def info(msg: str, data: dict = {}):
    u.logger.info(f": {msg}{_fdata(data)}")


def warning(msg: str, data: dict = {}):
    u.logger.warning(f": {msg}{_fdata(data)}")


def error(msg: str, data: dict = {}):
    u.logger.error(f": {msg}{_fdata(data)}")


def critical(msg: str, data: dict = {}):
    u.logger.critical(f": {msg}{_fdata(data)}")


# startup bot
def main():
    # check for directories
    if not os.path.exists("logs"):
        os.mkdir("logs")
    if not os.path.exists("assets"):
        os.mkdir("assets")
    if not os.path.exists("assets/audio"):
        os.mkdir("assets/audio")
        
    # create logger
    u.init_logger()

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
        info("Successful login", {"client": bot.user.id})

    # load cogs
    info("Loading extensions")
    for filename in os.listdir(os.path.join(os.getcwd(), "cogs")):
        if filename.endswith(".py"):
            asyncio.run(bot.load_extension(f"cogs.{filename[0:-3]}"))
            info("Loaded extension", {"extension": filename[0:-3]})

    # run bot
    bot.run(u.config.get("BOT_TOKEN"), log_handler=None)


if __name__ == "__main__":
    main()
    del logging
