import settings
import discord
from discord.ext import commands


def run():
    intents = discord.Intents.default()
    bot = commands.Bot(command_prefix="CH3", intents=intents)
    print(bot)


if __name__ == "__main__":
    run()