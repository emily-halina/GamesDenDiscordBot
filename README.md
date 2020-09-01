# GamesDenDiscordBot
Small discord bot for the Games Den game development club at University of Alberta.

Written by Eric Halina, with reference to previous bot by Atharv Vohra --> https://github.com/AtharvVohra/BearBot

## Includes:
- join / leave message for users joining and leaving server
- assigning / removing roles based on reactions to a specific message
- filtering message content for curses and requesting users to edit their messages
- logging these activities in a seperate bot log channel
- dice rolling command for D&D


## .env file setup
Create a .env file in the same directory as the bot script, and copy paste the following into it, replacing the relevant information as needed.

```
# .env
DISCORD_TOKEN = your_bot_token
DISCORD_SERVER = your_server_name
CURSE_WORDS = censored, list, of, words, formatted, like, so
GREETING_CHANNEL = channel_ID
BOT_LOG_CHANNEL = channel_ID
ROLE_MESSAGE = message_ID
```

## To add:
- editable / quotable rules text
- more to come
