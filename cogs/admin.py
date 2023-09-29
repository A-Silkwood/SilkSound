import discord
from discord.ext import commands
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
        self.info("Reloading extensions")
        for filename in os.listdir(os.path.join(os.getcwd(), "cogs")):
            if filename.endswith(".py"):
                await self.bot.reload_extension(f"cogs.{filename[0:-3]}")
                self.info(f"Loaded extension", {"extension": filename[0:-3]})
        print("Finished reload")

    # close bot
    @commands.command()
    @commands.is_owner()
    async def quit(self, ctx):
        self.warning("Closing app", {"reason": "Owner Command"})
        await self.bot.close()


async def setup(bot):
    await bot.add_cog(Admin(bot))


async def teardown(bot):
    await bot.remove_cog(Admin(bot))
