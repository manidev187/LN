import asyncio
import discord
from discord.ext import commands
from discord.utils import get 
import random
import time

class giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('* Die Erweiterung \'giveaway\' wurde erfolgreich eingebunden...')

    @commands.command()
    async def gw(ctx, time):



        time_final = int(time.time()) + (time * 60)

        await ctx.send(f"Ends: <t:{int(time_final)}:R>")


def setup(bot):
    bot.add_cog(giveaway(bot))