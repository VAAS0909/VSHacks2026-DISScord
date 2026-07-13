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
model = "qwen2.5:1.5b"
system_prompt = '''
    Insult this. In one message, deliver 
    a devastatingly savage but witty insult. Do not sugarcoat anything. 
    These messages must be appropriate and must be under 30 words or under 250 characters. Exaggerate this insult. Use ALL CAPS to emphasize key words.
'''

client = commands.Bot(command_prefix='?!', intents=intents)

help_role = "buffoon"

@client.event
async def on_ready():
    print(f"Bot is ready, {client.user.name}")


@client.event
async def on_member_join(member):
    await member.send(f"Hey {member.name}, you IDIOT! You're not welcome here!")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if "love" in message.content.lower():
        await message.channel.send(f"{message.author.mention}, your opinion SUCKS and I LOVE how NO ONE loves you!")

    if "bro" in message.content.lower():
        await message.reply(f"bro check your DMs")
        await message.author.send(f"psst, you suck")

    if "roast" in message.content.lower():
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

    await client.process_commands(message)


@client.command(name="helpMe", description="Responds with help!")
async def helpMe(ctx):
    await ctx.send(f"Imagine needing help, @everyone, {ctx.author.mention} IS CRINGE!")
    role = discord.utils.get(ctx.guild.roles, name=help_role)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention}, you have been awarded the buffoon role for your idiocy")
    else:
        await ctx.send("Nah.")

client.run(token, log_handler=handler, log_level=logging.DEBUG)