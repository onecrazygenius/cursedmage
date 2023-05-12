from app.combat.deck.card import Card

class CursedCard(Card):
    def __init__(self):
        super().__init__(
            name="Cursed Card",
            damage=0,
            shield=0,
            target="none"
        )
        self.cursed = True
    
    def play(self, combat):
        combat.popup("You can not play a cursed card")