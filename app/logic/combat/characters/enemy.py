from app.logic.combat.characters.character import Character

class Enemy(Character):

    '''
    Base class for all enemies in the game.
    '''
    def __init__(self):
        super().__init__(
            name="Goblin",
            health=100,
            attack=10,
            defense=5,
            shield=0,
            cost=3,
            filename="enemies"
        )