import discord
from discord.ext import commands
from discord.utils import get 

class reactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('* Die Erweiterung \'reactions\' wurde erfolgreich eingebunden...') 
    
    #@commands.Cog.listener()
    #async def on_raw_reaction_add(self, payload):
        #if payload.channel_id == 957498495017816074:
            #if payload.message_id == 957592403865378836:
                #guild: discord.Guild = self.bot.get_guild(952261006053245028)

                #role: discord.Role = guild.get_role(952261006053245031)
                #await payload.member.add_roles(role, reason="Zuweisung")


        

def setup(bot):
    bot.add_cog(reactions(bot))