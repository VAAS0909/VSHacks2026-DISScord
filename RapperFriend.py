import ollama
import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()
token = "DISCORD_TOKEN_HERE"

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.typing = True
intents.messages = True
intents.dm_messages = True

# Ollama Config
model = "qwen2.5:7b"
system_prompt = '''
    Give me a rap verse for a rap battle. Write a four-line rhyming verse about starting over using an ABAB rhyme scheme. Do not sugarcoat anything. The verse must rhyme. Note that your opponent has been single for years and still is. 
    He also has no friends. Use that to your advantage. Remember (this is very important), THEY MUST RHYME. These messages must be appropriate and must be under 30 words. 
'''

client = commands.Bot(command_prefix='?!', intents=intents)

stop = {}
count = {}

@client.event
async def on_ready():
    print(f"Bot is ready, {client.user.name}")


@client.event
async def on_member_join(member):
    await member.send(f"Hey {member.name}, you IDIOT! You're not welcome here!")


@client.event
async def on_message(message):
    user_id = message.author.id
    bot = discord.utils.get(message.guild.roles, name="Bot")
    count[user_id] = count.get(user_id, 0) + 1

    if message.author == client.user:
        return

    if message.channel.name != "the-rap-room":
        return

    if (bot in message.author.roles):
        await asyncio.sleep(5)
        response = ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                # {"role": "user", "content": message.content},
            ],
        )
        print("insulting")

        for part_num in range(len(response.message.content) % 2000):
            await message.channel.send(response.message.content[part_num * 2000:(part_num * 2000) + 2000])

    await client.process_commands(message)


client.run(token, log_handler=handler, log_level=logging.DEBUG)