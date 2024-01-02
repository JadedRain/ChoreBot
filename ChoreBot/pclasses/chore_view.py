import discord
import discord.ui

class ChoreView(discord.ui.View):
    page_length = 5
    chore_pages = []
    

    def __init__(self):
        super().__init__(timeout=60)
        self.current_page = 0
        self.chore_list_embed = None


    def create_pages(self, chores):
        self.chore_pages = []
        def page_setup():
            embed = discord.Embed()
            embed.title = "Weekly Chore To Do List"
            embed.description = "Chores to get done this week."
            embed.color = 0xBDECB6
            embed.set_footer(text=f"Page {len(self.chore_pages) + 1}")
            return embed
            
        page = page_setup()
        for chore in chores:
             if chore.get_person() == None:
                 page.add_field(name = f"Chore: {chore.get_chore()}", value = f"Person: Unassigned \n Completed: {('No', 'Yes')[int(chore.completed)]}")
             else:
                 page.add_field(name = f"Chore: {chore.get_chore()}", value = f"Person: <@{chore.get_person()}> \n Completed: {('No', 'Yes')[int(chore.completed)]}")    
             if len(page.fields) == self.page_length:
                 self.chore_pages.append(page)
                 page = page_setup()
        if len(page.fields):
            self.chore_pages.append(page)
        
        self.chore_list_embed = self.chore_pages[0]
    
    @discord.ui.button(label="Prev Page")
    async def previous_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page -= 1
        if self.current_page < 0:
            self.current_page = len(self.chore_pages) - 1
        await interaction.message.edit(embed=self.chore_pages[self.current_page])
        await interaction.response.defer()
        
    @discord.ui.button(label="Next Page")
    async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page += 1
        if self.current_page >= len(self.chore_pages):
            self.current_page = 0
        await interaction.message.edit(embed=self.chore_pages[self.current_page])
        await interaction.response.defer()
        
             
             

