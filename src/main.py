from dotenv import load_dotenv
load_dotenv()

import os
import asyncio
from typing import Optional
import discord
from discord import app_commands
from discord.ext import commands

from interfaces import Player
from players.ytdlp import YtdlpPlayer

intents = discord.Intents.default()
intents.message_content = True

DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]


class PlayerCog(commands.Cog):
    def __init__(self, bot, player: Player):
        super().__init__()
        self.bot = bot
        self.player = player

    @commands.command()
    async def play(self, ctx: commands.Context, url: str):
        await self.player.play(ctx, url)

    @commands.command()
    async def playnext(self, ctx: commands.Context, url: str):
        await self.player.playnext(ctx, url)

    @commands.command()
    async def pause(self, ctx: commands.Context):
        await self.player.pause(ctx)

    @commands.command()
    async def resume(self, ctx: commands.Context):
        await self.player.resume(ctx)

    @commands.command()
    async def stop(self, ctx: commands.Context):
        await self.player.stop(ctx)

    @commands.command()
    async def skip(self, ctx: commands.Context, skips: str = "1"):
        nskips = 1
        try:
            nskips = int(skips)
        except ValueError:
            await ctx.send("Invalid number of skips")
            return

        await self.player.skip(ctx, nskips)

    @commands.command()
    async def clear(self, ctx: commands.Context):
        await self.player.clear(ctx)

    @commands.command()
    async def queue(self, ctx: commands.Context):
        await self.player.queue(ctx)

async def main():
    bot = commands.Bot(command_prefix="!", intents=intents)
    await bot.add_cog(PlayerCog(bot, YtdlpPlayer(bot)))

    print("starting...")
    await bot.start(DISCORD_TOKEN)

asyncio.run(main())
