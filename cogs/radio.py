import asyncio
from typing import Self
import discord
from discord.ext import commands
import os
import uuid
import yt_dlp as yt

from cog import Cog
import utils as u


class Radio(Cog):
    def __init__(self, bot):
        super().__init__(bot)
        self.name = "radio"  # used for logging
        self.sessions = {}

        # initialize all sessions
        for client in self.bot.voice_clients:
            self.sessions[str(client.channel.id)] = {
                "paused": False,
                "queue": [],
                "lock_play": False,
            }

    # find voice client using given channel id
    def find_client(self, channel_id):
        for client in self.bot.voice_clients:
            if client.channel.id == channel_id:
                return client
        return None

    # connect to a voice channel
    @commands.command()
    async def join(self, ctx):
        # check if user is in a voice channel
        if ctx.author.voice is not None:
            try:
                # try to join voice channel
                voice = await ctx.author.voice.channel.connect()
                self.info(
                    "Joined voice channel",
                    {
                        "user": ctx.author.id,
                        "channel": voice.channel.id,
                    },
                )
            except Exception as e:
                self.error(
                    f"Couldn't join voice channel; ErrMsg-[ {e} ] ",
                    {"user": ctx.author.id},
                )
        else:
            self.debug(
                "Couldn't join voice channel; User not in a channel",
                {"user": ctx.author.id},
            )

    # disconnect from a voice channel
    @commands.command()
    async def leave(self, ctx):
        # check if user is in a voice channel
        if ctx.author.voice is not None:
            channel = ctx.author.voice.channel

            client = self.find_client(channel.id)
            if client is not None:
                # disconnect from the voice channel
                try:
                    await client.disconnect()
                    self.info(
                        "Left voice channel",
                        {"user": ctx.author.id, "channel": channel.id},
                    )
                except Exception as e:
                    self.error(
                        f"Couldn't leave voice channel; ErrMsg-[ {e} ] ",
                        {"user": ctx.author.id, "channel": channel.id},
                    )
            else:
                self.debug(
                    "Couldn't leave voice channel; Bot not in channel",
                    {"user": ctx.author.id, "channel": channel.id},
                )
        else:
            self.debug(
                "Couldn't leave voice channel; User not in a channel",
                {"user": ctx.author.id, "channel": channel.id},
            )

    # called when voice state changes
    @commands.Cog.listener()
    async def on_voice_state_update(self, user, before, after):
        # bot specific voice state changes
        if str(user.id) == u.config.get("BOT_CLIENTID"):
            ## create and remove sessions when bot moves voice channels

            # remove old session
            if (
                before.channel is not None
                and (after.channel is None or before.channel.id != after.channel.id)
                and self.sessions.get(str(before.channel.id)) is not None
            ):
                self.sessions.pop(str(before.channel.id))
                self.debug(
                    "Removed session",
                    {"channel": before.channel.id},
                )

            # create new session
            if after.channel is not None:
                self.sessions[str(after.channel.id)] = {
                    "paused": False,
                    "queue": [],
                    "lock_play": False,
                }
                self.debug(
                    "Created session",
                    {"channel": after.channel.id},
                )

    # queue audio from given url to play in voice channel
    @commands.command()
    async def play(self, ctx, url):
        if ctx.author.voice is not None:
            channel = ctx.author.voice.channel
            client = self.find_client(channel.id)

            if client is not None:
                # check length of source
                # TODO return if > 20 min

                # vars
                queue = self.sessions.get(str(channel.id)).get("queue")
                audio_id = uuid.uuid4()
                download_opts = {
                    "outtmpl": os.path.join("assets", "audio", f"{audio_id}.%(ext)s"),
                    "format": "opus/bestaudio/best",
                    "postprocessors": [
                        {
                            "key": "FFmpegExtractAudio",
                            "preferredcodec": "opus",
                        }
                    ],
                }

                try:
                    # download audio
                    with yt.YoutubeDL(download_opts) as ydl:
                        error_code = ydl.download(url)
                    # queue audio
                    queue.append(audio_id)
                    self.info(
                        "Added audio to session queue",
                        {
                            "user": ctx.author.id,
                            "url": url,
                            "audio": audio_id,
                            "pos": len(queue),
                            "channel": channel.id,
                        },
                    )
                except Exception as e:
                    self.error(
                        f"Couldn't queue audio; ErrMsg-[ {e} ] ",
                        {"user": ctx.author.id, "url": url, "channel": channel.id},
                    )

                # start audio play
                if self.sessions.get(str(channel.id)).get("paused"):
                    # unpause
                    await self.toggle_pause(channel.id)
                elif not client.is_playing():
                    # start playing
                    await self.play_audio(channel.id)
            else:
                self.debug(
                    "Couldn't queue audio; Bot not in channel",
                    {"user": ctx.author.id, "channel": channel.id},
                )
        else:
            self.debug(
                "Couldn't queue audio; User not in a channel",
                {"user": ctx.author.id, "channel": channel.id},
            )

    # play next audio source in a channel's queue
    async def play_audio(self, channel_id):
        client = self.find_client(channel_id)
        if client is not None:
            queue = self.sessions.get(str(channel_id)).get("queue")

            if client.is_playing():
                self.warning(
                    "Couldn't play next in queue; Already playing audio",
                    {"channel": channel_id},
                )
            elif len(queue) > 0:
                # play next audio in queue
                audio_id = queue[0]
                source = await discord.FFmpegOpusAudio.from_probe(
                    os.path.join("assets", "audio", f"{audio_id}.opus"),
                    method="fallback",
                )

                # check for race condition
                # TODO use more graceful solution
                if not client.is_playing():
                    client.play(
                        source,
                        after=lambda e: asyncio.run(self.play_next(channel_id, e)),
                    )
                    self.info(
                        "Playing next audio in queue",
                        {"audio": audio_id, "channel": channel_id},
                    )
                else:
                    self.warning(
                        "Couldn't play next in queue; Race condition",
                        {"channel": channel_id},
                    )
            else:
                self.info("Complete audio queue", {"channel": channel_id})
        else:
            self.error(
                "Couldn't play next in queue; Channel client not found",
                {"channel": channel_id},
            )

    # prepare for next audio source to play
    async def play_next(self, channel_id, err):
        queue = self.sessions.get(str(channel_id)).get("queue")

        # possible play error
        if err is not None:
            self.error(
                f"Problem playing audio; ErrMsg-[ {err} ] ",
                {
                    "audio": queue[0] if len(queue) > 0 else None,
                    "channel": channel_id,
                },
            )

        # remove current audio
        if len(queue) > 0:
            audio_id = queue[0]
            try:
                # removing from queue first to remove further bugs if the file could not be removed
                queue.pop(0)
                os.remove(
                    os.path.join(
                        "assets",
                        "audio",
                        f"{audio_id}.opus",
                    )
                )
                self.debug(
                    "Removed audio from queue",
                    {"audio": audio_id, "channel": channel_id},
                )
            except Exception as e:
                # file most likely won't get deleted
                self.critical(
                    f"Couldn't remove audio; ErrMsg-[ {e} ] ",
                    {"audio": audio_id, "channel": channel_id},
                )

        # continue queue
        await self.play_audio(channel_id)

    # pause/unpause audio play
    @commands.command()
    async def pause(self, ctx):
        # check if user is in a voice channel
        if ctx.author.voice is not None:
            channel = ctx.author.voice.channel

            client = self.find_client(channel.id)
            if client is not None:
                # toggle the pause of the session
                await self.toggle_pause(channel.id)
                self.info(
                    "Toggled pause of session",
                    {"user": ctx.author.id, "channel": channel.id},
                )
            else:
                self.debug(
                    "Couldn't pause/unpause; Bot not in channel",
                    {"user": ctx.author.id, "channel": channel.id},
                )
        else:
            self.debug(
                "Couldn't pause/unpause; User not in a channel",
                {"user": ctx.author.id, "channel": channel.id},
            )

    # pause/unpause audio playing in a channel
    async def toggle_pause(self, channel_id):
        session = self.sessions.get(str(channel_id))
        if session is not None:
            session["paused"] = not session["paused"]

            client = self.find_client(channel_id)
            if client is not None:
                if not session.get("paused"):
                    # play or resume audio session
                    try:
                        if client.is_paused():
                            client.resume()
                            self.info("Resumed playing audio", {"channel": channel_id})
                        else:
                            await self.play_audio(channel_id)
                    except Exception as e:
                        session["paused"] = not session["paused"]  # revert
                        self.error(
                            f"Couldn't resume audio; ErrMsg-[ {e} ] ",
                            {"channel": channel_id},
                        )
                else:
                    # pause audio session
                    try:
                        if client.is_playing():
                            client.pause()
                    except Exception as e:
                        session["paused"] = not session["paused"]  # revert
                        self.error(
                            f"Couldn't pause audio; ErrMsg-[ {e} ] ",
                            {"channel": channel_id},
                        )
            else:
                self.error(
                    "Couldn't pause/unpause; Channel client not found",
                    {"channel": channel_id},
                )
        else:
            self.error(
                "Couldn't pause/unpause; Session does not exists",
                {"channel": channel_id},
            )


async def setup(bot):
    await bot.add_cog(Radio(bot))


async def teardown(bot):
    await bot.remove_cog(Radio(bot))
