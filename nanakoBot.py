import discord
import openai
import os
import logging
import logging.handlers

# main part
intents = discord.Intents.default()
intents.message_content = True

discordToken = '[yourTokenHere]'
openaiToken = '[yourTokenHere]'

client = discord.Client(intents=intents)
openai.api_key = openaiToken
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

# gpt part
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('娜娜子') or message.content.startswith('Nanako'):
        print(message.content)
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=[
                {"role": "system", "content": "You are a female virtual assistant named Nanako."},
                {"role": "user", "content": message.content}
            ]
        )
        print(response.choices[0].message.content)
        await message.channel.send(response.choices[0].message.content)

# logging part
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
logging.getLogger('discord.http').setLevel(logging.INFO)

handler = logging.handlers.RotatingFileHandler(
    filename='discord.log',
    encoding='utf-8',
    maxBytes=32 * 1024 * 1024,  # 32 MiB
    backupCount=5,  # Rotate through 5 files
)
dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Assume client refers to a discord.Client subclass...
# Suppress the default configuration since we have our own
client.run(discordToken, log_handler=None)
