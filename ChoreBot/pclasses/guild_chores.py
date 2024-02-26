import discord
import datetime
import pytz
from pclasses.chore import Chore
from pclasses.chore_view import ChoreView

class GuildChore:
    def __init__(self, guild):    
        self.guild_id = guild.id;
        self.guild_name = guild.name; 
        self.chore_list = []
        self.person_list = {}
        self.announcement_channel = None
        self.announcement_time = datetime.time(hour = 9, minute = 30).strftime('%H:%M')
        self.timezone = "UTC"
        self.chore_role_name = "roommate"
        self.chore_role_id = discord.utils.find(lambda r: r.name.lower() == self.chore_role_name, guild.roles).id
        self.job_started = False
        self.job_id = str(self.guild_id)
        self.person_setup(guild)        

    def add_chore(self, chore):
        self.chore_list.append(chore)
    
    def remove_chore(self, chore_name):
        for chore in self.chore_list:
            if chore.get_chore().lower() == chore_name.lower():
                self.chore_list.remove(chore)
                return True
        return False
    
    def add_person(self, member):
        self.person_list[member.id] = member.display_name
                
    def remove_person(self, member):
        member_name = self.person_list.pop(str(member.id))
        for chore in self.chore_list:
            if chore.get_person() == member_name:
                chore.set_person(None)
    
    def get_view(self):
        return ChoreView()       

    def set_announcement(self, channel):
        self.announcement_channel = channel

    def job_toggle(self):
        self.job_started = not self.job_started
        
    def load_data(self, data):
        self.chore_list.extend(self.load_chores(data["chore_list"]))
        self.person_list = data["person_list"]
        self.announcement_channel = data["announcement_channel"]
        self.announcement_time = data["announcement_time"]
        self.timezone = data["timezone"]
        self.chore_role_name = data["chore_role_name"]
        self.chore_role_id = data["chore_role_id"]
        self.job_started = data["job_started"]
        
    def load_chores(self, chores):
        return list(map(lambda c: Chore(c["chore"], c["completed"], c["person"]), chores))



    # adds users to pick from for chores
    def person_setup(self, guild):
        role = guild.get_role(self.chore_role_id)
        for member in role.members:
            self.person_list[member.id] = member.display_name

