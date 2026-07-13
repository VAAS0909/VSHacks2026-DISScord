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
intents.moderation = True


client = commands.Bot(command_prefix='?!', intents=intents)

# Roles the authenticator bot could give the user
pending_role = "joiner"
approval_role = "passer"
disapproval_role = "no-goer"

# Number of messages purged during the final purge
purgeMessages = 20

# Counts attempts
attempts = {}


# When the bot is ready
@client.event
async def on_ready():
    print(f"Bot is ready, {client.user.name}")


# When a user joins
@client.event
async def on_member_join(member):
    guild = member.guild
    channel = discord.utils.get(guild.text_channels, name="interrogation-room")

    # Asks for the passcode
    if channel:
        await channel.send(f"Hello {member.name}. What is the passcode?")
    else:
        print("Couldn't find interrogation-room.")
        return

    # Gives the pending role
    pending = discord.utils.get(guild.roles, name=pending_role)
    if pending:
        await member.add_roles(pending)
    else:
        await channel.send("I suppose no role for you")
        await asyncio.sleep(10)
        await channel.purge(limit=1)

    #if the number of pending roles given out are greater than one, then kick the last member that joined
    count = sum(1 for mem in guild.members if pending in mem.roles)
    if count > 1:
        await member.kick(reason="One person in the interrogation room at a time! Wait till the other guy finishes.")
        await channel.purge(limit=1)


# When someone sends a message
@client.event
async def on_message(message):
    user_id = message.author.id
    bot = discord.utils.get(message.guild.roles, name="Bot")
    pending = discord.utils.get(message.guild.roles, name=pending_role)

    # ignores if the bot is the same as the
    if message.author == client.user:
        return

    # restricts the bot to the interrogation room
    if message.channel.name != "interrogation-room":
        return

    # doesn't allow itself to reply to bots
    if bot in message.author.roles:
        return

    # checks if the message sent was a password
    if message.content.strip() == "DISSisapassword":
        await message.delete()
        role = discord.utils.get(message.guild.roles, name=approval_role)
        attempts[user_id] = 0

        pending = discord.utils.get(message.guild.roles, name=pending_role)
        if pending:
            await message.author.remove_roles(pending)

        if role:
            await message.author.add_roles(role)
            await message.channel.send(f"{message.author.mention}, you have been granted access")
            await asyncio.sleep(10)
            await message.channel.purge(limit=purgeMessages)
            await message.channel.set_permissions(message.author, send_messages=False, read_messages=False, add_reactions=False)
        else:
            await message.channel.send("Nah no access for you.")
            await asyncio.sleep(10)
            await message.channel.purge(limit=purgeMessages)

    # if not the pasword
    else:
        await message.channel.purge(limit=1)
        attempts[user_id] = attempts.get(user_id, 0) + 1

        if attempts[user_id] >= 3:
            role = discord.utils.get(message.guild.roles, name=disapproval_role)
            attempts[user_id] = 0

            pending = discord.utils.get(message.guild.roles, name=pending_role)
            if pending:
                await message.author.remove_roles(pending)

            if role:
                await message.author.add_roles(role)
                await message.channel.send(f"{message.author.mention}, YOU SHALL NOT PASS!")
                await asyncio.sleep(10)
                await message.channel.purge(limit=purgeMessages)
                await message.channel.set_permissions(message.author, send_messages=False, read_messages=False, add_reactions=False)
            else:
                await message.channel.send("Nah no access for you.")
                await asyncio.sleep(10)
                await message.channel.purge(limit=1)
        else:
            await message.channel.send(f"{message.author.mention}, try again.")
            await asyncio.sleep(10)
            await message.channel.purge(limit=1)

    await client.process_commands(message)

@client.command
async def ping(ctx):
    await ctx.send('pong')

client.run(token, log_handler=handler, log_level=logging.DEBUG)