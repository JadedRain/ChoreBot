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
        self.person_setup()
        print("Chore commands loaded")
        
    @commands.command(name="addchore")
    async def add_chore(self, ctx, *chore_name):
        c = Chore(' '.join(chore_name[:]).title())
        self.chore_list.append(c)
        
    @commands.command(name="shchores")
    async def show_chores(self, ctx):
        for i in range(len(self.chore_list)):
            await ctx.channel.send(f"Chore: {self.chore_list[i].get_chore()} Person: <@{self.chore_list[i].get_person()}> Completed: {self.chore_list[i].completed}")
            
    @commands.command(name="assign")
    async def assign_chores(self, ctx):
        for chore in self.chore_list:
            chore.set_person(random.choice(list(self.person_list.values())))
            
    @commands.command(name="complete")
    async def complete_chore(self, ctx, *chore):
        for c in self.chore_list:
            if c.get_chore() == ' '.join(chore[:]).title() and ctx.author.id == c.get_person():
                c.completed = True
            

            
    
    # adds users to pick from for chores
    def person_setup(self):
        guilds = self.bot.guilds
        for guild in guilds:
            role = discord.utils.find(lambda r: r.name.lower() == "roommate", guild.roles)
            for member in guild.members:
                if role in member.roles:
                   self.person_list[member.display_name] = member.id
            
async def setup(bot):
    await bot.add_cog(ChoreCommands(bot))




