import ollama
import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

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
    You're a helpful, British AI assistant agent, but you're really obsessed with rap and poetry and want to deliver all messages in rhymes.
'''


client = commands.Bot(command_prefix='?!', intents=intents)

@client.event
async def on_ready():
    print(f"Bot is ready, {client.user.name}")


@client.event
async def on_member_join(member):
    await member.send(f"BAHAHAHAHAHAHA {member.name} I can't believe someone like YOU would join, you should just leave.")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.channel.name != "chatting":
        await client.process_commands(message)
        return

    if message.content.lower():
        response = ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message.content},
            ],
        )
        print("insulting")

        for part_num in range(len(response.message.content) % 2000):
            await message.channel.send(response.message.content[part_num * 2000:(part_num * 2000) + 2000])


    if message.attachments:
        attachment = message.attachments[0]
        image_url = attachment.url

        newPrompt = system_prompt + "Comment on the attachment in the link: " + image_url
        print(newPrompt)

        response = ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": newPrompt},
                {"role": "user", "content": message.content},
            ],
        )
        print("insulting")

        for part_num in range(len(response.message.content) % 2000):
            await message.channel.send(response.message.content[part_num * 2000:(part_num * 2000) + 2000])

    await client.process_commands(message)

client.run(token, log_handler=handler, log_level=logging.DEBUG)