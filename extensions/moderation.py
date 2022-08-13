import asyncio
import discord
from discord.ext import commands
from datetime import datetime, timedelta
from discord.utils import get

GUILD = "L&N Services™"

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Events sind bei cogs "listener"
    @commands.Cog.listener()
    async def on_ready(self):
        print('* Die Erweiterung \'Moderation\' wurde erfolgreich eingebunden...')

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.pinned:
            return
        if message.author.bot:
            return
        if message.channel.id == 964656829802110996:
            await asyncio.sleep(1)
            await message.delete()
            channel = self.bot.get_channel(964656829802110996)
            embed = discord.Embed(title=f"{message.author}", description=f"{message.content}", colour=0x00B6FF,
                                  timestamp=datetime.now())
            embed.set_thumbnail(url=message.author.avatar.url)
            testmessage = await channel.send(embed=embed)
            await testmessage.add_reaction("✅")
            await testmessage.add_reaction("❌")
            return
        bad_words = ["nigger", "bastard", "hurrensohn", "huan", "knecht", "leck", "ahole", "anus", "ashole",
                             "assholz", "bitch", "blowjob", "bastards", "cock", "nigga", "hurensohn",
                             "fick deine toten", "deine toten", "nuttensohn", "discord.gg"]
        for words in bad_words:
            if words in message.content.lower().split(" "):
                await message.delete()
                bad_word_embed = discord.Embed(title="Bad Word",
                                               description=f"{message.author.mention}, bitte Achte auf deine Wortwahl",
                                               colour=0x00B6FF)

                await message.channel.send(embed=bad_word_embed, delete_after=5.0)
                
        if message.channel.id == 943218112948486215: # Channel ID einfügen für Auto-Delete! 
            await asyncio.sleep(360)
            await message.delete()

        if message.content.startswith("n2nyd"):
            guild: discord.Guild = self.bot.get_guild(942460979961270293)

            role: discord.Role = guild.get_role(942477398157455442)
            await message.author.add_roles(role, reason="Zuweisung")

        if message.channel.id == 951959501039366184:
            await asyncio.sleep(60)
            await message.delete()
        
        # Dieser Prozess wird glaub ich nur bei standalone Bots und der Main Datei gebraucht.
        #await self.bot.process_commands(message)

    @commands.command()
    async def ban(self, ctx, member: discord.Member = None, *, reason=None):
        role = discord.utils.get(ctx.guild.roles, id=942460980124872726)
        if role not in ctx.author.roles:
            await ctx.send("Du hast keine Rechte dafür!", delete_after=10)
            return
        if member is None:
            await ctx.send("Es wurde kein Member angegeben")
            return
        await member.send(f"Du wurdest von {GUILD} gebannt für `{reason}`")
        await member.ban(reason=reason)
        embed = discord.Embed(title="Erfolgreich gebannt",
                              description=f"{member.mention} wurde gebannt\nGrund: {reason} ",
                              colour=discord.Colour.red())
        await ctx.send(embed=embed)
        


    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.send(f'Member is not found')

    @commands.command()
    async def unban(self, ctx, user: discord.User):
        role = discord.utils.get(ctx.guild.roles, id=942460980124872726)

        if role not in ctx.author.roles:
            await ctx.send("Du hast keine Rechte dafür!", delete_after=10)
            return

        guild = ctx.guild
        mbed = discord.Embed(
            title='Erfolgreich!',
            description=f"{user} wurde erfolgreich.", colour=0x00B6FF
        )
        if ctx.author.guild_permissions.ban_members:
            await ctx.send(embed=mbed)
            await guild.unban(user=user)

    @commands.command()
    async def kick(self, ctx, member: discord.Member = None, *, reason=None):
        role = discord.utils.get(ctx.guild.roles, id=942460980124872726)
        if role not in ctx.author.roles:
            await ctx.send("Du hast keine Rechte dafür!", delete_after=10)
            return
        if member is None:
            await ctx.send("Es wurde kein Member angegeben")
            return
        if reason is None:
            await ctx.send(f"Du solltest noch eine Begründung angeben um den User {member.mention} zu kicken")
            return
        embed = discord.Embed(title="Erfolgreich gekickt",
                              description=f"Ich habe für dich {member.mention} gekickt\nGrund: {reason}",
                              colour=0x00B6FF)
        await ctx.send(embed=embed)
        await member.kick(reason=reason)

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.send(f'Member is not found')

    @commands.command()
    async def ping(self, ctx):
        await ctx.message.delete()
        embed = discord.Embed(title="Ping", description=f"Pong 🏓  **{round(self.bot.latency * 1000)}ms**",
                              colour=0x00B6FF)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Moderation(bot))