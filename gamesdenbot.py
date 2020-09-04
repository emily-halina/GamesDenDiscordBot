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
'⚔️': 'Looking for TTRPG',
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
    if not message.channel.is_nsfw() and not message.author.bot:
        for curse in CURSE_WORDS:
            if curse in content:
                await message.channel.send('Hey do not say that please edit ur message')
                await log.send(
                f"Posted warning for {message.author}'s message: \n"
                f"```{content}```")
                break
    # let them say that
    if 'uwu' in content and not message.author.bot:
        await message.channel.send('owo')
    if 'owo' in content and not message.author.bot:
        await message.channel.send('uwu')
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

@client.command()
async def roll(ctx):
    '''
    Multi purpose dice roller.
    Takes input in the format of: AdB + C
    Supports multiple dice and modifiers in the same roll, as well as negative dice.

    Input Examples:
    2d6 + 1d8 + 2
    5+d6+7d8
    d20 + 7
    2d8 - d6 + 2

    If no argument is given, returns a random number between 1 and 100.
    '''
    # parse the input if it is valid and get the results
    process = True
    VALID_CHARS = [' ', '   ', '1','2','3','4','5','6','7','8','9','0','d', '+', '-', '💯']
    for c in ctx.message.content[6:]:
        if c.lower() not in VALID_CHARS:
            process = False
    if process == True:
        result = parse_dice_rolls(ctx.message.content[6:])
    else:
        await ctx.channel.send('Error! Please check your formatting and try again..')
        return
    # if the result is a list, the input was a sequence of dice
    if type(result) == type([]):
        # process the result of the rolls and place into an embedded message
        desc_str = '**' + ctx.message.content[6:] + '**'
        roll_embed = discord.Embed(title="Dice Roll Results", description=desc_str, color=0x709cdb)
        for item in result:
            if type(item) == type([]):
                rolls = ''
                i = 1
                while i < len(item):
                    rolls += (item[i] + ' ')
                    i += 1
                roll_embed.add_field(name=item[0], value=rolls, inline=False)
        modifier = result[len(result)-2]
        # add on the modifier tab if there is a modifier
        if type(modifier) == type(1) and modifier != 0:
            if modifier > 0:
                modifier = str(modifier)
                modifier = '+' + modifier
            else:
                modifier = str(modifier)
            roll_embed.add_field(name='Modifier:', value=modifier, inline=False)
        roll_embed.add_field(name='Total:', value= '**' + result[len(result)-1] + '**', inline=False)
    # if the result is an integer, there was no provided argument (roll a d100)
    elif type(result) == type(1):
        roll_embed = discord.Embed(title="Dice Roll Results", description='d100', color=0x709cdb)
        roll_embed.add_field(name='d100', value=result, inline=False)
    elif type(result) == type('hi'):
        await ctx.channel.send(result)
        return
    # failsafe
    else:
        await ctx.channel.send('Error! This command takes input in the format of AdB + C')
        return
    await ctx.channel.send(embed=roll_embed)

@client.command()
@commands.has_role('execs')
async def nickname_check(ctx):
    '''
    if someone hasn't changed their username, tattle on them
    '''
    member_list = client.guilds[0].members
    join_list = []
    for member in member_list:
        if member.nick == None:
            join_list.append(member)
    join_list.sort(key=lambda member: member.joined_at)
    embed = discord.Embed(title='Nickname Check', description='bad boyz girlz and enbiez', color=0x709cdb)
    for member in join_list:
        embed.add_field(name=member.name + '#' + str(member.discriminator), value=str(member.joined_at), inline=False)
    await ctx.channel.send(embed=embed)

@client.command()
@commands.has_role('execs')
async def shuffle(ctx):
    '''
    shuffles the users in a given voice channel

    takes input in the form of !shuffle Channel Name
    '''
    server = client.guilds[0]
    channel_list = server.voice_channels
    game_chats = []
    for channel in channel_list:
        if ctx.message.content[9:] == channel.name:
            match = True
            shuffle_channel = channel
        elif 'Game Chat' in channel.name:
            game_chats.append(channel)
    if match:
        random_ids = []
        i = 0
        # add the appropriate amount of numbers
        for member in shuffle_channel.members:
            random_ids.append(i)
            if i < 2:
                i += 1
            else:
                i = 0
        random.shuffle(random_ids)
        # move members to random channels
        k = 0
        for member in shuffle_channel.members:
            await member.move_to(game_chats[random_ids[k]])
            k += 1
    else:
        await ctx.channel.send('Error, not a valid channel!')

client.run(TOKEN)
