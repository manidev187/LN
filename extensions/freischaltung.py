import asyncio
import discord
from discord.ext import commands
from discord.ui import Button, View, Modal, InputText
from discord.utils import get 
import random

logo = "https://cdn.discordapp.com/attachments/962707012339245146/1000181293293777050/Screenshot_2022-07-21_230205.png"

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


    @commands.command()
    async def embed(self, ctx):
        await ctx.channel.purge(limit=1)

        button = Button(label="Ticket Channel", url="https://discord.com/channels/942460979961270293/942475978200985742")

        view = View(timeout=None)
        view.add_item(button)

        embed = discord.Embed(title="L&N Services™ Präsentiert- Whitelistsystem für FiveM Server", color=0xff0000)
        embed.add_field(name="Was ist ein Whitelistsystem?", value="""> Ein Whitelistsystem ist ein System, das einem Server Team von einem FiveM Server die Whitelist vereinfacht.
        > Diese Whitelists sind einzigartig, da sie von uns selber exclusiv sind.""", inline=False)
        embed.add_field(name="Funktionen", value="""> Man drückt einen Button und dann wird eine Nachricht geschickt die einen Counter von 60 Sekunden beinhaltet.
        > Sollte der Counter abgelaufen sein, muss man den Verify Button erneut drücken.
        > Sobald man alle Buttons gedrückt hat, öffnet sich ein Forumular/Modal wo Fragen stehen und man diese beantworten muss.
        > Das Team bekommt dann ich einen Definierten Channel eine Nachricht mit den Inhalt der zuvor von dem User ausgefühlt wurde.
        > zum [Video](https://vimeo.com/732625071)""", inline=False)
        embed.add_field(name="Preis", value="> 7€", inline=False)
        embed.add_field(name="Interessiert?", value="""> Dann klick unten auf Ticket Kanal und Erstell in in der Jeweiligen Katergorie ein Ticket.""")
        embed.set_thumbnail(url=logo)
        embed.set_author(name="L&N Services™", icon_url=logo)
        
        message = await ctx.send(embed=embed, view=view)
        await ctx.send("https://cdn.discordapp.com/attachments/962707012339245146/1000182598112387103/2022-07-23_01-10-34_Trim.mp4")




def setup(bot):
    bot.add_cog(price(bot))