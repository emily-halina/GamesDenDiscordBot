# Games Den Bot: West Marches Edition
# An edited edition of Bear Bot, with changed functionality for the WM server!

import discord
from discord.ext import commands
from discord.utils import get

import os
from datetime import datetime
from dotenv import load_dotenv

import random
from dnd_dice_roller import parse_dice_rolls
from west_marches import *

# load up attributes from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('DISCORD_SERVER')
CURSE_STRING = os.getenv('CURSE_WORDS')
CURSE_WORDS = CURSE_STRING.split(', ')

BOT_LOG_CHANNEL = int(os.getenv('BOT_LOG_CHANNEL'))

intents = discord.Intents.default() # Needed to enable recieving updates on member join/leave
intents.members = True

client = commands.Bot(command_prefix = '!', intents=intents)


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
                if str(message.author) == 'TheArcticGiraffe#5863':
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
@commands.has_role('Dungeon Masters')
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

# WM specific commands
@client.command()
async def createChar(ctx):
    '''
    Creates a character for West Marches.
    Usage: !create_char character_name gold
    '''
    content = ctx.message.content.split()
    if len(content) == 3:
        try:
            result = create_char(content[1], ctx.author.name, content[2])
        except Exception as e:
            await ctx.channel.send("Usage: !createChar character_name starting_gold")
        else:
            await ctx.channel.send(result)
    else:
        await ctx.channel.send("Usage: !createChar character_name starting_gold")

@client.command()
async def gainEXP(ctx):
    '''
    Gains a character's exp based on the session they just completed.
    Usage: !gainEXP charater_name encounter_level
    '''
    content = ctx.message.content.split()
    if len(content) == 3:
        try:
            result = gain_exp(content[1], ctx.author.name, int(content[2]))
        except Exception as e:
            await ctx.channel.send("Usage: !gainEXP charater_name encounter_level")
        else:
            await ctx.channel.send(result)
    else:
        await ctx.channel.send("Usage: !gainEXP charater_name encounter_level")


@client.command()
async def gainGold(ctx):
    '''
    Adds gold to a character. Only takes positive values.
    Usage: !gainGold character_name gold_value
    '''
    content = ctx.message.content.split()
    if len(content) == 3:
        try:
            if int(content[2]) <= 0:
                raise Exception
            result = change_gold(content[1], ctx.author.name, int(content[2]))
        except Exception as e:
            await ctx.channel.send("Usage: !gainGold charater_name gold_value (positive)")
        else:
            await ctx.channel.send(result)
    else:
        await ctx.channel.send("Usage: !gainGold charater_name encounter_level")

@client.command()
async def spendGold(ctx):
    '''
    Removes gold from a character. Only takes positive values.
    Usage: !spendGold character_name gold_value
    '''
    content = ctx.message.content.split()
    if len(content) == 3:
        try:
            if int(content[2]) <= 0:
                raise Exception
            result = change_gold(content[1], ctx.author.name, int(content[2]) * (-1))
        except Exception as e:
            await ctx.channel.send("Usage: !spendGold charater_name gold_value (positive)")
        else:
            await ctx.channel.send(result)
    else:
        await ctx.channel.send("Usage: !spendGold charater_name encounter_level")

@client.command()
async def charStatus(ctx):
    '''
    Checks on a character's status. Displays the info the bot stores!
    Usage: !charStatus character_name
    '''
    content = ctx.message.content.split()
    if len(content) == 2:
        try:
            char = get_status(content[1])
        except Exception as e:
            await ctx.channel.send("Usage: !charStatus character_name")
        else:
            char_embed = discord.Embed(title="Character Status", description=char[0], color=0x709cdb)
            char_embed.add_field(name="Player", value=char[1], inline=False)
            char_embed.add_field(name="Current Level", value=char[2], inline=False)
            char_embed.add_field(name="EXP to Next Level", value=str(char[3]), inline=False)
            char_embed.add_field(name="Gold", value=char[4], inline=False)
            char_embed.add_field(name="Guild Coins", value=char[5], inline=False)
            await ctx.channel.send(embed=char_embed)
    else:
        await ctx.channel.send("Usage: !charStatus character_name")

@client.command()
@commands.has_role('Dungeon Masters')
async def gainGC(ctx):
    '''
    Adds guild coins to the given character's stats.
    Usage: !gainGC character_name gc_value (positive)
    '''
    content = ctx.message.content.split()
    if len(content) == 3:
        try:
            result = change_GC(content[1], ctx.author.name, int(content[2]))
        except Exception as e:
            await ctx.channel.send("Usage: !gainGC character_name gc_value (positive)")
        else:
            await ctx.channel.send(result)
    else:
        await ctx.channel.send("Usage: !gainGC character_name gc_value (positive)")

@client.command()
@commands.has_role('Dungeon Masters')
async def spendGC(ctx):
    '''
    Adds guild coins to the given character's stats.
    Usage: !spendGC character_name gc_value (positive)
    '''
    content = ctx.message.content.split()
    if len(content) == 3:
        try:
            if int(content[2]) < 0:
                raise Exception
            result = change_GC(content[1], ctx.author.name, int(content[2]) * -1)
        except Exception as e:
            await ctx.channel.send("Usage: !spendGC character_name gc_value (positive)")
        else:
            await ctx.channel.send(result)
    else:
        await ctx.channel.send("Usage: !spendGC character_name gc_value (positive)")

client.run(TOKEN)
