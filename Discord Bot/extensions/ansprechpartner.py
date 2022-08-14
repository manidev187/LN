import asyncio
import discord
from discord.ext import commands
from discord.ui import Button, View, Modal, InputText



logo = "https://cdn.discordapp.com/attachments/962707012339245146/992861858136592444/Komp_1.gif"

class ansprech(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.Cog.listener()
    async def on_ready(self):
        print('* Die Erweiterung \'Vorlage\' wurde erfolgreich eingebunden...')



    @commands.command()
    async def ansprech(self, ctx, member: discord.Member):
        await ctx.channel.purge(limit=1)

        button = Button(label="Feedback", url=f"https://discord.com/channels/942460979961270293/987863893881815120")
        
        
        view = View(timeout=None)
        view.add_item(button)

        embed = discord.Embed(title="Ansprechpartner", description=f"""Der Ansprechpartner für dein Ticket ist {member.mention}""", color=0xf7051d)

        embed.set_footer(text="Copyright © 2022 L&N Services™ - All Rights Reserved")
        embed.set_author(name="L&N Services™", icon_url=logo)

        await ctx.send(embed=embed, view = view)



def setup(bot):
    bot.add_cog(ansprech(bot))