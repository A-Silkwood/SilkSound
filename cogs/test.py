import discord
from discord.ext import commands

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
    await bot.add_cog(Test(bot))