import discord
import dotenv
import os
import random
from discord import Message, Guild
from discord.ext.commands import Bot
from discord.utils import get

dotenv.load_dotenv()
CURSE_STRING = os.getenv("CURSE_WORDS")
CURSE_WORDS = CURSE_STRING.split(", ")
PRESIDENT = os.getenv("PRESIDENT_USERNAME")
PRONOUN = os.getenv("PRESIDENT_TITLE")
BOT_LOG_CHANNEL = int(os.getenv("BOT_LOG_CHANNEL"))
# get base path for file sending
BASE_PATH = os.getenv("BASE_PATH") + "/"


async def message_handler(message: Message, server: Guild, client: Bot):
    content = message.content.lower()
    log = get(server.channels, id=BOT_LOG_CHANNEL)
    if not message.channel.is_nsfw() and not message.author.bot:
        for curse in CURSE_WORDS:
            if curse in content:
                if str(message.author) == PRESIDENT:
                    await message.channel.send(
                        "Hey, please check your mess-Oh, I'm sorry %s. President, I didn't realize" +
                        " it was you! I'll look the other way this time but please watch your language in the future!"
                        % PRONOUN
                    )
                else:
                    await message.channel.send(
                        "Hey, please check your message for swears!"
                    )

                audit_embed = discord.Embed(
                    title="Swear detected",
                    description=str(message.author),
                    color=0xFC3232,
                    timestamp=message.created_at,
                )
                audit_embed.add_field(
                    name="Original Message", value=content, inline=False
                )
                audit_embed.add_field(name="Offending Word", value=curse, inline=False)
                audit_embed.add_field(
                    name="Channel", value=message.channel.name, inline=False
                )

                await log.send(embed=audit_embed)
                break

    if "uwu" in content and not message.author.bot:
        if random.randint(1, 10) == 1:
            await message.channel.send(file=discord.File(BASE_PATH + "uwu.png"))
        else:
            await message.channel.send("owo")
    if "owo" in content and not message.author.bot:
        await message.channel.send("uwu")
    if "uwo" in content and not message.author.bot:
        await message.channel.send("owu")
    if "owu" in content and not message.author.bot:
        await message.channel.send("uwo")
    await client.process_commands(message)
