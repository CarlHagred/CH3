from discord.ext import commands
import abc


class Player(abc.ABC):
    @abc.abstractmethod
    async def play(self, ctx: commands.Context, url: str):
        pass

    @abc.abstractmethod
    async def playnext(self, ctx: commands.Context, url: str):
        pass

    @abc.abstractmethod
    async def pause(self, ctx: commands.Context):
        pass

    @abc.abstractmethod
    async def resume(self, ctx: commands.Context):
        pass

    @abc.abstractmethod
    async def stop(self, ctx: commands.Context):
        pass

    @abc.abstractmethod
    async def skip(self, ctx: commands.Context, skips: int):
        pass

    @abc.abstractmethod
    async def queue(self, ctx: commands.Context):
        pass

    @abc.abstractmethod
    async def clear(self, ctx: commands.Context):
        pass
