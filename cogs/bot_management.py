import discord
from discord.ext import commands
import logging
import logging.handlers

import os

import utils as u


class BotManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.name = "bot_management"
    
    def log_debug(self, message):
        u.logger.debug(f'.{self.name}: {message}')

    def log_info(self, message):
        u.logger.info(f'.{self.name}: {message}')

    def log_warning(self, message):
        u.logger.warning(f'.{self.name}: {message}')

    def log_error(self, message):
        u.logger.error(f'.{self.name}: {message}')

    def log_critical(self, message):
        u.logger.critical(f'.{self.name}: {message}')

    # reload all cogs
    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx):
        self.log_info("Reloading extensions")
        for filename in os.listdir(os.path.join(os.getcwd(), "cogs")):
            if filename.endswith(".py"):
                await self.bot.reload_extension(f"cogs.{filename[0:-3]}")
                self.logger.info(f"Loaded {filename[0:-3]}")

    # close bot
    @commands.command()
    @commands.is_owner()
    async def quit(self, ctx):
        self.logger.warn("Closing due to owner command")
        await self.bot.close()


async def setup(bot):
    await bot.add_cog(BotManagement(bot))


async def teardown(bot):
    await bot.remove_cog(BotManagement(bot))
