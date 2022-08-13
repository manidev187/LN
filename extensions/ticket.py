import discord
from discord.ext import commands
from discord.commands import slash_command

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener('on_ready')
    async def ticketlistener(self):
        self.bot.add_view(CreateMenu())
        self.bot.add_view(TicketMenu())
    
    ###Guild ID´s ###
    @slash_command(guild_ids=[942460979961270293])
    async def ticket_setup(self, ctx: commands.Context, channel: discord.Option(discord.TextChannel, "Select a channel", required=False)):
        """Setup the Ticket System"""
        panel = discord.Embed(title="Ticket System", description="To create a ticket, react with `📨 Create a Ticket`", colour=discord.Color.light_gray())
        if ctx.guild.icon is not None:
            panel.set_thumbnail(url=ctx.guild.icon.url)
            panel.set_footer(text="Made by ﾉ刀ｲ乇ｲ乙ひ#2144", icon_url=ctx.guild.icon.url)
        else:
            panel.set_footer(text="Made by ﾉ刀ｲ乇ｲ乙ひ#2144")
        if channel is None:
            await ctx.respond(embed=panel, view=CreateMenu())
        else:
            await channel.send(embed=panel, view=CreateMenu())

class CreateMenu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.roles = [942461967774388224] ### Staff roles ID´s ###
    
    @discord.ui.button(label="Create a Ticket", style=discord.ButtonStyle.gray, emoji="📨", custom_id="CreateTicket")
    async def create_callback(self, button: discord.Button, interaction: discord.Interaction):

        category = discord.utils.get(interaction.guild.categories, id=943392214531317760) ### Ticket Category ID ###
        member = interaction.user
        await interaction.response.defer(ephemeral=True)
        channel = await category.create_text_channel(name=member.display_name, topic=f"Ticket from {member.mention}", reason="Ticket Support")
        await channel.set_permissions(member, view_channel = True, send_messages = True,  read_messages=True)
        staffroles = [interaction.guild.get_role(i) for i in self.roles]
        staffroles_mention = " ".join([i.mention for i in staffroles])
        for i in staffroles:
            await channel.set_permissions(i, view_channel=True, send_messages = True, read_messages=True)
        await channel.set_permissions(interaction.guild.default_role, view_channel = False)
        await interaction.followup.send(content=f"Your Ticket was created in {channel.mention}", ephemeral=True)
        await channel.send(f"{staffroles_mention}\n\n{member.mention} here is your Ticket", view=TicketMenu())

        staffchannel = interaction.guild.get_channel(956331477262540830)
        await staffchannel.send(content=f"{staffroles_mention}\n\n{member.mention} has created a ticket\n\nChannel: {channel.mention}")
    
class TicketMenu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.roles = [942461967774388224] ### Staff roles ID´s ###
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        member = interaction.user
        for i in member.roles:
            if i.id in self.roles:
                return True
        if i.id not in self.roles:
            await interaction.response.send_message(content="You don't have permission to do this", ephemeral=True)
            return False
    
    @discord.ui.button(label="Close", style=discord.ButtonStyle.gray, emoji="❌", custom_id="CloseTicket")
    async def close_callback(self, button: discord.Button, interaction: discord.Interaction):
        await interaction.channel.delete()
    
    @discord.ui.button(label="Claim", style=discord.ButtonStyle.gray, emoji="📑", custom_id="ClaimTicket")
    async def claim_callback(self, button: discord.Button, interaction: discord.Interaction):
        author = interaction.user
        staffroles = [interaction.guild.get_role(i) for i in self.roles]
        channel = interaction.guild.get_channel(interaction.channel_id)
        for i in staffroles:
            await channel.set_permissions(i, view_channel = False, send_messages=False)
        await channel.set_permissions(author, send_messages = True, read_messages=True, view_channel=True)

        await channel.send(content=f"The ticket was claimed by {author}")
        button.disabled = True
        await interaction.response.edit_message(view=self)
            
def setup(bot):
    bot.add_cog(Tickets(bot))