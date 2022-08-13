import asyncio
import discord
from discord.ext import commands
from discord.utils import get 
import random


class price(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print('* Die Erweiterung \'price\' wurde erfolgreich eingebunden...')
    
    @commands.command()
    async def schaltung(self, ctx, member: discord.Member):
        if member is None: 
            await ctx.send("Bitte gib einen User an!")
        else:
            await member.add_roles(discord.utils.get(ctx.guild.roles, name="Prices"))
            channel = self.bot.get_channel(953000070482128978)
            await channel.send(f"{member.mention} hat die Rechte erhalten!", delete_after=10)
            await member.send("Du wurdest erfolgreich zu den <#953000070482128978> hinzugefügt!")







def setup(bot):
    bot.add_cog(price(bot))