import discord
from pclasses.chore import Chore
from pclasses.chore_view import ChoreView

class GuildChore:
    def __init__(self, guild):    
        self.guild = guild;
        self.chore_list = []
        self.person_list = {}
        self.chore_view = ChoreView()
        self.person_setup()
        

    def add_chore(self, chore):
        self.chore_list.append(chore)
    
    def remove_chore(self, chore_name):
        for chore in self.chore_list:
            if chore.get_chore().lower() == chore_name:
                self.chore_list.remove(chore)

    # adds users to pick from for chores
    def person_setup(self):
        role = discord.utils.find(lambda r: r.name.lower() == "roommate", self.guild.roles)
        for member in self.guild.members:
            if role in member.roles:
                self.person_list[member.display_name] = member.id
