from logging import currentframe
import discord
from discord.ext import commands
import wavelink


class Music(commands.Cog):
    vc: wavelink.Player = None
    current_track = None

    def __init__(self, bot):
        self.bot = bot

    async def setup(self):
        await wavelink.NodePool.create_node(
            bot=self.bot, host="localhost", port=2333, password="changeme"
        )

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        print(f"{node} is ready")

    @commands.command()
    async def join(self, ctx):
        channel = ctx.author.voice.channel
        if channel:
            self.vc = await channel.connect(cls=wavelink.Player)

    @commands.command()
    async def add(self, ctx, *search_words: str):
        chosen_track = await wavelink.YouTubeTrack.search(
            query=" ".join(search_words), return_first=True
        )
        if chosen_track:
            self.current_track = chosen_track

    @commands.command()
    async def play(self, ctx):
        if self.current_track and self.vc:
            await self.vc.play(self.current_track)


async def setup(bot):
    music_cog = Music(bot)
    await bot.add_cog(music_cog)
    await music_cog.setup()
