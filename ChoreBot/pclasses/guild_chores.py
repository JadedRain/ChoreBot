import discord
from pclasses.chore import Chore

class GuildChore:
    def __init__(self, guild):    
        self.guild = guild;
        self.chore_list = []
        self.person_list = {}
        self.person_setup()
        

    def add_chore(self, chore):
        self.chore_list.append(chore)

    # adds users to pick from for chores
    def person_setup(self):
        role = discord.utils.find(lambda r: r.name.lower() == "roommate", self.guild.roles)
        for member in self.guild.members:
            if role in member.roles:
                self.person_list[member.display_name] = member.id
