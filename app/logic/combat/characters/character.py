from app.logic.combat.deck.deck import Deck

class Character:
    '''
    Base class for all characters in the game.
    '''
    def __init__(self, 
                 name, 
                 cards=[],
                 health=100, 
                 attack=0, 
                 defense=0, 
                 shield=0,
                 cost=3,
                ):
        self.name = name
        self.max_health = health
        self.cur_health = health
        self.attack = attack
        self.defense = defense
        self.shield = shield
        self.cost = cost
        self.level = 1
        self.deck = Deck(
            cards=cards,
        )

    def is_dead(self):
        return self.current_health <= 0