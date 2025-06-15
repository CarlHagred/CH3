import asyncio
from typing import Any
import discord
from discord.ext import commands
from interfaces import Player

from yt_dlp import YoutubeDL

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)



class YtdlpPlayer(Player):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.voice_client = None
        self.song_queue = []

    async def play(self, ctx: commands.Context, url: str):
        if not isinstance(ctx.author, discord.Member) or not ctx.author.voice:
            return

        if not isinstance(ctx.author.voice, discord.VoiceState):
            return

        voice_channel = ctx.author.voice.channel
        if not voice_channel:
            await ctx.send("You are not connected to a voice channel.")
            return

        # connect or move to correct voice channel
        if self.voice_client:
            if not self.voice_client.is_connected():
                self.voice_client = await voice_channel.connect()

            if self.voice_client.channel != voice_channel:
                await self.voice_client.move_to(voice_channel)
        else:
            self.voice_client = await voice_channel.connect()

        # resolve the song
        song = await self.resolve_song(url)
        if not song:
            await ctx.send(f"Could not find song {url}")

        self.song_queue.append(song)

        # if we're not playing already, start playing :-)
        if not self.voice_client.is_playing():
            while len(self.song_queue) > 0:
                song = self.song_queue.pop(0)
                await self.play_song(ctx, song)

    async def resolve_song(self, url: str):
        loop = asyncio.get_event_loop()
        ytdlp = YoutubeDL({"format": "bestaudio/best",})
        info: dict[str, Any] | None = await loop.run_in_executor(None, lambda: ytdlp.extract_info(url, download=False))
        if not info:
            return None

        return (info["title"], info["url"])

    async def play_song(self, ctx: commands.Context, song: tuple[str, str]):
        title, url = song
        await ctx.send(content=f"Playing {title}")

        # play the stream
        try:
            if not self.voice_client: # should not happen?
                return

            ffmpeg = discord.FFmpegOpusAudio(
                url,
                before_options="-fflags nobuffer -flags low_delay -rtbufsize 1G -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
                options="-vn"
            )
            # ffmpeg = discord.FFmpegPCMAudio(
            #     url,
            #     before_options="-fflags nobuffer -flags low_delay -rtbufsize 1G",
            #     options="-vn"
            # )
            ffmpeg.read() # this is a hack to make sure the stream is opened before playing
            self.voice_client.play(ffmpeg)
            while self.voice_client.is_playing() or self.voice_client.is_paused():
                await asyncio.sleep(1)
        except Exception as e:
            print("oh no")
            logging.exception(e)
            await ctx.send("Error playing the song.")
            return


    async def stop(self, ctx: commands.Context):
        if not self.voice_client:
            await ctx.send("Nothing playing.")
            return

        await self.voice_client.disconnect()


    async def pause(self, ctx: commands.Context):
        if not self.voice_client:
            await ctx.send("Nothing playing.")
            return
        self.voice_client.pause()


    async def resume(self, ctx: commands.Context):
        if not self.voice_client:
            await ctx.send("Nothing playing.")
            return
        self.voice_client.resume()

    async def skip(self, ctx: commands.Context, skips: int):
        # TODO skip multiple? using `skips`
        if not self.voice_client:
            await ctx.send("Nothing playing.")
            return

        self.voice_client.stop()

    async def queue(self, ctx: commands.Context):
        if not self.song_queue:
            await ctx.send("Queue is empty.")
            return

        songs = "\n".join([f"- {title}" for title, _ in self.song_queue])
        await ctx.send("Queue:\n" + songs)

    async def playnext(self, ctx: commands.Context, url: str):
        logging.debug(f"Adding {url} to the front of the queue")
        self.song_queue.insert(0, await self.resolve_song(url))

    async def clear(self, ctx: commands.Context):
        self.song_queue.clear()
