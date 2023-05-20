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
        self.max_cost = cost
        self.level = 1
        self.deck = Deck(
            cards=cards,
        )

        # do the first card draw
        self.deck.draw_card(2)

    def is_dead(self):
        return self.cur_health <= 0