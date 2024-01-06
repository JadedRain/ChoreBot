import discord
from pclasses.chore import Chore
from pclasses.chore_view import ChoreView

class GuildChore:
    def __init__(self, guild):    
        self.guild = guild;
        self.chore_list = []
        self.person_list = {}
        self.chore_view = ChoreView()
        # self.chore_view
        self.chore_role_name = "roommate"
        self.chore_role = discord.utils.find(lambda r: r.name.lower() == self.chore_role_name, self.guild.roles)
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

    # adds users to pick from for chores
    def person_setup(self):
        for member in self.chore_role.members:
            self.person_list[member.id] = member.display_name

