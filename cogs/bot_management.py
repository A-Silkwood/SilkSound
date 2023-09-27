import discord
from discord.ext import commands
import logging
import logging.handlers

import os

import utils as u


class BotManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # reload all cogs
    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx):
        u.logger.info("Reloading extensions")
        for filename in os.listdir(os.path.join(os.getcwd(), "cogs")):
            if filename.endswith(".py"):
                await self.bot.reload_extension(f"cogs.{filename[0:-3]}")
                u.logger.info(f"Loaded {filename[0:-3]}")

    # close bot
    @commands.command()
    @commands.is_owner()
    async def quit(self, ctx):
        u.logger.warn("Closing due to owner command")
        await self.bot.close()


async def setup(bot):
    await bot.add_cog(BotManagement(bot))


async def teardown(bot):
    await bot.remove_cog(BotManagement(bot))
