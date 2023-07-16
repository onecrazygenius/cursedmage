from app.logic.combat.characters.character import Character


class Boss(Character):
    '''
    Base class for bosses in the game.
    '''

    def __init__(self, name):
        super().__init__(
            name,
            filename="bosses"
        )
