import discord
import random
from discord.ext import commands
from discord.ui import view
from pclasses.chore import Chore
from pclasses.guild_chores import GuildChore


class ChoreCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guilds = {}
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.setup()
        print("Chore commands loaded")
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        self.guilds[guild.id] = GuildChore(guild)
        
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        del self.guilds[guild.id]
        
        
    @commands.command(name="addchore")
    async def add_chore(self, ctx, *chore_name):
        c = Chore(' '.join(chore_name[:]).title())
        self.guilds[ctx.guild.id].add_chore(c)
    
    @commands.command(name="rmchore")
    async def remove_chore(self, ctx, *chore_name):
        self.guilds[ctx.guild.id].remove_chore(' '.join(chore_name[:]))
        
    @commands.command(name="shchores")
    async def show_chores(self, ctx):
        for i in range(len(self.guilds[ctx.guild.id].chore_list)):
            await ctx.channel.send(f"Chore: {self.guilds[ctx.guild.id].chore_list[i].get_chore()} Person: <@{self.guilds[ctx.guild.id].chore_list[i].get_person()}> Completed: {self.guilds[ctx.guild.id].chore_list[i].completed}")
            
    @commands.command(name="assign")
    async def assign_chores(self, ctx):
        for chore in self.guilds[ctx.guild.id].chore_list:
            chore.set_person(random.choice(list(self.guilds[ctx.guild.id].person_list.values())))
            
    @commands.command(name="complete")
    async def complete_chore(self, ctx, *chore):
        for c in self.guilds[ctx.guild.id].chore_list:
            if c.get_chore() == ' '.join(chore[:]).title() and ctx.author.id == c.get_person():
                c.completed = True
            
    def setup(self):
        for guild in self.bot.guilds:
            self.guilds[guild.id] = GuildChore(guild)
            
    

            
async def setup(bot):
    await bot.add_cog(ChoreCommands(bot))




