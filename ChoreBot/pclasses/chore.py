class Chore():
    def __init__(self, person, chore):
        self.person = person
        self.chore = chore
        self.completed = False
        

    def get_person(self):
        return self.person
    
    def set_person(self, person):
        self.person = person
        
    def get_chore(self):
        return self.chore
    




