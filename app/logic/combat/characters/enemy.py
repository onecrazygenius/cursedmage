from app.logic.combat.characters.character import Character


class Enemy(Character):
    '''
    Base class for all enemies in the game.
    '''

    def __init__(self):
        super().__init__(
            name="Goblin",
            filename="enemies"
        )
