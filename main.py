import discord
from discord.ext import commands
import logging
import logging.handlers

from dotenv import dotenv_values
import os


def main():
    # load config
    config = dotenv_values(".env")

    # initialize logger
    logger = logging.getLogger("discord")
    logger.setLevel(logging.DEBUG if config.get("ENV") else logging.INFO)
    if not os.path.exists("logs"):
        os.mkdir("logs")
    handler = logging.handlers.RotatingFileHandler(
        filename=os.path.join(os.getcwd(), "logs", "discord.log"),
        encoding="utf-8",
        maxBytes=32 * 1024 * 1024,  # 32 MiB
        backupCount=5,  # Rotate through 5 files
    )
    dt_fmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(
        "[{asctime}] [{levelname:<8}] {name}: {message}", dt_fmt, style="{"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # initialize bot
    intents = discord.Intents.default()
    intents.message_content = True
    client = commands.Bot(command_prefix="!", intents= intents)
    
    @client.event
    async def on_ready():
        print(f"We have logged in as {client.user}")
        
    @client.command()
    async def basic(ctx):
        await ctx.send("test")   
        
    @client.command()
    async def positional(ctx, arg1):
        await ctx.send(f"{arg1}")    
    
    @client.command()
    async def positional(ctx, arg1, arg2):
        await ctx.send(f"{arg1} {arg2}")
    
    @client.command()
    async def positional(ctx, arg1, arg2, arg3):
        await ctx.send(f"{arg1} {arg2} {arg3}")
        
    @client.command()
    async def variable(ctx, *args):
        await ctx.send(args)

    # run bot
    client.run(config.get("BOT_TOKEN"), log_handler=None)


if __name__ == "__main__":
    main()
