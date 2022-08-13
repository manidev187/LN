import asyncio
import discord
from discord.ext import commands
from discord.utils import get 
import random
from discord.ui import Button, View, Modal, InputText
from discord import message_command, user_command

class apps(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('* Die Erweiterung \'apps\' wurde erfolgreich eingebunden...')


    
    @user_command(name=f"hallo", guild=[942460979961270293]) # Der Name von deiner App. Bei Bedarf auch die Guild einfügen.
    async def App(ctx, message: discord.Member): # Selbsterklärend.
        await ctx.respond(f"{message.mention} hi", ephemeral=True)

        





def setup(bot):
    bot.add_cog(apps(bot))