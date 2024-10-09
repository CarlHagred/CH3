from logging import currentframe
import discord
from discord.ext import commands
import wavelink
import yt_dlp


class Music(commands.Cog):
    vc = None
    current_track = None

    def __init__(self, bot):
        self.bot = bot

    async def setup(self):
        pass

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        print(f"{node} is ready")

    @commands.command()
    async def join(self, ctx):
        channel = ctx.author.voice.channel
        if channel:
            self.vc = await channel.connect()

    async def download_mp3(self, youtube_url, output_path="song"):
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': output_path,
            'noplaylist': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])

        return output_path + ".mp3" 

    @commands.command()
    async def add(self, ctx, *search_words: str):
        chosen_track = await self.download_mp3(" ".join(search_words), "song")
        if chosen_track:
            self.current_track = chosen_track

        if not ctx.author.voice:
            await ctx.send("You need to be in a voice channel to play music!")
            return
        
        channel = ctx.author.voice.channel
        voice_client = await channel.connect()

        voice_client.play(discord.FFmpegPCMAudio(self.current_track))
        '''
        while voice_client.is_playing():
            await discord.utils.sleep_until(voice_client.is_done())
        
        await voice_client.disconnect()
        os.remove(mp3_path)
        '''
    


    @commands.command()
    async def play(self, ctx):
        if self.current_track and self.vc:
            await self.vc.play(self.current_track)


async def setup(bot):
    music_cog = Music(bot)
    await bot.add_cog(music_cog)
    await music_cog.setup()
