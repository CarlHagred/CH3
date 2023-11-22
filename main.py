import settings
import discord
from discord.ext import commands


def run():
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="CH3 ", intents=intents)

    @bot.event
    async def on_ready():
        print(bot.user)
        print(bot.user.id)
        await bot.load_extension("cogs.music")

    @bot.command()
    async def ping(ctx):
        await ctx.send("pong")

    bot.run(settings.DISCORD_API_SECRET)


if __name__ == "__main__":
    run()
