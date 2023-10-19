import datetime
import humanfriendly
import nextcord
from nextcord.ext import commands
import os

import Tickets, EmbedCreator, Logs

from nextcord import Intents, File, ButtonStyle, Embed, Color, SelectOption, Interaction, SlashOption

intents = Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
serverId = os.environ["SERVER_ID"]
color_class = [Color.blue(), Color.red(), Color.green(), Color.magenta(), Color.dark_magenta(), Color.dark_grey(),
               Color.dark_green(), Color.dark_gold(), Color.orange(), Color.purple()]
endTicketImage = ""
roleName = ""
welcomeImage = ""
welcomeMessage = ""
goodbyeMessage = ""
goodbyeImage = ""
welcomeChannel = ""
goodbyeChannel = ""
messageLogs = ""
punishmentLogs = ""
creatorId = 991043009070125166


@bot.slash_command(guild_ids=[int(serverId)])
async def test(interaction: Interaction):
    model = Tickets.EndReason()
    await interaction.response.send_modal(model)


@bot.slash_command(guild_ids=[int(serverId)])
async def bot_config(interaction: Interaction, mod_role: str = "", welcome_image: str = "", welcome_channel: str = "",
                     goodbye_image: str = "", goodbye_channel: str = "", message_logs: str = "",
                     punishment_logs: str = "", end_ticket_image: str = "", welcome_message: str = "",
                     goodbye_message: str = ""):
    global creatorId
    if interaction.user.id == interaction.guild.owner_id or interaction.user.id == creatorId:
        global roleName, endTicketImage, welcomeImage, welcomeChannel, goodbyeMessage, \
            goodbyeImage, goodbyeChannel, messageLogs, punishmentLogs, welcomeMessage
        print(mod_role)
        if mod_role:
            roleName = mod_role

        if welcome_image:
            welcomeImage = welcome_image

        if welcome_channel:
            welcomeChannel = welcome_channel.replace("#", "").replace("<", "").replace(">", "")

        if goodbye_image:
            goodbyeImage = goodbye_image

        if goodbye_channel:
            goodbyeChannel = goodbye_channel.replace("#", "").replace("<", "").replace(">", "")

        if message_logs:
            messageLogs = message_logs.replace("#", "").replace("<", "").replace(">", "")

        if punishment_logs:
            punishmentLogs = punishment_logs.replace("#", "").replace("<", "").replace(">", "")

        if end_ticket_image:
            endTicketImage = end_ticket_image

        if welcome_message:
            welcomeMessage = welcome_message

        if goodbye_message:
            goodbyeMessage = goodbye_message
        await interaction.response.send_message("Config has been set successfully")
    else:
        await interaction.response.send_message("You do not have permission to use this command")


@bot.slash_command(guild_ids=[int(serverId)])
async def create_ticket(interaction: Interaction,
                        color: int = SlashOption(name="color", choices={"Blue": 0, "Red": 1, "Green": 2, "Pink": 3,
                                                                        "Magenta": 4, "Gray": 5, "Dark green": 6,
                                                                        "Gold": 7, "Orange": 8, "Purple": 9}),
                        title: str = "", body: str = "", image: str = "",
                        thumbnail: str = "", footer: str = ""):
    global roleName
    global creatorId
    for i in interaction.guild.roles:
        if i.name == roleName or interaction.user.id == interaction.guild.owner_id or interaction.user.id == creatorId:
            ender = False
            if i in interaction.user.roles or interaction.user.id == interaction.guild.owner_id:

                colorFinal = color_class[color]

                body = body.replace("%n", f'\n')
                ticket = Tickets.CreateTicketMenu()
                ticket.createEmbed(colorFinal, title, body, image, thumbnail, footer)

                await ticket.start(interaction=interaction)

            else:
                await interaction.response.send_message("No permission")
            break
    if ender:
        await interaction.response.send_message("No permission")


@bot.slash_command(guild_ids=[int(serverId)])
async def create_embed(interaction: Interaction,
                       color: int = SlashOption(name="color", choices={"Blue": 0, "Red": 1, "Green": 2, "Pink": 3,
                                                                       "Magenta": 4, "Gray": 5, "Dark green": 6,
                                                                       "Gold": 7, "Orange": 8, "Purple": 9}),
                       title: str = "", body: str = "", image: str = "",
                       thumbnail: str = "", footer: str = ""):
    try:
        colorFinal = color_class[color]

        body = body.replace("%n", f'\n')

        embed = EmbedCreator.createEmbed(colorFinal, title, body, image, thumbnail, footer)

        await interaction.response.send_message(embed=embed)

    except:
        print("something went wrong")


@bot.slash_command(guild_ids=[int(serverId)])
async def punishment(interaction: Interaction, user_id: str,
                     type: int = SlashOption(name="punishment", choices={"Mute": 0, "Kick": 1, "Ban": 2, "Un-ban": 3,
                                                                         "Un-mute": 4}),
                     reason: str = "", mute_duration: str = "12h"):
    global roleName
    global creatorId
    for i in interaction.guild.roles:
        if i.name == roleName or interaction.user.id == interaction.guild.owner_id or interaction.user.id == creatorId:
            ender = False
            if i in interaction.user.roles or interaction.user.id == interaction.guild.owner_id:

                time = humanfriendly.parse_timespan(mute_duration)

                print(time)
                finalID = await interaction.client.fetch_user(user_id)
                memberList = interaction.guild.members
                try:
                    if type == 0:
                        for i in memberList:

                            if i.id == finalID.id:
                                await i.edit(timeout=nextcord.utils.utcnow() + datetime.timedelta(seconds=time))
                                await interaction.response.send_message(f'User {i.name} has been muted for {time}')
                    elif type == 1:
                        mute_duration = ''
                        await interaction.guild.kick(finalID, reason=reason)
                        await interaction.response.send_message(f'User {finalID.name} has been kicked for {reason}')
                    elif type == 2:
                        mute_duration = ''
                        await interaction.guild.ban(finalID, delete_message_seconds=None, delete_message_days=7,
                                                    reason=reason)
                        await interaction.response.send_message(f'User {finalID.name} has been banned for {reason}')
                    elif type == 3:
                        mute_duration = ''
                        await interaction.guild.unban(finalID, reason=reason)
                        await interaction.response.send_message(f'User {finalID.name} has been un-banned for {reason}')
                    elif type == 4:
                        mute_duration = ''
                        for i in memberList:

                            if i.id == finalID.id:
                                await i.edit(timeout=nextcord.utils.utcnow() + datetime.timedelta(seconds=1))
                                await interaction.response.send_message(f'User {i.name} has been un-muted')
                    else:
                        await interaction.response.send_message("Something went wrong")

                    for i in interaction.guild.channels:
                        global punishmentLogs
                        if i.id == int(punishmentLogs):
                            channel = i
                    await channel.send(embed=Logs.punishment_log(type, finalID, reason, mute_duration))
                except:
                    print("Something went wrong")
                else:
                    await interaction.response.send_message("No permission")
                break
    if ender:
        await interaction.response.send_message("No permission")


@bot.event
async def on_ready():
    print(f'logged in as {bot.user.name} ({bot.user.id})')
    print("....................................")


@bot.event
async def on_message(msg):
    print(msg)
    print(msg.content)


@bot.event
async def on_message_delete(msg):
    if not msg.author.bot:
        global messageLogs
        for i in msg.guild.channels:
            if i.id == int(messageLogs):
                channel = i
        await channel.send(embed=Logs.message_log(0, msg))


@bot.event
async def on_message_edit(before, after):
    if not before.author.bot and before.lower() != after.lower():
        global messageLogs
        for i in before.guild.channels:
            if i.id == int(messageLogs):
                channel = i
        msg = (before, after)
        await channel.send(embed=Logs.message_log(1, msg))


@bot.event
async def on_member_join(member):
    if not member.bot:
        global welcomeChannel, welcomeImage, welcomeMessage
        embed = EmbedCreator.createEmbed(Color.magenta(), f'Welcome to {member.guild.name}', welcomeMessage,
                                         welcomeImage, "", "")
        for i in member.guild.channels:

            if i.id == int(welcomeChannel):
                print("in if")
                channel = i
                await channel.send(f'{member.mention}', embed=embed)


@bot.event
async def on_member_remove(member):
    if not member.bot:
        global goodbyeChannel, goodbyeImage, goodbyeMessage
        embed = EmbedCreator.createEmbed(Color.magenta(), f'User {member.name.mention} has left', goodbyeMessage,
                                         goodbyeImage, "", "")
        for i in member.guild.channels:

            if i.id == int(goodbyeChannel):
                print("in if")
                channel = i
                await channel.send(f'{member.mention}', embed=embed)


bot.run(os.environ["DISCORD_TOKEN"])
