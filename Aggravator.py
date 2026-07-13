import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import time
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
intents.moderation = True

client = commands.Bot(command_prefix='?!', intents=intents)

pending_role = "joiner"
approval_role = "passer"
disapproval_role = "no-goer"

purgeMessages = 20

attempts = {}


@client.event
async def on_ready():
    print(f"Bot is ready, {client.user.name}")


@client.event
async def on_member_join(member):
    guild = member.guild
    channel = discord.utils.get(guild.text_channels, name="beat-em-up")

    # if channel:
    #     await channel.send(f"Hello {member.name}. How was your day?")
    # else:
    #     print("Couldn't find beat-em-up.")
    #     return


@client.event
async def on_message(message):
    user_id = message.author.id
    target_role = discord.utils.get(message.guild.roles, name="Bot")

    if message.author == client.user:
        return

    if target_role in message.author.roles:
        return

    if message.channel.name != "beat-em-up":
        await client.process_commands(message)
        return

    else:
        attempts[user_id] = attempts.get(user_id, 0) + 1

        if attempts[user_id] == 1:
            await message.channel.send(f"Boys, insult {message.author.mention}!")

        for attempts[user_id] in range(10):
            attempts[user_id] = attempts.get(user_id, 0) + 1
            await asyncio.sleep(5)
            await message.channel.send(f"Insult them again!")

        await asyncio.sleep(30)
        await message.channel.purge(limit=200)
        await message.channel.send(f"How was your day?")

    await client.process_commands(message)


@client.command
async def ping(ctx):
    await ctx.send('pong')


client.run(token, log_handler=handler, log_level=logging.DEBUG)