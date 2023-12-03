class Chore():
    def __init__(self, chore):
        self.chore = chore
        self.completed = False
        self.person = None
        

    def get_person(self):
        return self.person
    
    def set_person(self, person):
        self.person = person
        
    def get_chore(self):
        return self.chore
    




