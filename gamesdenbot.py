# Games Den Bot v0.1
# small bot for Games Den discord server

import discord
from discord.ext import commands
from discord.utils import get

import os
import dotenv
from dotenv import load_dotenv

import random
from dnd_dice_roller import parse_dice_rolls

# load up attributes from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('DISCORD_SERVER')
CURSE_STRING = os.getenv('CURSE_WORDS')
CURSE_WORDS = CURSE_STRING.split(', ')

# specific channel / message ids: change based on your server
GREETING_CHANNEL = int(os.getenv('GREETING_CHANNEL'))
BOT_LOG_CHANNEL = int(os.getenv('BOT_LOG_CHANNEL'))
ROLE_MESSAGE = int(os.getenv('ROLE_MESSAGE'))

client = commands.Bot(command_prefix = '!')


# list of roles
roles = {
'🖌️': 'Artist',
'🖥️': 'Programmer',
'📝': 'Writer',
'🎵': 'Audio',
'👔': 'Producer',
'⚔️': 'Looking for D&D',
'🎲': 'Board Games'
}
role_emoji_list = roles.keys()

@client.event
async def on_ready():
    # find the servers bot is connected to, and print their names and ids
    for guild in client.guilds:
        if guild.name == SERVER:
            break

    print(f'{client.user} has connected to Discord:\n'
        f'{guild.name}(id: {guild.id})'
    )
# greeting message when member joins server
@client.event
async def on_member_join(member):
    channel = client.get_channel(GREETING_CHANNEL)
    await channel.send(f'Welcome {member.mention}! Be sure to check out #rules-and-info and enjoy your stay in the Games Den!')

# leaving message when member leaves server
@client.event
async def on_member_remove(member):
    channel = client.get_channel(BOT_LOG_CHANNEL)
    await channel.send(f'Bye Bye {member.name} . . .')

# don't let them say that
@client.event
async def on_message(message):
    content = message.content.lower()
    server = client.guilds[0]
    log = get(server.channels, id=BOT_LOG_CHANNEL)
    # if the channel isn't nsfw, ask users to edit their message and post a log message
    if not message.channel.is_nsfw() and message.channel != log:
        for curse in CURSE_WORDS:
            if curse in content:
                await message.channel.send('Hey do not say that please edit ur message')
                await log.send(
                f"Posted warning for {message.author}'s message: \n"
                f"```{content}```")
                break
    await client.process_commands(message)

# error handling for commands not existing
@client.event
async def on_command_error(message, error):
    if isinstance(error, commands.CommandNotFound):
        await message.channel.send('Error: Command does not exist')

# assign roles based on reaction to specific message
# note: on_raw_reaction_add is used rather than on_reaction_add to avoid issues with the bot forgetting all messages before it is turned on
@client.event
async def on_raw_reaction_add(payload):
    # collect info from the payload
    message_id = payload.message_id
    server = client.guilds[0]
    # only check the emotes on one specific message
    if message_id == ROLE_MESSAGE:
        emoji = payload.emoji.name
        member = server.get_member(payload.user_id)
        if emoji in role_emoji_list:
            if member:
                role = get(server.roles, name=roles[emoji])
                await member.add_roles(role)

@client.event
async def on_raw_reaction_remove(payload):
    # collect info from the payload
    message_id = payload.message_id
    server = client.guilds[0]
    # only check the emotes on one specific message
    if message_id == ROLE_MESSAGE:
        emoji = payload.emoji.name
        member = server.get_member(payload.user_id)
        if emoji in role_emoji_list:
            if member:
                role = get(server.roles, name=roles[emoji])
                await member.remove_roles(role)

# test of commands
@client.command()
async def uwu(ctx):
    await ctx.channel.send('owo')

@client.command()
async def roll(ctx):
    result = parse_dice_rolls(ctx.message.content[6:])
    await ctx.channel.send(result)
client.run(TOKEN)
