# commands/hello.py
import discord
from discord.ext import commands

class Hello(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        await ctx.send("Hello, I'm Nova! -# Also lilac is super adorable <3")

async def setup(bot):
    await bot.add_cog(Hello(bot))
