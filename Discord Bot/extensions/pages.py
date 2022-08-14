import datetime
from datetime import datetime
import time
import discord
from discord.ext import commands
from discord.ext.commands import CommandInvokeError
from discord import utils
import asyncio
from discord.ext import commands, pages
from discord.ext import tasks, commands


class bilder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.launch_time = datetime.utcnow()

    # Events sind bei cogs "listener"
    @commands.Cog.listener()
    async def on_ready(self):
        print('* Die Erweiterung \'pages\' wurde erfolgreich eingebunden...')

    @commands.command(name="feedback")
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def feedback(self, ctx):

        if ctx.channel.id != 987863893881815120:
            return
    
        await ctx.channel.purge(limit=1)
        embed = discord.Embed(title=f"`⭐`⇒ Feedback", description="Hallo, da wir unser Supportsystem ständig verbessern wollen, brauchen wir dein Feedback.", color=0x3e4ad6)
        embed.add_field(name="`⭐`Wähle Sterne", value="Bitte benutz die Buttonsum, die Sterne anzahl von **1 und 5** auszuwählen.\n Dein Feedback kann nur die Projektleitung einsehen!")
        embed.set_image(url="https://cdn.discordapp.com/attachments/982755800210620516/982787438315466772/unknown.png")

        embed2 = discord.Embed(title=f"`⭐`⇒ __Negatives Feedback__", description="Hallo, vielen Dank für dein Feedback von:\n :star:<:stern:987863964203507792><:stern:987863964203507792><:stern:987863964203507792><:stern:987863964203507792> Stern.", color=0xfc0505)
        embed2.add_field(name="`📌`", value="Solltest du eine Beschwerde haben, so öffne ein Ticket in unserem Supportsystem!")

        embed3 = discord.Embed(title=f"`⭐`⇒ __Negatives Feedback__", description="Hallo, vielen Dank für dein Feedback von:\n :star::star:<:stern:987863964203507792><:stern:987863964203507792><:stern:987863964203507792> Stern.", color=0xc45145)
        embed3.add_field(name="`📌`", value="Solltest du eine Beschwerde haben, so öffne ein Ticket in unserem Supportsystem!")



        embed5 = discord.Embed(title=f"`⭐`⇒ __Postives Feedback__", description="Hallo, vielen Dank für dein Feedback von:\n :star::star::star:<:stern:987863964203507792><:stern:987863964203507792> Stern.", color=0x117d13)
        embed5.add_field(name="`📌`", value="Solltest du Fragen haben, melde dich bei uns!")

        embed6 = discord.Embed(title=f"`⭐`⇒ __Postives Feedback__", description="Hallo, vielen Dank für dein Feedback von:\n :star::star::star::star:<:stern:987863964203507792> Stern.", color=0x179c34)
        embed6.add_field(name="`📌`", value="Solltest du Fragen haben, melde dich bei uns!")

        embed7 = discord.Embed(title=f"`⭐`⇒ __Postives Feedback__", description="Hallo, vielen Dank für dein Feedback von:\n :star::star::star::star::star: Stern.", color=0x02f738)
        embed7.add_field(name="`📌`", value="Solltest du Fragen haben, melde dich bei uns!")



        embed.set_footer(text=f"Feedback von {ctx.author.display_name}", icon_url=ctx.author.avatar.url)
        embed2.set_footer(text=f"Feedback von {ctx.author.display_name}", icon_url=ctx.author.avatar.url)
        embed3.set_footer(text=f"Feedback von {ctx.author.display_name}", icon_url=ctx.author.avatar.url)
        embed5.set_footer(text=f"Feedback von {ctx.author.display_name}", icon_url=ctx.author.avatar.url)
        embed6.set_footer(text=f"Feedback von {ctx.author.display_name}", icon_url=ctx.author.avatar.url)
        embed7.set_footer(text=f"Feedback von {ctx.author.display_name}", icon_url=ctx.author.avatar.url)

        seiten = [embed, embed2, embed3, embed5, embed6, embed7]

        paginator = pages.Paginator(pages=seiten, author_check=True, timeout=60, disable_on_timeout=True,
                                        show_indicator=False)

        await paginator.send(ctx)

    @feedback.error
    async def feedback_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title="Cooldown",
                                description='Vielen dank für dein Feedback. Bitte warte {:.2f} Stunde(n) um es erneut nutzen zu können'.format(
                                    error.retry_after / 60 / 60), color=0xff0000)
            await ctx.send(embed=embed)
        else:
            raise error




def setup(bot):
    bot.add_cog(bilder(bot))