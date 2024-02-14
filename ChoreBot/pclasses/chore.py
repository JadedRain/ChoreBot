class Chore():
    def __init__(self, chore, completed=False, person=None):
        self.chore = chore
        self.completed = completed
        self.person = person
        

    def get_person(self):
        return self.person
    
    def set_person(self, person):
        self.person = person
        
    def get_chore(self):
        return self.chore
    
    def complete(self):
        self.completed = True
    




