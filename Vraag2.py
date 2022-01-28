
class Vraag:
    
    syntax = {}
    
    def __init__(self, soort, label, vraagtekst, antwoorden):
        
        self.soort = soort
        self.label = label
        self.vraagtekst = vraagtekst
        self.antwoorden = antwoorden
        self.syntax[label] = self
