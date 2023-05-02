from app.combat.card import Card

class CursedCard(Card):
    def __init__(self):
        self.name = "Cursed Card"
    
    def play(self, combat):
        combat.popup("You can not play a cursed card")