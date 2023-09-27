import discord
from discord.ext import commands
import logging
import logging.handlers

import os

from cog import Cog


class Admin(Cog):
    def __init__(self, bot):
        super().__init__(bot)
        self.name = "admin"

    # reload all cogs
    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx):
        self.log_info("Reloading extensions")
        for filename in os.listdir(os.path.join(os.getcwd(), "cogs")):
            if filename.endswith(".py"):
                await self.bot.reload_extension(f"cogs.{filename[0:-3]}")
                self.log_info(f"Loaded {filename[0:-3]}")

    # close bot
    @commands.command()
    @commands.is_owner()
    async def quit(self, ctx):
        self.log_warning("Closing due to owner command")
        await self.bot.close()


async def setup(bot):
    await bot.add_cog(Admin(bot))


async def teardown(bot):
    await bot.remove_cog(Admin(bot))
