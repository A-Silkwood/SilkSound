import discord
from discord.ext import commands

import os

class BotManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    # reload all cogs
    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx):
        print("Reloading extensions")
        for filename in os.listdir(os.path.join(os.getcwd(), "cogs")):
            if filename.endswith(".py"):
                await self.bot.reload_extension(f"cogs.{filename[0:-3]}")
                print(f"Loaded '{filename[0:-3]}'")
    
async def setup(bot):
    await bot.add_cog(BotManagement(bot))
    
async def teardown(bot):
    await bot.remove_cog(BotManagement(bot))