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
        time_format = "%H:%M"
        time_info = list(time)
        try:
            tz = str(pytz.timezone(time_info[1]))
            guild.timezone = tz
            valid_time = datetime.datetime.strptime(time_info[0], time_format).time()
            guild.announcement_time = valid_time.strftime(time_format)   
            if guild.job_started:
                self.scheduler.reschedule_job(guild.job_id, 
                                            trigger='cron',
                                            hour = valid_time.hour, 
                                            minute = valid_time.minute, 
                                            timezone = guild.timezone)
                
            await ctx.channel.send(f"Reminder successfully set to {valid_time.strftime('%I:%M %p')}-{tz}")
        except:
            await ctx.channel.send("Failed to change reminder time. Remember to use military time in the format HH:MM TZ (09:30 MST)")

    
    @commands.command(name="start")
    async def start_chore_announcement(self, ctx):
        guild = self.get_guild(ctx.guild)
        time = datetime.datetime.strptime(guild.announcement_time, '%H:%M').time()
        if guild.job_started: 
            return
        else:
            self.scheduler.add_job(self.show_chores_scheduled, 
                                                 'cron', 
                                                 hour = time.hour, 
                                                 minute = time.minute, 
                                                 timezone = guild.timezone, 
                                                 args = [ctx], 
                                                 id = guild.job_id)

            guild.job_toggle()
            
    @commands.command(name="stop")
    async def stop_chore_announcement(self, ctx):
        guild = self.get_guild(ctx.guild)
        if not guild.job_started:
            return
        else:
            self.scheduler.remove_job(guild.job_id)
            guild.job_toggle()
            
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
    async def save_data(self, ctx):
        guild = self.get_guild(ctx.guild)
        with open(f"data/{guild.guild_id}.json", "w+") as write_file:
            json.dump(guild, default=lambda o: o.__dict__, fp=write_file, indent=4)
        await ctx.channel.send("It worked")
         
            
    async def show_chores_scheduled(self, ctx):
        guild = self.get_guild(ctx.guild)
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
            
    def setup(self):
        for guild in self.bot.guilds:
            self.guilds[guild.id] = GuildChore(guild)
        self.scheduler.start()
            
    def get_guild(self, guild):
        return self.guilds[guild.id]
            
async def setup(bot):
    await bot.add_cog(ChoreCommands(bot))




