import discord
import random
from discord.ext import commands
from discord.ui import view
from pclasses.chore import Chore

class ChoreCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.chore_list = []
        self.person_list = {}        
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Chore commands loaded")
        
    @commands.command(name="addchore")
    async def add_chore(self, ctx, *chore_name):
        c = Chore(random.choice(list(self.person_list.keys())), ' '.join(chore_name[:]).title())
        self.chore_list.append(c)
        
    @commands.command(name="shchores")
    async def show_chores(self, ctx):
        for i in range(len(self.chore_list)):
            await ctx.channel.send(self.chore_list[i].get_chore())
            
    @commands.command(name="addppl")
    async def person_setup(self, ctx):
        guild = ctx.message.guild
        role = discord.utils.find(lambda r: r.name.lower() == "roommate", guild.roles)
        for member in guild.members:
            if role in member.roles:
               self.person_list[member.display_name] = member.id
               print(f"{member.display_name} added")
            
async def setup(bot):
    await bot.add_cog(ChoreCommands(bot))




