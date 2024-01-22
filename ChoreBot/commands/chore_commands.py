import logging
import datetime
import discord
import discord.ui
import pytz
import random
import re
from discord.ext import commands, tasks
from discord.ui import view
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
        guild = before.guild
        if after.id in self.guilds[guild.id].chore_role.members:
            self.guilds[guild.id].add_person(after)
        elif after.id not in self.guilds[guild.id].chore_role.members:
            self.guilds[guild.id].remove_person(after)
        
    @commands.command(name="addchore")
    async def add_chore(self, ctx, *chore_name):
        c = Chore(' '.join(chore_name[:]).title())
        self.guilds[ctx.guild.id].add_chore(c)
    
    @commands.command(name="rmchore")
    async def remove_chore(self, ctx, *chore_name):
        self.guilds[ctx.guild.id].remove_chore(' '.join(chore_name[:]))
    
    @commands.command(name="shchores")
    async def show_chores_command(self, ctx):
        guild = self.get_guild(ctx)
        guild.chore_view.create_pages(guild.chore_list)
        embed = guild.chore_view.chore_list_embed
        view = guild.chore_view
        if len(view.chore_pages) > 0:
            await ctx.channel.send(embed=embed, view = view)
        
    @commands.command(name="setchan")
    async def set_announcement_channel(self, ctx):
        self.guilds[ctx.guild.id].set_announcement(ctx.channel.id)
        await ctx.channel.send("Channel has been set")
        
    @commands.command(name="settime")
    async def set_guild_schedule_time(self, ctx, *time):
        guild = self.get_guild(ctx)
        time_format = "%H:%M"
        time_info = list(time)
        try:
            tz = pytz.timezone(time_info[1])
            valid_time = datetime.datetime.strptime(time_info[0], time_format).time()
            guild.announcement_time = valid_time
            guild.timezone = tz
            await ctx.channel.send(f"Reminder successfully set to {valid_time.strftime('%I:%M %p')}-{tz}")
        except:
            await ctx.channel.send("Failed to change reminder time. Remember to use military time in the format HH:MM TZ (09:30 MST)") 
    
    
    @commands.command(name="start")
    async def start_chore_announcement(self, ctx):
        guild = self.get_guild(ctx)
        if guild.job_started: 
            return
        else:
            guild.set_job(self.scheduler.add_job(self.show_chores_scheduled, 'cron', 
                                                                     hour = guild.announcement_time.hour, 
                                                                     minute = guild.announcement_time.minute, 
                                                                     timezone = guild.timezone, 
                                                                     args = [ctx], 
                                                                     id = str(guild.guild.id)))

            guild.job_toggle()
            
    @commands.command(name="stop")
    async def stop_chore_announcement(self, ctx):
        guild = self.get_guild(ctx)
        if not guild.job_started:
            return
        else:
            self.scheduler.remove_job(guild.pop_job())
            guild.job_toggle()
            
    @commands.command(name="assign")
    async def assign_chores(self, ctx):
        guild = self.get_guild(ctx)
        for chore in guild.chore_list:
            chore.set_person(random.choice(list(guild.person_list.keys())))
            
    @commands.command(name="complete")
    async def complete_chore(self, ctx, *chore):
        guild = self.get_guild(ctx)
        for c in guild.chore_list:
            if c.get_chore() == ' '.join(chore[:]).title() and ctx.author.id == c.get_person():
                c.complete()
            
    async def show_chores_scheduled(self, ctx):
        guild = self.get_guild(ctx)
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
            
    def get_guild(self, ctx):
        return self.guilds[ctx.guild.id]
            
async def setup(bot):
    await bot.add_cog(ChoreCommands(bot))




