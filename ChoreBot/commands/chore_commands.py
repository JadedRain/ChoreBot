import datetime
import json
import pytz
import random
from discord.ext import commands
from pclasses.chore import Chore
from pclasses.guild_chores import GuildChore
from apscheduler.schedulers.asyncio import AsyncIOScheduler


class ChoreCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.time_format = '%H:%M'
        self.default_channel = "general"
        self.guilds = {}
        self.scheduler = AsyncIOScheduler()
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.setup()
        await self.load_all_guilds()
        self.scheduler.add_job(self.auto_save, 
                               'cron', 
                               hour = '*', 
                               id = "autosave")
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
        if after.id in self.get_role_members(after):
            guild.add_person(after)
        elif after.id not in self.get_role_members(before) and before.id in self.get_role_members(before):
            guild.remove_person(after)
         
        
    @commands.command(name="addchore")
    async def add_chore(self, ctx, *chore_name):
        if ctx.message.author.guild_permissions.administrator:
            c = Chore(' '.join(chore_name[:]).title())
            self.guilds[ctx.guild.id].add_chore(c)
    
    @commands.command(name="rmchore")
    async def remove_chore(self, ctx, *chore_name):
        if ctx.message.author.guild_permissions.administrator:
            if self.guilds[ctx.guild.id].remove_chore(' '.join(chore_name[:])):
                await ctx.channel.send(f"{' '.join(chore_name[:]).title()} removed.")
    
    @commands.command(name="shchores")
    async def show_chores_command(self, ctx):
        guild = self.get_guild(ctx.guild)
        view = guild.get_view()
        view.create_pages(guild.chore_list)
        if len(view.chore_pages) > 0:
            await ctx.channel.send(embed=view.chore_list_embed, view = view)
        
    @commands.command(name="setchan")
    async def set_announcement_channel(self, ctx):
        if ctx.message.author.guild_permissions.administrator:
            self.guilds[ctx.guild.id].set_announcement(ctx.channel.id)
            await ctx.channel.send("Channel has been set")
        
    @commands.command(name="settime")
    async def set_guild_schedule_time(self, ctx, *time):
        if ctx.message.author.guild_permissions.administrator:
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
    async def start_announcement_command(self, ctx):
        if ctx.message.author.guild_permissions.administrator:
            guild = self.get_guild(ctx.guild)
            if guild.job_started: 
                return
            else:
                await self.start_job(guild)
            
    @commands.command(name="stop")
    async def stop_announcement_command(self, ctx):
        if ctx.message.author.guild_permissions.administrator:
            guild = self.get_guild(ctx.guild)
            if not guild.job_started:
                return
            else:
                await self.stop_job(guild)
            
    @commands.command(name="assign")
    async def assign_command(self, ctx):
        if ctx.message.author.guild_permissions.administrator:
            guild = self.get_guild(ctx.guild)
            self.assign(guild)
            
    @commands.command(name="complete")
    async def complete_command(self, ctx, *chore):
        guild = self.get_guild(ctx.guild)
        for c in guild.chore_list:
            if c.get_chore() == ' '.join(chore[:]).title() and ctx.author.id == c.get_person():
                c.complete()
    
    @commands.command(name="save")
    async def save_command(self, ctx):
        if ctx.message.author.guild_permissions.administrator:
            guild = self.get_guild(ctx.guild)
            await self.save_data(guild.guild_id, guild)
            await ctx.channel.send("Chore information has been saved.")
        
    @commands.command(name="load")
    async def load_command(self, ctx):
        if ctx.message.author.guild_permissions.administrator:
            guild = self.get_guild(ctx.guild)
            await self.load(guild)
            await ctx.channel.send("Chore information has been loaded.")
    
       
    async def show_chores_scheduled(self, guild):
        view = guild.get_view()
        view.create_pages(guild.chore_list)
        if len(view.chore_pages) > 0:
            channel = None
            if guild.announcement_channel:
                channel = self.bot.get_channel(guild.announcement_channel)
            else:
                self.bot.get_guild
                for c in self.bot.get_guild(guild.guild_id).text_channels:
                    if c.name.lower() == self.default_channel:
                        channel = c
                        break
            await channel.send(embed=view.chore_list_embed, view = view)
            
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
        return data
    
    async def job_load(self, guild, data):
            # check if a job was started during last save. if so then start job again
            if data["job_started"] and not self.scheduler.get_job(data["job_id"]):
                await self.start_job(guild)
            elif not data["job_started"] and self.scheduler.get_job(data["job_id"]):
                await self.stop_job(guild)
      
    async def load_all_guilds(self):
        for id in self.guilds:
            guild = self.guilds[id]
            await self.load(guild)
          
        
    
    async def load(self, guild):
            data = await self.load_data(guild.guild_id, guild)
            guild.load_data(data)
            await self.job_load(guild, data)

    async def auto_save(self):
        for id in self.guilds:
            guild = self.guilds[id]
            await self.save_data(id, guild)
        
            
    def setup(self):
        for guild in self.bot.guilds:
            self.guilds[guild.id] = GuildChore(guild)
        self.scheduler.add_job(self.assign_job,
                               'cron',
                               day_of_week = 'mon',
                               hour = 9,
                               timezone = 'mst')
        self.scheduler.start()
        
    def assign(self, guild):
        temp1 = list(guild.person_list.keys())
        temp2 = []
        use_list_one = True
        for chore in guild.chore_list:
            if use_list_one:
                person = random.choice(temp1)
                temp1.remove(person)
                temp2.append(person)
                if len(temp1) == 0:
                    use_list_one = False
            else:
                person = random.choice(temp2)
                temp2.remove(person)
                temp1.append(person)
                if len(temp2) == 0:
                    use_list_one = True
            
            chore.set_person(person)
    
    def assign_job(self):
        for guild in self.guilds:
            self.assign(guild)
            
    def get_guild(self, guild):
        return self.guilds[guild.id]
    
    def get_role_members(self, before):
        member_ids = []
        for member in before.guild.get_role(self.get_guild(before.guild).chore_role_id).members:
            member_ids.append(member.id)
        return member_ids
            
async def setup(bot):
    await bot.add_cog(ChoreCommands(bot))




