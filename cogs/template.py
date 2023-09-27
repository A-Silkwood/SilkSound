import discord
from discord.ext import commands
import logging
import logging.handlers

import os

import utils as u


class Template(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.name = "template"
    
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

    # command with 3 positional arguments
    @commands.command()
    async def basic(self, ctx):
        await ctx.send(f"Test")

    # command with 3 positional arguments
    @commands.command()
    async def positional(self, ctx, arg1, arg2, arg3):
        await ctx.send(f"{arg1} {arg2} {arg3}")

    # command with variable argument count
    @commands.command()
    async def variable(self, ctx, *args):
        await ctx.send(args)

    # command with no argument handling; arg is just the rest of the msg
    @commands.command()
    async def custom(self, ctx, *, arg):
        await ctx.send(arg)


async def setup(bot):
    await bot.add_cog(Template(bot))


async def teardown(bot):
    await bot.remove_cog(Template(bot))
