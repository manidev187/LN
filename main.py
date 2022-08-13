import random
import discord
import pytz
from discord.ext import commands
from discord.ext.commands import has_permissions
import datetime
from datetime import timedelta, timezone
import asyncio
from discord.ui import Button, View
from discord import Color
from discord import Member
import os
import traceback
from colorama import Fore, Back, Style
import sys
import requests


intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command("help")
token = '' # Token Einfügen
logo = "logoattachmmentlink"

# Cogs
if __name__ == '__main__':
    for filename in os.listdir('cogs'):
       if filename.endswith('.py'):
        try:
            bot.load_extension(f'cogs.{filename[:-3]}')
        except Exception as e:
            print(f'Failed to load extension .', file=sys.stderr)
            traceback.print_exc()

# IDS           
GUILD_ID = 0
TICKET_CHANNEL = 0
CATEGORY_ID = 0
TEAM_ROLE = 0
LOG_CHANNEL = 0
role_id = 0
guild_id = 0

# Verify Bot

class RoleButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="Verifizieren", # Text auf dem Button! 
            style=discord.enums.ButtonStyle.blurple, # Button-Fabre! 
            custom_id="interaction:RoleButton",
        )
    async def callback(self, interaction: discord.Interaction):
        user = interaction.user

        role = interaction.guild.get_role(role_id)

        if role is None:
            return

        if role not in user.roles:
            await user.add_roles(role)
            await interaction.response.send_message(f"🎉 Du bist nun verifiziert!", ephemeral=True)

        else:
            await interaction.response.send_message(f"❌ Du bist bereits verifiziert!", ephemeral=True)


embed = discord.Embed(
                description=f"""Reagiere mit der Nachricht um dich zu Allowlisten""",
                colour=0xFFD723) 

@commands.has_permissions(administrator=True)
@bot.command()
async def v(ctx: commands.Context): # Command
    view = discord.ui.View(timeout=None)

    view.add_item(RoleButton())

    await ctx.send(embed=embed, view=view)
    
# Dropdown Ticket Menu   

class MyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.select(
        custom_id="Customid",
        options=[
            discord.SelectOption(
                label="Button Name",
                value="Button Name"
            )
        ]
    )
    async def callback(self, select, interaction):
        if "Button Name" in interaction.data['values']:
            if interaction.channel.id == TICKET_CHANNEL:
                guild = bot.get_guild(GUILD_ID)
                for ticket in guild.channels:
                    if str(interaction.user.id) in ticket.name:
                        embed = discord.Embed(title=f"Du kannst nur ein ticket aufmachen", description=f"Hier ist dein --> {ticket.mention}", color=0xff0000)
                        await interaction.response.send_message(embed=embed, ephemeral=True)
                        return

                category = bot.get_channel(CATEGORY_ID)
                ticket_channel = await guild.create_text_channel(f"Support ticket{interaction.user.id}", category=category,
                                                                topic=f"Ticket from {interaction.user} \nUser-ID: {interaction.user.id}")

                await ticket_channel.set_permissions(guild.get_role(TEAM_ROLE), send_messages=True, read_messages=True, add_reactions=False,
                                                    embed_links=True, attach_files=True, read_message_history=True,
                                                    external_emojis=True)
                await ticket_channel.set_permissions(interaction.user, send_messages=True, read_messages=True, add_reactions=False,
                                                    embed_links=True, attach_files=True, read_message_history=True,
                                                    external_emojis=True)
                await ticket_channel.set_permissions(guild.default_role, send_messages=False, read_messages=False, view_channel=False)
                embed = discord.Embed(description=f'Welcome {interaction.user.mention}!\n'
                                                   'Hallo Lieber User,\nErläutere dein Anliegen',
                                                   color=discord.colour.Color.orange())
                await ticket_channel.send(embed=embed)


                embed = discord.Embed(description=f'📬 Ticket wurde erstellt Siehe hier --> {ticket_channel.mention}',
                                        colour=0xFFD723)

                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
    
            
@commands.has_permissions(administrator=True)            
@bot.command()
async def ticket(ctx):
    channel = bot.get_channel(TICKET_CHANNEL)
    embed = discord.Embed(title="""***Ticket Support***""", description="""***Hast du Ein anliegen?\n
Erstelle jetzt ein Ticket mit einem Klick auf den darunterliegenden Button.***""",  colour=0xFFD723)
    await channel.send(embed=embed, view=MyView())

@bot.command()
async def close(ctx):
    if "-" in ctx.channel.name:
        channel = bot.get_channel(LOG_CHANNEL)
        closed = ctx.channel.name

        fileName = f"{ctx.channel.name}.txt"
        with open(fileName, "w") as file:
            async for msg in ctx.channel.history(limit=None, oldest_first=True):
                file.write(f"- {msg.author.display_name}: {msg.clean_content}\n")

        embed = discord.Embed(
                description=f'Ticket schließt in 5 Sekunden automatisch!',
                colour=0xFFD723)
        embed2 = discord.Embed(title="Ticket Geschlossen!", description=f"Ticket-Name: {closed}\n Closed-From: {ctx.author.display_name}\n Transcript: ", color=discord.colour.Color.orange())
        file = discord.File(fileName)
        await channel.send(embed=embed2)
        await asyncio.sleep(1)
        await channel.send(file=file)       
        await ctx.send(embed=embed)
        await asyncio.sleep(5)
        await ctx.channel.delete()

# Button Ticket Menu

@bot.command()
@commands.has_permissions(administrator=True)
async def ticketmsg(ctx):
    button1 = Button(label="📩", style=discord.ButtonStyle.blurple, custom_id="Support")
    view = View()
    view.add_item(button1)
    embed = discord.Embed(description=f"""
""", title=f"🌊Wave Tickets🌊", colour=0x0764fa)
    channel = bot.get_channel(TICKET_CHANNEL)
    await channel.send(embed=embed, view=view)
    await ctx.reply("Gesendet!")

@bot.event
async def on_interaction(interaction):
    if interaction.channel.id == TICKET_CHANNEL:
        if "Support" in str(interaction.data):
            guild = bot.get_guild(GUILD_ID)
            for ticket in guild.channels:
                if str(interaction.user.id) in ticket.name:
                    embed = discord.Embed(description=f"Du kannst nur ein Ticket gleichzeitig öffnen!\nHier hast du bereits ein Ticket offen! {ticket.mention}")
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    return

            category = bot.get_channel(CATEGORY_ID)
            ticket_channel = await guild.create_text_channel(f"📩┃support-{interaction.user.id}", category=category,
                                                            topic=f"Ticket von {interaction.user} \nClient-ID: {interaction.user.id}")

            await ticket_channel.set_permissions(guild.get_role(TEAM_ROLE), send_messages=True, read_messages=True, add_reactions=False,
                                                embed_links=True, attach_files=True, read_message_history=True,
                                                external_emojis=True)
            await ticket_channel.set_permissions(interaction.user, send_messages=True, read_messages=True, add_reactions=False,
                                                embed_links=True, attach_files=True, read_message_history=True,
                                                external_emojis=True)
            embed = discord.Embed(description=f'Willkommen im Ticket {interaction.user.mention}!\n'
                                            f'Pack hier deine Frage rein!\n'
                                            f'Ticket mit `?close` schließen!',
                                color=62719)

            embed.set_author(name=f'Neues Ticket!')
            mess_2 = await ticket_channel.send(embed=embed)
            embed = discord.Embed(title="📬 | Ticket geöffnet!",
                                description=f'Dein Ticket wurde erstellt! {ticket_channel.mention}',
                                color=discord.colour.Color.green())

            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

@bot.command()
async def tadd(ctx, member : discord.Member): 
 role = discord.utils.get(ctx.guild.roles, id=0)
 if role not in ctx.author.roles: 
        await ctx.send("``Du hast keine Rechte dafür!``", delete_after=10)
        return

 if "📩┃support-" in ctx.channel.name:
    await ctx.channel.set_permissions(member, read_messages=True, send_messages=True)
    embed = discord.Embed()
    embed = discord.Embed(title="Hinzugefügt", description=f"{member} wurde Hinzugefügt", colour=0x3e4ad6)
    await ctx.channel.send(embed=embed)
    
@bot.command()
async def close(ctx):
 role = discord.utils.get(ctx.guild.roles, id=0)
 if role not in ctx.author.roles: 
        await ctx.send("``Du hast keine Rechte dafür!``", delete_after=10)
        return

 if "📩┃support-" in ctx.channel.name:
        embed = discord.Embed(
                description=f'Ticket schließt in 5 Sekunden automatisch!',
                color=16711680)
        await ctx.channel.send(embed=embed)
        await asyncio.sleep(5)
        await ctx.channel.delete()
        
        
# Youtube Im Voice Schauen

@bot.slash_command()
async def youtube(ctx):
    """Startet YT in deinem VC"""
    if ctx.author.voice != None:
        channel = ctx.author.voice.channel
        invite = await channel.create_activity_invite(discord.EmbeddedActivity.watch_together, max_age=600, reason="YT geöffnet") # Wichtigste Zeile :P 
        embed=discord.Embed(title="Youtube gestartet", description=f"[Du oder deine Freunde können diesen Link klicken um YT zu schauen]({invite.url})", color=0xbe8aff)
        embed.set_footer(text='Will expire after 600s!')
        await ctx.respond(embed=embed)
    else:
        await ctx.respond(embed=discord.Embed(description=":warning: | Du musst in einem VC sein!", color=0xff7a7a))
        
        
# Simple Giweaway

@bot.command()
async def win(ctx):
    channel = bot.get_channel(942460980489773087)

    server = bot.get_guild(942460979961270293)

    user1 = random.choice(server.members)
    
    await channel.send(f"{user1.mention}")

    embed = discord.Embed(title="Win", description=f"{user1.mention} hat gewonnen einen Kostenlosen Bot mit Ticketsystem gewonnen!", color=0xd008fc)
    embed.set_thumbnail(url="https://media.giphy.com/media/Y3qaJQjDcbJPyK7kGk/giphy.gif")
    embed.set_footer(text="Gewonnen")
    await channel.send(embed=embed)
    
    
# Showcase 
@bot.command()

async def ticketsystem(ctx):
    button = Button(label="Ticket Channel", url="https://discord.com/channels/942460979961270293/942475978200985742")

    view = View(timeout=None)
    view.add_item(button)

    
    embed = discord.Embed(title="L&N Service Präsentiert\n Wir bieten nun ein Voll Funktionierendes Ticket System an!", description="""**Funktionen**:
    > Ticket per Buttons/Selectmenu öffnen
    > Nur eine bestimmte Rolle kann das Ticket sehen und der Ersteller!
    > Ein Transkript  vom Channel wird automatisch erstellt
""", colour=0xfa0008)
    embed.add_field(name="Was bekommt ihr beim Kauf?", value="> Beim Kauf müsst ihr uns einen Bot Token schicken, oder wir erstellen einen für euch!\n> falls ihr Hilfe benötigt wird dies in dem Ticket angeboten!")
    embed.add_field(name="Preis", value="> 5€ (LIFETIME)", inline=False)
    embed.add_field(name="Interessiert?", value="> Dann klick unten auf Ticket Kanal und Erstell in der Jeweiligen Kanal ein Ticket")
    embed.set_footer(text="Copyright © 2022 L&N Services™ - All Rights Reserved")
    embed.set_author(name="L&N Services™", icon_url=logo)

    

    await ctx.send(embed=embed, view=view)
    await ctx.send("https://cdn.discordapp.com/attachments/962707012339245146/990710437207232542/bot2.png")
    await ctx.send("https://cdn.discordapp.com/attachments/962707012339245146/990710437433704488/bot1.png")
    await ctx.send("https://cdn.discordapp.com/attachments/962707012339245146/990711601747357826/unknown.png")



@bot.command()
async def welcome(ctx):
    await ctx.channel.purge(limit=4)
    button = Button(label="Ticket Channel", url="https://discord.com/channels/942460979961270293/942475978200985742")

    view = View(timeout=None)
    view.add_item(button)

    
    embed = discord.Embed(title="L&N Service Präsentiert\n Wir bieten nun ein Voll Funktionierendes Willkommen/verlassen System an! NUR IM KAUF VON EINEM BOT ENTNHALTEN", description="""**Funktionen**:
    > Wenn jemand deinen Discord Betritt bekommt der jenige einen Rang und eine Privat Nachricht und auch in deinem
> Discord wird eine Nachricht versendet!
> Wenn jemand dein Server Verlässt wirst du in einen eingestellen Kanal eine Nachricht bekommen!
""", colour=0xfa0008)
    embed.add_field(name="Was bekommt ihr beim Kauf?", value="> beim Kauf erhaltet ihr den gesamten Code!\n> falls ihr Hilfe benötigt wird dies in dem Ticket angeboten!", inline=False)

    embed.add_field(name="Interessiert?", value="> Dann klick unten auf Ticket Kanal und Erstell in der Jeweiligen Kanal ein Ticket", inline=False)
    embed.set_footer(text="Copyright © 2022 L&N Services™ - All Rights Reserved")
    embed.set_author(name="L&N Services™", icon_url=logo)

    

    await ctx.send(embed=embed, view=view)
    await ctx.send("https://cdn.discordapp.com/attachments/962707012339245146/992843181899124866/unknown.png")
    await ctx.send("https://cdn.discordapp.com/attachments/962707012339245146/992843272449962094/unknown.png")



@bot.command()
async def everyone(ctx):
    await ctx.channel.purge(limit=1)
    await ctx.send("<@everyone>")
    await ctx.channel.purge(limit=1)

@bot.command()
async def unserebots(ctx):
    await ctx.channel.purge(limit=1)
    embed = discord.Embed(title="L&N Service Präsentiert", description="In Folgender übersicht seht ihr auf welchen Servern unsere Bots sind!\n ", colour=0xfa0008)
    embed.add_field(name="Eddilaxx [892 Mitglieder]", value="[Server](https://discord.gg/JyR89mVtVf)")
    embed.add_field(name="Kratzeis Fivem Stuff [616 Member]", value="[Server](https://discord.gg/4pPRjdnz99)", inline=False)
    embed.add_field(name="Epicmoddz [242 Member]", value="[Server](https://discord.gg/GfmK5jPxPa)", inline=False)
    embed.add_field(name="DinaLive [143 Member]", value="[Server](https://discord.gg/uDmD7WnH2C)", inline=False)
    embed.add_field(name="MagentaCity [72 Member]", value="[Server](https://discord.gg/YCQSkxPV)", inline=False)
    embed.add_field(name="Compton Crimelife [87 Member]", value="[Server](https://discord.gg/3H3dXyBe)", inline=False)
    embed.add_field(name="NastyCrimelife [62 Member]", value="[Server](https://discord.gg/jTbjBgt8Cz)", inline=False)
    embed.add_field(name="Majestic-V [51 Member]", value="[Server](https://discord.gg/CpjsTGr3pT)", inline=False)
    embed.add_field(name="Nex-Scripts [34 Member]", value="[Server](https://discord.gg/624rdJdFvV)", inline=False)



    embed.set_footer(text="Copyright © 2022 L&N Services™ - All Rights Reserved - Stand 28.06.2022")
    embed.set_author(name="L&N Services™", icon_url=logo)
    
    await ctx.send(embed=embed)
@bot.command()
async def paket1(ctx):
    button = Button(label="Hier Kaufen", url="https://discord.com/channels/942460979961270293/942475978200985742")

    view = View(timeout=None)
    view.add_item(button)

    embed = discord.Embed(title="L&N Paket 1", description="""**Information**
    Dies ist das erste Paket von L&N Services.""", colour=0xfc0000)



    embed.set_footer(text="©L&N Services")
    embed.set_thumbnail(url=logo)
    embed.set_author(name="L&N Services", icon_url=logo)
    await ctx.send(embed=embed, view=view)

@bot.command()
async def design(ctx):

    button = Button(label="Ticket Channel", url="https://discord.com/channels/942460979961270293/942475978200985742")

    view = View(timeout=None)
    view.add_item(button)

    embed = discord.Embed(title="Design", description="""Statisches Logo 5 €
Animiertes Logo 10 €
Discord Banner 5€
Custom Design per Ticket""", colour=0xfc0000)
    embed.set_author(name="L&N Services", icon_url=logo)
    embed.set_footer(text="©L&N Services")
    await ctx.send(embed=embed, view=view)

# Apps

@bot.message_command(name=f"Errinerung", guild=[0]) 
async def App(ctx, message: discord.Member): 
    await asyncio.sleep(120)
    await ctx.respond(f"{ctx.author.mention} ich errinere dich", ephemeral=False)
    
# Random Memes

@bot.slash_command(name = 'meme', description = 'Hollt n random meme')
async def meme(ctx):
    async def delete_msg(inter):
        if not inter.user == ctx.author:
            embed=discord.Embed(description=":warning: | Du hast das Menü nicht erstellt!", color=0xff7070)
            await inter.response.send_message(embed=embed, ephemeral=True)
            return
        await inter.message.delete()
    async def anoth(inter):
        if not inter.user == ctx.author:
            embed=discord.Embed(description=":warning: | Du hast das Menü nicht erstellt!", color=0xff7070)
            await inter.response.send_message(embed=embed, ephemeral=True)
            return
        embed = epic_meme()
        await inter.response.edit_message(embed=embed)
    view = View()
    anotherone = Button(label="Noch einen!", emoji="👍", style=discord.ButtonStyle.blurple)
    exit = Button(label="Löschen")
    anotherone.callback = anoth
    exit.callback = delete_msg
    view.add_item(anotherone)
    view.add_item(exit)
    embed = epic_meme()
    await ctx.respond(embed=embed, view=view)

def epic_meme():
    listreddit = ['memes', 'dankmemes']
    subreddit = random.choice(listreddit)
    count = 1
    timeframe = 'day' # Hier alle timeframes: hour, day, week, month, year, all
    listing = 'random' # Themen: controversial, best, hot, new, random, rising, top

    def get_reddit(subreddit,count):
        try:
            base_url = f'https://www.reddit.com/r/{subreddit}/{listing}.json?count={count}&t={timeframe}'
            request = requests.get(base_url, headers = {'User-agent': 'yourbot'})
        except:
            print('Ein Fehler ist aufgetreten!')
        return request.json()
    
    top_post = get_reddit(subreddit,count)
    

    title = top_post[0]['data']['children'][0]['data']['title']
    url = top_post[0]['data']['children'][0]['data']['url']
    ups = top_post[0]['data']['children'][0]['data']['ups']
    embed=discord.Embed(title=f":rofl: | {title}", color=discord.Color.random())
    embed.set_image(url=url)
    embed.set_footer(text=f"r/{subreddit} >> {ups} Upvotes")
    return embed



def getstatus(m):
    if str(m.status) == "dnd":
        return "do not disturb"
    return m.status

# Info

@bot.command()
async def info(ctx, member: discord.Member):

    if member is None:
        member = ctx.author

    # Calculating time since the user created his discord account using the member.created_at method
    c_delta = datetime.utcnow() - member.created_at
    c_ago = datetime.fromtimestamp(c_delta.seconds, tz=timezone.utc).strftime("%H:%M:%S")
    c_at = member.created_at.strftime("%c")

    # Getting join position by sorting the guild.members list with the member.joined_at method
    join_pos = sorted(ctx.guild.members, key=lambda member: member.joined_at).index(member) + 1
    
    # Defining discord.Embed instance
    embed = discord.Embed(title=f"{member.name}#{member.discriminator}", timestamp=datetime.utcnow(), colour=0x000)
    
    # Adding fields to the embed
    embed.add_field(name="Status:", value=getstatus(member), inline=True)
    embed.add_field(name="Guild name:", value=member.display_name, inline=True)
    embed.add_field(name="Join position:", value=f"{join_pos}/{len(ctx.guild.members)}", inline=True)

    embed.add_field(name="Created at:", value=f"{c_at}\n({c_delta.days} days, {c_ago} ago)", inline=True)
    embed.add_field(name="ID:", value=member.id, inline=True)
    embed.add_field(name="Bot:", value="✅ Yes" if member.bot else "❌ No", inline=True)
    
    # Setting the thumbnail as the users profile picture
    embed.set_thumbnail(url=member.avatar_url)
    
    # Setting a footer
    embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)

    await ctx.send(embed=embed)
      
#warnings

@bot.event
async def on_guild_join(guild):
    bot.warnings[guild.id] = {}

@bot.command()
@commands.has_permissions(administrator=True)
async def warn(ctx, member: discord.Member=None, *, reason=None):
    guild = bot.get_guild(991006129368760330) # "991006129368760330" mit euerer Server ID ersetzen!
    if member is None:
        return await ctx.send("**Das angegebene Mitglied konnte nicht gefunden werden oder du hast vergessen, einen anzugeben.**")
        
    if reason is None:
        return await ctx.send("**Bitte gebe einen Grund für die Warnung dieses Mitglieds an.**")

    try:
        first_warning = False
        bot.warnings[ctx.guild.id][member.id][0] += 1
        bot.warnings[ctx.guild.id][member.id][1].append((ctx.author.id, reason))

    except KeyError:
        first_warning = True
        bot.warnings[ctx.guild.id][member.id] = [1, [(ctx.author.id, reason)]]

    count = bot.warnings[ctx.guild.id][member.id][0]

    async with aiofiles.open(f"{ctx.guild.id}.txt", mode="a") as file:
        await file.write(f"{member.id} {ctx.author.id} {reason}\n")

    embed=discord.Embed(description=f"**Grund:** {reason}", color=0xEE00EE)
    embed.set_author(name=f'{member.display_name}#{member.discriminator} wurde gewarnt', icon_url=member.display_avatar)
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def warns(ctx, member: discord.Member=None):
    if member is None:
        return await ctx.send("Das angegebene Mitglied konnte nicht gefunden werden oder du hast vergessen, einen anzugeben.")
    
    embed = discord.Embed(title=f"**Warnungen von {member.name}**", description="", color=0xfa1302)
    try:
        i = 1
        for admin_id, reason in bot.warnings[ctx.guild.id][member.id][1]:
            admin = ctx.guild.get_member(admin_id)
            embed.description += f"**Warnung {i} von:** {admin.mention} **Grund:** `{reason}`\n"
            i += 1

        await ctx.send(embed=embed)

    except KeyError: 
        await ctx.send("Dieses Mitglied hat keine Warnungen!")
    
bot.run(token)