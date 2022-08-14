import asyncio
import discord
from discord.ext import commands
from discord.utils import get 
import datetime
from datetime import datetime, timedelta


class fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('* Die Erweiterung \'fun\' wurde erfolgreich eingebunden...') 

    @commands.command()
    async def uptime(self, ctx):
        delta_uptime = datetime.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        embed = discord.Embed(
            title='Uptime',
            description=f'{days}d, {hours}h, {minutes}m, {seconds}s', colour=0x00B6FF)
        await ctx.send(embed=embed)

    
    @commands.command()
    async def ui(self,ctx, member:discord.Member=None) :
        if member:
         embed=discord.Embed(title=f"Userinfo für {member.display_name}", colour=0x00B6FF)
         embed.add_field(name="Name:", value=f"```{member}```")
         embed.add_field(name="Server beigetreten:", value=f"```{member.joined_at}```")
         embed.add_field(name="Discord beigetreten:", value=f"```{member.created_at}```")
         embed.add_field(name="Server beigetreten:", value=f"```{member.joined_at}```")
         embed.add_field(name="Rollen:", value=f"```{len(member.roles)-1}```")
         await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=f"Userinfo für {ctx.author.display_name}", colour=0x00B6FF)
            embed.add_field(name="Name:", value=f"```{ctx.author}```")
            embed.add_field(name="Discord beigetreten:", value=f"```{ctx.author.created_at}```")
            embed.add_field(name="Rollen:", value=f"```{len(ctx.author.roles) - 1}```")

    @commands.command()
    async def member(self, ctx):
        await ctx.send(f"Der Server hat {len(set(self.bot.users))} Member")


    @commands.command()
    async def avatar(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        embed = discord.Embed(title=f"Avatar von {member.display_name}", colour=0x00B6FF)
        embed.set_image(url=member.avatar.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def serverinfo(self, ctx):
        embed = discord.Embed(title=f"Serverinfo für {ctx.guild.name}", colour=0x00B6FF)
        embed.add_field(name="Name:", value=f"```{ctx.guild.name}```")
        embed.add_field(name="ID:", value=f"```{ctx.guild.id}```")
        embed.add_field(name="Region:", value=f"```{ctx.guild.region}```")
        embed.add_field(name="Erstellt am:", value=f"```{ctx.guild.created_at}```")
        embed.add_field(name="Beigetreten am:", value=f"```{ctx.author.joined_at}```")
        embed.add_field(name="Rollen:", value=f"```{len(ctx.guild.roles) - 1}```")
        embed.add_field(name="Mitglieder:", value=f"```{len(ctx.guild.members)}```")
        embed.add_field(name="Owner:", value=f"```{ctx.guild.owner}```")
        await ctx.send(embed=embed)

 
    @commands.command()
    async def servericon(self, ctx):
        embed = discord.Embed(title=f"Servericon für {ctx.guild.name}", colour=0x00B6FF)
        embed.set_image(url=ctx.guild.icon.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def serverid(self, ctx):
        await ctx.send(f"Die ID des Servers ist: {ctx.guild.id}")

    @commands.command()
    async def serverowner(self, ctx):
        await ctx.send(f"Der Serverowner ist: {ctx.guild.owner}")

    @commands.command()
    async def serverregion(self, ctx):
        await ctx.send(f"Die Region des Servers ist: {ctx.guild.region}")
    
    @commands.command()
    async def servermembers(self, ctx):
        await ctx.send(f"Die Mitglieder des Servers sind: {ctx.guild.members}")


    
def setup(bot):
    bot.add_cog(fun(bot))
