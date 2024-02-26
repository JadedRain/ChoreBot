
class GuildInfo():
    count = 0

    def __init__(self, bot_guilds):
        self.bot_guilds = bot_guilds
        self.count_guilds()

    def count_guilds(self):
        for guild in self.bot_guilds:
            self.count+=1
    def get_guilds(self):
        g = []
        for guild in self.bot_guilds:
            g.append(guild.name)
        return g
    
    async def list_guild_info(self):
        for guild in self.bot_guilds:
            print(f"- {guild.id} (name: {guild.name})")
        print(f"\nBot is currently running in {self.count} servers.\n")
        
    




