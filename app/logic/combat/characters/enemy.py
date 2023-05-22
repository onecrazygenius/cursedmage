from app.logic.combat.characters.character import Character


class Enemy(Character):
    '''
    Base class for all enemies in the game.
    '''

    def __init__(self, name, sprite="goblin"):
        super().__init__(
            name,
            filename="enemies",
            sprite=sprite
        )
