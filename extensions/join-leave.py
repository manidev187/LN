import asyncio
import discord
from discord.ext import commands
from discord.utils import get 
from datetime import datetime, timedelta
import mysql.connector
from discord.ui import Button, View


class joinleave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('* Die Erweiterung \'join-leave\' wurde erfolgreich eingebunden...')


    
    @commands.Cog.listener()
    async def on_member_join(self, member):


        ROLE = 'Member'
        role = get(member.guild.roles, name=ROLE)
        await member.add_roles(role)

        GUILD = member.guild
        member_count = len(member.guild.members) # includes bots
        join = self.bot.get_channel(942549730024640532)
        embed = discord.Embed(title="Willkommen", description=f"Herzlich Willkommen {member.mention} auf {GUILD}. Wir wünschen dir viel Spaß\nNeuer Membercount: {member_count}" ,colour=0xfa0008)

        embed.set_footer(text="Copyright © 2022 L&N Services™ - All Rights Reserved")
        embed.set_author(name="L&N Services™", icon_url="https://cdn.discordapp.com/attachments/962707012339245146/990677652870430860/LN.png")
        await join.send(embed=embed)


    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
     if after.channel != None:
        if after.channel.id == 942460980800159807:
            for guild in self.bot.guilds:
                maincategory = discord.utils.get(
                    guild.categories, id=942460980653326380)
                channel2 = await guild.create_voice_channel(name=f'🔊 | {member.display_name}', category=maincategory)
                await channel2.set_permissions(member, connect=True, manage_channels=True, move_members=True)                
                await member.move_to(channel2)

                def check(x, y, z):
                    return len(channel2.members) == 0
                await self.bot.wait_for('voice_state_update', check=check)
                await channel2.delete()



    


def setup(bot):
    bot.add_cog(joinleave(bot))