import datetime
import discord
import discord.ui
import json
import pytz
import random
from discord.ext import commands
from pclasses.chore import Chore
from pclasses.guild_chores import GuildChore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger


class ChoreCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.time_format = '%H:%M'
        self.guilds = {}
        self.scheduler = AsyncIOScheduler()
    
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
        
    # Add event listener for when roles update.
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        guild = self.get_guild(before.guild)
        if after.id in before.guild.get_role(guild.chore_role_id).members:
            guild.add_person(after)
        elif after.id not in before.guild.get_role(guild.chore_role_id).members:
            guild.remove_person(after)
        
    @commands.command(name="addchore")
    async def add_chore(self, ctx, *chore_name):
        c = Chore(' '.join(chore_name[:]).title())
        self.guilds[ctx.guild.id].add_chore(c)
    
    @commands.command(name="rmchore")
    async def remove_chore(self, ctx, *chore_name):
        self.guilds[ctx.guild.id].remove_chore(' '.join(chore_name[:]))
    
    @commands.command(name="shchores")
    async def show_chores_command(self, ctx):
        guild = self.get_guild(ctx.guild)
        view = guild.get_view()
        view.create_pages(guild.chore_list)
        if len(view.chore_pages) > 0:
            await ctx.channel.send(embed=view.chore_list_embed, view = view)
        
    @commands.command(name="setchan")
    async def set_announcement_channel(self, ctx):
        self.guilds[ctx.guild.id].set_announcement(ctx.channel.id)
        await ctx.channel.send("Channel has been set")
        
    @commands.command(name="settime")
    async def set_guild_schedule_time(self, ctx, *time):
        guild = self.get_guild(ctx.guild)
        time_info = list(time)
        try:
            guild.timezone = str(pytz.timezone(time_info[1]))
            valid_time = datetime.datetime.strptime(time_info[0], self.time_format).time()
            guild.announcement_time = valid_time.strftime(self.time_format)   
            if guild.job_started:
                await self.change_job_time(guild)
                
            await ctx.channel.send(f"Reminder successfully set to {valid_time.strftime('%I:%M %p')}-{guild.timezone}")
        except:
            await ctx.channel.send("Failed to change reminder time. Remember to use military time in the format HH:MM TZ (09:30 MST)")

    
    @commands.command(name="start")
    async def start_chore_announcement(self, ctx):
        guild = self.get_guild(ctx.guild)
        if guild.job_started: 
            return
        else:
            await self.start_job(guild)
            
    @commands.command(name="stop")
    async def stop_chore_announcement(self, ctx):
        guild = self.get_guild(ctx.guild)
        if not guild.job_started:
            return
        else:
            await self.stop_job(guild)
            
    @commands.command(name="assign")
    async def assign_chores(self, ctx):
        guild = self.get_guild(ctx.guild)
        for chore in guild.chore_list:
            chore.set_person(random.choice(list(guild.person_list.keys())))
            
    @commands.command(name="complete")
    async def complete_chore(self, ctx, *chore):
        guild = self.get_guild(ctx.guild)
        for c in guild.chore_list:
            if c.get_chore() == ' '.join(chore[:]).title() and ctx.author.id == c.get_person():
                c.complete()
    
    @commands.command(name="save")
    async def save_command(self, ctx):
        guild = self.get_guild(ctx.guild)
        await self.save_data(guild.guild_id, guild)
        await ctx.channel.send("Chore information has been saved.")
        
    @commands.command(name="load")
    async def load_command(self, ctx):
        guild = self.get_guild(ctx.guild)
        await self.load_data(guild.guild_id, guild)
        await ctx.channel.send("Chore information has been loaded.")
         
            
    async def show_chores_scheduled(self, guild):
        guild.chore_view.create_pages(guild.chore_list)
        embed = guild.chore_view.chore_list_embed
        view = guild.chore_view
        if len(view.chore_pages) > 0:
            channel = None
            if guild.announcement_channel:
                channel = self.bot.get_channel(guild.announcement_channel)
            else:
                for c in guild.guild.text_channels:
                    if c.name.lower() == "general":
                        channel = c
                        break
            await channel.send(embed=embed, view = view)
            
    async def start_job(self, guild):
        time = datetime.datetime.strptime(guild.announcement_time, self.time_format).time()
        self.scheduler.add_job(self.show_chores_scheduled, 
                               'cron', 
                               hour = time.hour, 
                               minute = time.minute, 
                               timezone = guild.timezone, 
                               args = [guild], 
                               id = guild.job_id)
        guild.job_toggle()
        
    async def stop_job(self, guild):
        self.scheduler.remove_job(guild.job_id)
        guild.job_toggle()
    
    async def change_job_time(self, guild):
        time = datetime.datetime.strptime(guild.announcement_time, self.time_format).time()
        self.scheduler.reschedule_job(guild.job_id, 
                                      trigger='cron',
                                      hour = time.hour, 
                                      minute = time.minute, 
                                      timezone = guild.timezone)
       
    async def save_data(self, file, data):
        with open(f"data/{file}.json", "w+") as write_file:
            json.dump(data, default=lambda o: o.__dict__, fp=write_file, indent=4)
            
    async def load_data(self, file, guild):
        with open(f"data/{file}.json", "r") as read_file:
            data = json.load(read_file)
            
        guild.load_data(data)
        
        # check if a job was started during last save. if so then start job again
        if data["job_started"] and not self.scheduler.get_job(data["job_id"]):
            await self.start_job(guild)
        elif not data["job_started"] and self.scheduler.get_job(data["job_id"]):
            await self.stop_job(guild)
            
    def setup(self):
        for guild in self.bot.guilds:
            self.guilds[guild.id] = GuildChore(guild)
        self.scheduler.start()
            
    def get_guild(self, guild):
        return self.guilds[guild.id]
            
async def setup(bot):
    await bot.add_cog(ChoreCommands(bot))




