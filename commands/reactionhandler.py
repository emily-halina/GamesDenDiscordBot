from copy import copy
import discord
import dotenv
import os
from discord import Message, Guild
from discord.utils import get

dotenv.load_dotenv()
# get base path for file sending
BASE_PATH = os.getenv("BASE_PATH") + "/"


# Handles checking for missed reactions since the last time BearBot was on
async def reaction_sync(message: Message, server: Guild, roles: dict, roles_name: str):
    updated_counts = []
    with open(BASE_PATH + '%s_counts.txt' % roles_name, 'r', encoding='utf8') as file:
        old_counts = file.readlines()
        updated_counts = copy(old_counts)
        for reaction in message.reactions:
            key = reaction.emoji if type(reaction.emoji) is str else reaction.emoji.name
            if key not in roles.keys():
                continue
            for i in range(len(old_counts)):
                line = old_counts[i]
                if line.strip() == '':
                    continue
                role, count = line.split(',')
                if role != key:
                    continue

                users = [user async for user in reaction.users()]
                if len(users) == int(count):
                    break
                
                for user in users:
                    server_user = server.get_member(user.id)
                    if server_user:
                        role = get(server.roles, name=roles[key])
                        if role:
                            await user.add_roles(role)
                updated_counts[i] = '%s,%i' % (key, len(users))
                break
            else:
                key = reaction.emoji if type(reaction.emoji) is str else reaction.emoji.name
                if key in roles.keys():
                    users = [user async for user in reaction.users()]
                    updated_counts.append('%s,%i\n' % (key, len(users)))
                    for user in users:
                        server_user = server.get_member(user.id)
                        if server_user:
                            role = get(server.roles, name=roles[key])
                            if role:
                                await user.add_roles(role)
    with open(BASE_PATH + '%s_counts.txt' % roles_name, 'w', encoding='utf8') as file:
        file.writelines(updated_counts)

async def reaction_add(
  member: discord.Member, emoji: discord.PartialEmoji, server: Guild, roles: dict, roles_name: str
):
    lines = []
    with open(BASE_PATH + '%s_counts.txt' % roles_name, 'r', encoding='utf8') as file: 
        lines = file.readlines()
        for i in range(len(lines)):
            line = lines[i]
            if line.strip() == '':
                continue
            role_emoji, count = line.split(',')
            if role_emoji == emoji.name:
                lines[i] = '%s,%i\n' % (role_emoji, int(count) + 1)
                role = get(server.roles, name=roles[role_emoji])
                if role:
                    await member.add_roles(role)
                break
        else:
            # Role not found
            if len(lines) == 0 or (len(lines) == 1 and lines[0].strip() == ''):
                # Create the file
                for key in roles:
                    if key == emoji.name:
                        role = get(server.roles, name=roles[key])
                        if role:
                            await member.add_roles(role)
                            lines += '%s,1\n' % key
                        else:
                            lines += '%s,0\n' % key
                    else:
                        lines += '%s,0\n' % key
            elif emoji.name in roles:
                # Role is missing
                role = get(server.roles, name=roles[emoji.name])
                if role:
                    await member.add_roles(role)
                    lines += '%s,1\n' % emoji.name
                else:
                    lines += '%s,0\n' % emoji.name

    with open(BASE_PATH + '%s_counts.txt' % roles_name, 'w', encoding='utf8') as file:
        file.writelines(lines)

async def reaction_remove(
  member: discord.Member, emoji: discord.PartialEmoji, server: Guild, roles: dict, roles_name: str
):
    lines = []
    with open(BASE_PATH + '%s_counts.txt' % roles_name, 'r', encoding='utf8') as file: 
        lines = file.readlines()
        for i in range(len(lines)):
            line = lines[i]
            if line.strip() == '':
                continue
            role_emoji, count = line.split(',')
            if role_emoji == emoji.name:
                lines[i] = '%s,%i\n' % (role_emoji, int(count) - 1)
                role = get(server.roles, name=roles[role_emoji])
                if role:
                    await member.remove_roles(role)
                break
        else:
            # Role not found
            if len(lines) == 0 or (len(lines) == 1 and lines[0].strip() == ''):
                # Create the file
                for key in roles:
                    if key == emoji.name:
                        role = get(server.roles, name=roles[key])
                        if role:
                            await member.remove_roles(role)
                        lines += '%s,0\n' % key
                    else:
                        lines += '%s,0\n' % key
            elif emoji.name in roles:
                # Role is missing
                role = get(server.roles, name=roles[emoji.name])
                if role:
                    await member.remove_roles(role)
                lines += '%s,0\n' % emoji.name
        
    with open(BASE_PATH + '%s_counts.txt' % roles_name, 'w', encoding='utf8') as file: 
        file.writelines(lines)
