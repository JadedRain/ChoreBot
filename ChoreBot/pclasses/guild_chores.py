import discord
import datetime
import pytz
from pclasses.chore import Chore
from pclasses.chore_view import ChoreView

class GuildChore:
    def __init__(self, guild):    
        self.guild = guild;
        self.chore_list = []
        self.person_list = {}
        self.chore_view = ChoreView()
        self.announcement_channel = None
        self.announcement_time = datetime.time(hour = 9, minute = 30)
        self.timezone = pytz.timezone("UTC")
        self.chore_role_name = "roommate"
        self.chore_role = discord.utils.find(lambda r: r.name.lower() == self.chore_role_name, self.guild.roles)
        self.job_started = False
        self.job = None
        self.person_setup()
        

    def add_chore(self, chore):
        self.chore_list.append(chore)
    
    def remove_chore(self, chore_name):
        for chore in self.chore_list:
            if chore.get_chore().lower() == chore_name:
                self.chore_list.remove(chore)
    
    def add_person(self, member):
        self.person_list[member.id] = member.display_name
                
    def remove_person(self, member):
        member_name = self.person_list.pop(member.id)
        for chore in self.chore_list:
            if chore.get_person() == member_name:
                chore.set_person(None)
                
    def set_announcement(self, channel):
        self.announcement_channel = channel
        
    def set_job(self, job):
        self.job = job
    
    def pop_job(self):
        t = self.job.id
        self.job = None
        return t

    def job_toggle(self):
        self.job_started = not self.job_started

    # adds users to pick from for chores
    def person_setup(self):
        for member in self.chore_role.members:
            self.person_list[member.id] = member.display_name

