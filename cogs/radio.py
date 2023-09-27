import discord
from discord.ext import commands
import logging
import logging.handlers

import os

from cog import Cog


class Radio(Cog):
    def __init__(self, bot):
        super().__init__(bot)
        self.name = "radio"

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
    await bot.add_cog(Radio(bot))


async def teardown(bot):
    await bot.remove_cog(Radio(bot))
