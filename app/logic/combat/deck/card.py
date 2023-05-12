import pygame, os

class Card:

    '''
    Card class for the game
    '''
    def __init__(self, 
                 name, 
                 card_type, 
                 power=1,
                 cost=1, 
                 description="", 
                 target="enemy", 
                 image="", 
                 cursed=False,
                 position=(0,0)
            ):
        self.name = name
        self.card_type = card_type
        self.power = power
        self.cost = cost
        self.description = description
        self.target = target
        self.image = image
        self.cursed = cursed
        self.position = position

    def draw(self, screen, position=None):
        # Position set to default if not specified
        if position is None:
            position = self.position
        self.position = position
        
        # Draw the card on the screen
        pygame.draw.rect(screen, (255, 255, 255), (position[0], position[1], 100, 150))
        
        # Load the font
        path = os.path.dirname(os.path.abspath(__file__))
        font = pygame.font.Font(os.path.join(path + '/../assets/fonts/cursed_font.tff'), 20)
        # Render text
        text = font.render(self.name, True, (0, 0, 0))

        # Blit the text to the screen
        screen.blit(text, (position[0] + 10, position[1] + 10))
