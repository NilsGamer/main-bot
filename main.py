import asyncio

import os

import discord
from discord import Member

client = discord.Client()

@client.event
async def on_ready():
    print('Login User: {}'.format(client.user.name))
    client.loop.create_task(status_task())

@client.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name="wilkommen")
    await channel.send(f"**Wilkommen** {member.mention} \nUser: {len(list(member.guild.members))")
    role = discord.utils.get(member.guild.roles, name="Member")
    await member.add_roles(role)

async def status_task():
    while True:
        await client.change_presence(activity=discord.Game('mache /? um die Hilfeliste anzuzeigen'), status=discord.Status.online)
        await asyncio.sleep(4)
        await client.change_presence(activity=discord.Game('Coded by NilsGamer'), status=discord.Status.online)
        await asyncio.sleep(3)
        await client.change_presence(activity=discord.Game('bei Fragen  schreib mich auf Insta per dm an linktr.ee/nilsgamer'), status=discord.Status.online)
        await asyncio.sleep(5)

def is_not_pinned(mess):
    return not mess.pinned

@client.event
async def on_message(message):
    if message.author.bot:
        return
    if "/?" in message.content:
        await message.channel.send("**Liste der Befehle**\r\n"
                                   "**/?** zeigt dir die Befehle an\r\n"
                                   "**/clear (anzahl)**löscht die Nachrichten (only Admin)\r\n"
                                   "**/userinfo** zeigt eine Info über den User\r\n"
                                   "**/addGlobal** der aktuelle Textchannel wird zum Globalchat\r\n"
                                   "**/say** gibt deinNachricht wieder\r\n"
                                   "**/caps** Gibt deine NAchricht in Caps wieder\r\n"
                                   "**/kill (user)** killt den ausgewählten User\r\n"
                                   "**/play (link von YouTube)** spielt im einem Sprachchennel die ausgewählte Musik")

    if message.content.startswith('/userinfo'):
        args = message.content.split(' ')
        if len(args) == 2:
            member: Member = discord.utils.find(lambda m: args[1] in m.name, message.guild.members)
            if member:
                embed = discord.Embed(title='Userinfo für {}'.format(member.name),
                                      description='Dies ist die Userinfo für den User {}'.format(member.mention),
                                      color=0x22a7f0)
                embed.add_field(name='Server beigetreten', value=member.joined_at.strftime("%m/%d/%Y, %H:%M:%S"),
                                inline=True)
                embed.add_field(name='Discord beigetreten', value=member.created_at.strftime("%m/%d/%Y, %H:%M:%S"),
                                inline=True)
                rollen = ''
                for role in member.roles:
                    if not role.is_default():
                        rollen += '{} \r\n'.format(role.mention)
                if rollen:
                    embed.add_field(name='Rollen', value=rollen, inline=True)
                embed.set_thumbnail(url=message.author.avatar_url)
                embed.set_footer(text='Ich bin ein EmbedFooter!')
                message = await message.channel.send(embed=embed)
                await message.add_reaction('🚍')
                await message.add_reaction('a:tut_herz:662606955520458754')

    if message.content.startswith('/clear'):
        if message.author.permissions_in(message.channel).manage_messages:
            args = message.content.split(' ')
            if len(args) == 2:
                if args[1].isdigit():
                    count = int(args[1]) + 1
                    deleted = await message.channel.purge(limit=count, check=is_not_pinned)
                    await message.channel.send('{} Nachrichten gelöscht.'.format(len(deleted) - 1))

    if message.content.startswith("/creator"):
        await message.channel.send("**Der Bot wurde von NilsGamer erstellt**\r\n"
                                   "Weitere Informationen: https://linktr.ee/nilsgamer")

client.run(os.environ["token"])
