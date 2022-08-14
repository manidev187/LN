import asyncio
import discord
from discord.ext import commands
from discord.utils import get 
from discord.ext.commands import has_permissions, MissingPermissions


class sayclear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('* Die Erweiterung \'say-clear\' wurde erfolgreich eingebunden...')

    @commands.command()
    @commands.cooldown(1,5, commands.BucketType.user, )
    async def say(self, ctx, *, respone=None):
        role = discord.utils.get(ctx.guild.roles, id=942460980124872726)
        if role not in ctx.author.roles:
            await ctx.send("Du hast keine rechte dafür!", delete_after=10)
            return
        if respone is None:
            await ctx.send("Gib eine Nachricht an!")
            return
        await ctx.channel.purge(limit=1)
        await ctx.send(respone)

    @say.error
    async def say_error(ctx, error): 
     if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f'Command "say" is on cooldown, you can us it in {round(error.retry_after, 5)} seconds.')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1,5, commands.BucketType.user)

    async def clear(self, ctx, amount=10): 

        await ctx.channel.purge(limit=amount + 1)
        embed = discord.Embed()
        embed = discord.Embed(title="Gelöscht!", description=f"Ich habe ``{amount}`` Nachrichten  für dich gelöscht!🚔", colour=0x00B6FF)
        await ctx.send(embed=embed, delete_after=10.1)

    @clear.error
    async def kick_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            text = "Sorry {}, du hast keine rechte dafür".format(ctx.message.author)
            await ctx.send(text)

    @commands.command()
    async def give(self, ctx):
        role = discord.utils.get(ctx.guild.roles, name="Ping")

        guild = ctx.guild
        role = ctx.guild.get_role(982962526297944126)
        for m in guild.members:
            await m.add_roles(role)


        await ctx.send("Done") 

    @commands.command()
    async def deinemum(self, ctx):
        await ctx.send("Test done")


def setup(bot):
    bot.add_cog(sayclear(bot))