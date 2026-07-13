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

help_role = "helped"
approval_role = "passer"
human_role = "human"

client = commands.Bot(command_prefix='?!', intents=intents)

attempts = {}

@client.event
async def on_ready():
    print(f"Bot is ready, {client.user.name}")


@client.event
async def on_member_join(member):
    await member.send(f"BAHAHAHAHAHAHA {member.name} I can't believe someone like YOU would join, you should just leave.")


@client.event
async def on_message(message):
    user_id = message.author.id
    if message.author == client.user:
        return

    if message.channel.name != "human-verification":
        await client.process_commands(message)
        return

    if message.attachments:
        attempts[user_id] = attempts.get(user_id, 0) + 1

        if attempts[user_id] == 1:
            await message.channel.send(f"Boys, roast {message.author.mention}!")

        for attempts[user_id] in range(5):
            attempts[user_id] = attempts.get(user_id, 0) + 1
            await asyncio.sleep(5)
            await message.channel.send(f"Roast them more!")

        role = discord.utils.get(message.guild.roles, name=human_role)
        if role:
            await message.author.add_roles(role)
        else:
            await message.send("Nah.")

        approval = discord.utils.get(message.guild.roles, name=approval_role)
        if approval:
            await message.author.remove_roles(approval)

        await asyncio.sleep(30)
        await message.channel.purge(limit=200)
        await message.channel.send(f"Please send a photo of yourself or a piece of government-issued id for human verification.")

    await client.process_commands(message)


@client.command(name="helpMe", description="Responds with help!")
async def helpMe(ctx):
    await ctx.send(f"Imagine needing help, @everyone, {ctx.author.mention} IS CRINGE!")
    role = discord.utils.get(ctx.guild.roles, name=help_role)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention}, you have been awarded the helped role for your idiocy and incompetency")
    else:
        await ctx.send("Nah.")

client.run(token, log_handler=handler, log_level=logging.DEBUG)