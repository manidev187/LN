import asyncio
import discord
from discord.ext import commands
from discord.ui import Button, View, Modal, InputText

logo = "https://cdn.discordapp.com/attachments/962707012339245146/992861858136592444/Komp_1.gif"

class marktplatz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('* Die Erweiterung \'marktplatz\' wurde erfolgreich eingebunden...')


    @commands.command()
    async def marktplatz(self, ctx):
        await ctx.channel.purge(limit=1)
        button = Button(label="Ticket Channel", url="https://discord.com/channels/942460979961270293/942475978200985742")

        view = View(timeout=None)
        view.add_item(button)
        
                                                     
        embed = discord.Embed(title="L&N Service Präsentiert\n", description="""Wir bieten euch jetzt die möglichkeit eure Sachen wie z.B Fivem Stuff bei uns zu verkaufen
    """, colour=0xfa0008)
        embed.add_field(name="Was bekommt ihr bei uns:", value="> Wenn ihr euch für uns interessiert bekommt ihr einen eigenen Channel und könnt dort eure sachen anbieten")
        embed.add_field(name="Interessiert?", value="> Dann klick unten auf Ticket Kanal und Erstell in der Jeweiligen Kanal ein Ticket", inline=False)
        embed.set_footer(text="Copyright © 2022 L&N Services™ - All Rights Reserved")
        embed.add_field(name="Bedingungen", value="> Wird per Ticket abgeklärt", inline=False)
        embed.set_author(name="L&N Services™", icon_url=logo)

        

        await ctx.send(embed=embed, view=view)

def setup(bot):
    bot.add_cog(marktplatz(bot))