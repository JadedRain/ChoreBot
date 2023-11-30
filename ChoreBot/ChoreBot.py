import asyncio
import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from pclasses.guild_info import GuildInfo


load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    guild_info = GuildInfo(bot.guilds)
    await guild_info.list_guild_info()
    
# @bot.command(name="test")
# async def test(ctx):
#     await ctx.send("this bot is up and running!")
    
async def main():
    await bot.start(DISCORD_TOKEN)
    

asyncio.run(main())