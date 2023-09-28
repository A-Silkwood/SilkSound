import discord
from discord.ext import commands

import os

from cog import Cog


class Radio(Cog):
    def __init__(self, bot):
        super().__init__(bot)
        self.name = "radio"

    # connect to a voice channel
    @commands.command()
    async def join(self, ctx):
        # check if user is in a voice channel
        if ctx.author.voice is not None:
            try:
                # try to join voice channel
                voice = await ctx.author.voice.channel.connect()
                self.log_info(
                    f"Joined voice channel: Channel ({voice.channel.id}) User ({ctx.author.id})"
                )
            except Exception as e:
                self.log_debug(
                    f"Couldn't join voice channel; ErrMsg-[ {e} ] : User ({ctx.author.id})"
                )
        else:
            self.log_debug(
                f"Couldn't join voice channel; User not in a channel: User({ctx.author.id})"
            )

    # disconnect from a voice channel
    @commands.command()
    async def leave(self, ctx):
        # check if user is in a voice channel
        if ctx.author.voice is not None:
            clients = self.bot.voice_clients
            channel = ctx.author.voice.channel
            # find if a voice client matches user's voice channel
            for client in clients:
                if channel.id == client.channel.id:
                    # disconnect from the voice channel
                    await client.disconnect()
                    self.log_info(
                        f"Left voice channel: Channel ({channel.id}) User ({ctx.author.id})"
                    )
                    return
            self.log_debug(
                f"Couldn't leave voice channel; Bot not in channel: Channel ({channel.id}) User ({ctx.author.id})"
            )
        else:
            self.log_debug(
                f"Couldn't leave voice channel; User not in a channel:  Channel ({channel.id}) User ({ctx.author.id})"
            )

    @commands.command()
    async def play(self, ctx, url):
        # check if user is in a voice channel
        if ctx.author.voice is not None:
            clients = self.bot.voice_clients
            channel = ctx.author.voice.channel
            # check if a voice client matches user's voice channel
            for client in clients:
                if channel.id == client.channel.id:
                    
                    # check if url is valid
                    # check for video
                    # download mp3
                    # encode into OPUS
                    # play or queue video
                    # delete mp3
                    
                    self.log_info(
                        f"Playing video: Channel ({channel.id}) URL ({url}) User ({ctx.author.id})"
                    )
                    return
            self.log_debug(
                f"Couldn't play video; Bot not in channel: Channel ({channel.id}) User ({ctx.author.id})"
            )
        else:
            self.log_debug(
                f"Couldn't play video; User not in a channel: Channel ({channel.id}) User ({ctx.author.id})"
            )


async def setup(bot):
    await bot.add_cog(Radio(bot))


async def teardown(bot):
    await bot.remove_cog(Radio(bot))
