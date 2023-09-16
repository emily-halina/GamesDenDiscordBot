#!/usr/bin/env python3
# Games Den Bot v0.1
# small bot for Games Den discord server

import discord
from discord.ext import commands
from discord.utils import get

import os
import dotenv
from datetime import datetime
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
PRONOUN_MESSAGE = int(os.getenv('PRONOUN_MESSAGE'))
DENIZEN_MESSAGE = int(os.getenv('DENIZEN_MESSAGE'))
WEST_MARCHES_MESSAGE = int(os.getenv('WEST_MARCHES_MESSAGE'))

# get base path for file sending
BASE_PATH = os.getenv('BASE_PATH') + '/'

# Get random greetings
greetings = []
with open(BASE_PATH + 'greetings.txt', 'r') as f:
    greetings = f.read().split(';\n')

intents = discord.Intents.default() # Needed to enable recieving updates on member join/leave
intents.members = True

client = commands.Bot(command_prefix = '!', intents=intents)

# list of roles
roles = {
'🖌️': 'Artist',
'🖥️': 'Programmer',
'🗺': 'Designer',
'📝': 'Writer',
'🎵': 'Audio',
'👔': 'Producer',
'⚔️': 'Looking for TTRPG',
'🎲': 'Board Games',
'🎴': 'Card Games'
}
pronouns = {
'💜': 'she/her',
'🧡': 'they/them',
'💛': 'he/him',
'💚': 'she/they',
'💙': 'he/they'
}
role_emoji_list = roles.keys()
pronoun_emoji_list = pronouns.keys()

questions = []
async def is_exec_or_speaker(ctx):
    for role in ctx.author.roles:
        if role.name == 'Execs' or role.name == 'Speaker' or role.name == 'Chairs':
            return True
    return False

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
    server = client.guilds[0]
    channel = client.get_channel(GREETING_CHANNEL)
    rules = get(server.channels, name='rules-and-info')
    intro = get(server.channels, name='introductions')
    role = get(server.channels, name='role-signup')

    message = random.choice(greetings).strip()
    await channel.send(message.format(member = member, rules = rules, intro = intro, role = role))

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
                if str(message.author) == 'AttacktoWin#7991':
                    await message.channel.send("Hey, please check your mess- Oh, I'm sorry Mr. President, I didn't realize it was you! I'll look the other way this time but please watch your language in the future!")
                else:
                    await message.channel.send('Hey, please check your message for swears!')

                audit_embed = discord.Embed(title="Swear detected", description=str(message.author), color=0xfc3232, timestamp=message.created_at)
                audit_embed.add_field(name="Original Message", value=content, inline=False)
                audit_embed.add_field(name="Offending Word", value=curse, inline=False)
                audit_embed.add_field(name="Channel", value=message.channel.name, inline=False)

                await log.send(embed=audit_embed)
                break
    # let them say that
    if 'uwu' in content and not message.author.bot:
        if random.randint(1, 10) == 1:
            await message.channel.send(file=discord.File(BASE_PATH + 'uwu.png'))
        else:
            await message.channel.send('owo')
    if 'owo' in content and not message.author.bot:
        await message.channel.send('uwu')
    if 'uwo' in content and not message.author.bot:
        await message.channel.send('owu')
    if 'owu' in content and not message.author.bot:
        await message.channel.send('uwo')
    await client.process_commands(message)

# error handling for commands not existing
@client.event
async def on_command_error(message, error):
    if isinstance(error, commands.CommandNotFound):
        pass

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
    if message_id == PRONOUN_MESSAGE:
        emoji = payload.emoji.name
        member = server.get_member(payload.user_id)
        if emoji in pronoun_emoji_list:
            if member:
                role = get(server.roles, name=pronouns[emoji])
                await member.add_roles(role)
    if message_id == DENIZEN_MESSAGE:
        emoji = payload.emoji.name
        member = server.get_member(payload.user_id)
        if emoji == 'main_bear':
            if member:
                role = get(server.roles, name='Denizens')
                await member.add_roles(role)
    if message_id == WEST_MARCHES_MESSAGE:
        emoji = payload.emoji.name
        member = server.get_member(payload.user_id)
        if emoji == '🧭':
            if member:
                role = get(server.roles, name = 'dnd-west-marches')
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
    if message_id == PRONOUN_MESSAGE:
        emoji = payload.emoji.name
        member = server.get_member(payload.user_id)
        if emoji in pronoun_emoji_list:
            if member:
                role = get(server.roles, name=pronouns[emoji])
                await member.remove_roles(role)
    if message_id == DENIZEN_MESSAGE:
        emoji = payload.emoji.name
        member = server.get_member(payload.user_id)
        if emoji == 'main_bear':
            if member:
                role = get(server.roles, name='Denizens')
                await member.remove_roles(role)
    if message_id == WEST_MARCHES_MESSAGE:
        emoji = payload.emoji.name
        member = server.get_member(payload.user_id)
        if emoji == 'compass':
            if member:
                role = get(server.roles, name = 'dnd-west-marches')
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
async def q(ctx):
    '''
    Adds a question to the question queue
    Usage: !q [Question]
    '''
    question = {
        "message": ctx.message.content[3:],
        "author": ctx.author
    }
    if len(question["message"]) == 0:
        return await ctx.channel.send('No question found! Make sure you have a question in the message!')
    questions.append(question)
    
    await ctx.channel.send(f'Added question! There\'s now **{len(questions)}** in the queue.')

@client.command()
@commands.check(is_exec_or_speaker)
async def dq(ctx):
    '''
    Gets the first question in the queue and posts it
    Use !dq all to remove all questions or !dq list to see how many are left
    '''
    if len(questions) == 0:
        return await ctx.channel.send('No messages in the queue.')
    if len(ctx.message.content) > 3:
        if ctx.message.content.split(' ')[1].strip().lower() == 'all':
            questions.clear()
            return await ctx.channel.send('Cleared all questions in the queue!')
        if ctx.message.content.split(' ')[1].strip().lower() == 'list':
            return await ctx.channel.send(f'There are **{len(questions)}** questions in the queue.')
    question = questions.pop(0)
    message = discord.Embed(title="Question", color=0xf2e835)
    message.add_field(name=question["author"], value=question["message"], inline=False)
    message.add_field(name='Questions left', value=len(questions), inline=False)

    await ctx.channel.send(content='<@&817218239888359465>', embed=message)

@client.command()
@commands.has_role('Execs')
async def nickname_check(ctx):
    '''
    if someone hasn't changed their username, tattle on them
    '''
    member_list = client.guilds[0].members
    join_list = []
    with open(BASE_PATH + 'good_list.txt', 'r') as f:
        whitelist = f.readlines()
        for member in member_list:
            if member.nick == None:
                if f'{str(member)}\n' not in whitelist:
                    join_list.append(member)
    join_list.sort(key=lambda member: member.joined_at)
    embed = discord.Embed(title='Nickname Check', description='bad boyz girlz and enbiez', color=0x709cdb)
    embed_limit = 20
    e = 1
    embed_list = []
    for member in join_list:
        embed.add_field(name=member.name + '#' + str(member.discriminator), value=str(member.joined_at), inline=False)
        e += 1
        if e > embed_limit:
            embed_list.append(embed)
            embed = discord.Embed(title='Nickname Check', description='bad boyz girlz and enbiez', color=0x709cdb)
            e = 1
    if e != 1:
        embed_list.append(embed)
    for message in embed_list:
        await ctx.channel.send(embed=message)

@client.command()
@commands.has_role('Execs')
async def whitelist_add(ctx):
    '''
    Adds a user to the good boyz/girlz/enbiez list even if they haven't
    changed their username
    '''
    with open(BASE_PATH + 'good_list.txt', 'r') as list_file:
        whitelist = list_file.readlines()
        name = ctx.message.content[15:]

        if name not in whitelist:
            with open(BASE_PATH + 'good_list.txt', 'a') as f:
                f.write('\n' + name)
            await ctx.channel.send('Added ' + name + ' to the good boyz/girlz/enbiez list')
        else:
            await ctx.channel.send(name + ' is already in the list!')

@client.command()
@commands.has_role('Execs')
async def whitelist_check(ctx):
    '''
    Lists all the members in the good list, for auditing
    '''
    with open(BASE_PATH + 'good_list.txt', 'r') as list_file:
        whitelist = list_file.readlines()
        whitelist.sort(key= lambda name: name.lower())
        message = '**Whitelist:**\n```'
        for count in range(len(whitelist)):
            message += '{name}'.format(name= whitelist[count].strip())
            if count != len(whitelist) - 1:
                message += ', '

        message += '```'

        await ctx.channel.send(message)

@client.command()
@commands.has_role('Execs')
async def whitelist_remove(ctx):
    '''
    Removes a name from the whitelist
    '''
    with open(BASE_PATH + 'good_list.txt', 'r') as list_file:
        whitelist = list_file.readlines()
        name = ctx.message.content[18:]

        for i in range(len(whitelist)):
            if whitelist[i].strip() == name:
                whitelist.pop(i)
                with open(BASE_PATH + 'good_list.txt', 'w') as f:
                    f.write(''.join(whitelist))
                await ctx.channel.send(f'{name} has been removed from the good list!')
                break
        else:
            await ctx.channel.send(f'{name} is not on the list.')


@client.command()
@commands.has_role('Execs')
async def say(ctx: discord.ext.commands.context.Context):
    '''
    Makes bearbot say whatever you'd like,
    wherever you'd like
    '''
    message = ' '.join(ctx.message.content.split()[2:])
    channel = ctx.message.channel_mentions[0]

    if channel:
        await channel.send(message)
    else:
        await ctx.channel.send('Cannot send message.')


@client.command()
@commands.has_role('Execs')
async def shuffle(ctx):
    '''
    shuffles the users in a given voice channel

    takes input in the form of !shuffle Channel Name, number of groups
    '''
    server = client.guilds[0]
    channel_list = server.voice_channels
    message = ctx.message.content.split(',')
    match = False
    num_groups = 0

    # find the voice channel in question
    for channel in channel_list:
        if message[0][9:] == channel.name:
            match = True
            shuffle_channel = channel
            break

    try:
        num_groups = int(message[1])
        if num_groups < 1: raise Exception()
    except:
        num = False
    else:
        num = True

    # if the syntax is valid
    if match and num:
        # shuffle up the members and disperse them into groups
        members = shuffle_channel.members
        random.shuffle(members)
        master_list = []
        j = 0
        for i in range(num_groups):
            master_list.append([])
        while len(members) > 0:
            master_list[j].append(members.pop())
            # increment j
            j = (j + 1) % num_groups
        # send the groups
        embed = discord.Embed(title="The Fixed Shuffle Command", description=str(num)+"groups", color=0xfc3232)
        k = 1
        for group in master_list:
            name = "Group " + str(k)
            k += 1
            content = ''
            for member in group:
                content += member.nick
                content += ', '
            embed.add_field(name=name, value=content, inline=False)
        await ctx.channel.send(embed=embed)
        
    elif not match:
        await ctx.channel.send('Error, not a valid channel!')
    elif not num:
        await ctx.channel.send('Error, not a valid number!')
    else:
        await ctx.channel.send('Something about your syntax is Just Wrong. check !help!!!')

client.run(TOKEN)
