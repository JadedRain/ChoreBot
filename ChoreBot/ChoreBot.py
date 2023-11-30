import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from pclasses.guild_info import GuildInfo


load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
