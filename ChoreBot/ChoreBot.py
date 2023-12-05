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

async def load():
    for filename in os.listdir('./commands'):
        if filename.endswith('.py'):
            await bot.load_extension(f'commands.{filename[:-3]}')

@bot.event
async def on_ready():
    guild_info = GuildInfo(bot.guilds)
    guilds = guild_info.get_guilds()
    await guild_info.list_guild_info()
    
@bot.event
async def on_guild_join(guild):
    print(f"Joined: {guild.name}")

async def main():
    await load()
    await bot.start(DISCORD_TOKEN)
    

asyncio.run(main())