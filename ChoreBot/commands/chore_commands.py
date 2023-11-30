import discord
import random
from discord.ext import commands
from discord.ui import view
from pclasses.chore import Chore

class ChoreCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.person_list = []
        self.chore_list = []
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Chore commands loaded")
        
    @commands.command(name="addchore")
    async def add_chore(self, ctx, *chore_name):
        c = Chore("greg", ' '.join(chore_name[:]).title())
        self.chore_list.append(c)
        
    @commands.command(name="shchores")
    async def show_chores(self, ctx):
        for i in range(len(self.chore_list)):
            await ctx.channel.send(self.chore_list[i].get_chore())
            
async def setup(bot):
    await bot.add_cog(ChoreCommands(bot))




