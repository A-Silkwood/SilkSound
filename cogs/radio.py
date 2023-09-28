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

    # connect to voice channel
    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is not None:
            voice = await ctx.author.voice.channel.connect()
            self.log_info(f"Connecting to voice channel - ID: {voice.channel.id}")
        else:
            self.log_debug(f"User was not connected to a channel")

    # disconnect from voice channel
    @commands.command()
    async def leave(self, ctx):
        if ctx.author.voice is not None:
            clients = self.bot.voice_clients
            channel = ctx.author.voice.channel

            # exit channel
            for client in clients:
                if channel.id == client.channel.id:
                    await client.disconnect()
                    self.log_info(
                        f"Disconnecting from voice channel - ID: {channel.id}"
                    )
                    return
            self.log_debug(f"Bot was not connected to voice channel - ID: {channel.id}")
        else:
            self.log_debug("User was not connected to a channel")

    @commands.command()
    async def play(self, ctx):
        if ctx.author.voice is not None:
            clients = self.bot.voice_clients
            channel = ctx.author.voice.channel

            # exit channel
            for client in clients:
                if channel.id == client.channel.id:
                    source = await discord.FFmpegOpusAudio.from_probe(
                        os.path.join("assets", "audio", "josh_rawr.mp3"),
                        method="fallback",
                    )
                    await client.play(source)
                    self.log_info(f"Playing audio in voice channel - ID: {channel.id}")
                    return
            self.log_debug(f"Bot was not connected to voice channel - ID: {channel.id}")
        else:
            self.log_debug("User was not connected to a channel")


async def setup(bot):
    await bot.add_cog(Radio(bot))


async def teardown(bot):
    await bot.remove_cog(Radio(bot))
