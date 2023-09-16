import dotenv
import discord
from discord import Message, Guild
from discord.utils import get
import os

dotenv.load_dotenv()
# get base path for file sending
BASE_PATH = os.getenv('BASE_PATH') + '/'

# Handles checking for missed reactions since the last time BearBot was on
async def reaction_sync(message: Message, server: Guild, roles: dict, roles_name: str):
    with open(BASE_PATH + '%s_counts.txt' % roles_name, 'a+', encoding='utf8') as file:
        old_counts = file.readlines()
        updated_counts = file.readlines()
        for reaction in message.reactions:
            if reaction.emoji not in roles.keys():
                continue
            for i in range(len(old_counts)):
                line = old_counts[i]
                role, count = line.split(',')
                if role != reaction.emoji:
                    continue
                
                users = [user async for user in reaction.users()]
                if len(users) == int(count):
                    continue
                
                for user in users:
                    if user is discord.Member:
                        role = get(server.roles, name=roles[reaction.emoji])
                        if role:
                            await user.add_roles(role)
                updated_counts[i] = '%s,%i' % (reaction.emoji.name, len(users))
                break
            else:
                if reaction.emoji in roles.keys():
                    users = [user async for user in reaction.users()]
                    updated_counts.append('%s,%i\n' % (reaction.emoji
                                                        if type(reaction.emoji) is str
                                                        else reaction.emoji.name, len(users)))
                    for user in users:
                        if user is discord.Member:
                            role = get(server.roles, name=roles[reaction.emoji])
                            if role:
                                await user.add_roles(role)
        file.seek(0)
        file.writelines(updated_counts)
        file.truncate()

async def reaction_add(member: discord.Member, emoji: discord.PartialEmoji, server: Guild, roles: dict):
    with open(BASE_PATH + 'reaction_counts.txt', 'a+', encoding='utf8') as file: 
        lines = file.readlines()
        for i in range(len(lines)):
            line = lines[i]
            role_emoji, count = line.split(',')
            if role_emoji == emoji.name:
                lines[i] = '%s,%i' % (role_emoji, int(count) + 1)
                role = get(server.roles, name=roles[role_emoji])
                if role:
                    await member.add_roles(role)
                break
        file.seek(0)
        file.writelines(lines)
        file.truncate()

async def reaction_remove(member: discord.Member, emoji: discord.PartialEmoji, server: Guild, roles: dict):
    with open(BASE_PATH + 'reaction_counts.txt', 'a+', encoding='utf8') as file: 
        lines = file.readlines()
        for i in range(len(lines)):
            line = lines[i]
            role_emoji, count = line.split(',')
            if role_emoji == emoji.name:
                lines[i] = '%s,%i' % (role_emoji, int(count) - 1)
                role = get(server.roles, name=roles[role_emoji])
                if role:
                    await member.remove_roles_roles(role)
                break
        file.seek(0)
        file.writelines(lines)
        file.truncate()
