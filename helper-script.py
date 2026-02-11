import discord
from discord.ext import commands
import base64
import asyncio

DISCORD_TOKEN = ""
CHANNEL_ID = 
C2_BOT_USER_ID = 

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Helper bot connected as {bot.user}')
    bot.channel = bot.get_channel(CHANNEL_ID)
    if not bot.channel:
        print("Channel not found!")

@bot.event
async def on_message(message):
    # Ignore messages not in target channel
    if message.channel.id != CHANNEL_ID:
        return

    # Only decode messages from the C2 bot
    if message.author.id != C2_BOT_USER_ID:
        return

    # Ignore empty messages or non-codeblock content
    if not message.content.startswith("```") or not message.content.endswith("```"):
        return

    encoded_output = message.content.strip()[3:-3].strip()  # Remove triple backticks

    try:
        decoded = base64.b64decode(encoded_output).decode('utf-8', errors='replace')
        await message.reply(f"Decoded Output:\n```\n{decoded}\n```")
    except Exception as e:
        pass

bot.run(DISCORD_TOKEN)