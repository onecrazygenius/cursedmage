from app.constants import *
from app.logic.combat.deck.card import Card
from app.states.components.button import Button
from app.states.state import State


class CursedCardPickupScreen(State):
    def __init__(self, game, player):
        super().__init__(game)
        self.game = game
        self.player = player
        path = os.path.dirname(os.path.abspath(__file__))
        self.font = pygame.font.Font(relative_resource_path("app/assets/fonts/cursed_font.tff"), 24)

        self.button = Button("OK", SCREEN_WIDTH // 2, 750, self.return_to_combat)

        # Actually pickup the cursed card
        self.pickup_card()

    def draw(self, surface):
        # Set background as background image
        background = pygame.image.load(relative_resource_path("app/assets/images/backgrounds/combat_victory.png"))
        # scale background image to fit screen
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        surface.blit(background, (0, 0))

        cursed_font = pygame.font.Font(relative_resource_path('app/assets/fonts/cursed_font.tff'), 72)

        # Draw text
        text_surface = cursed_font.render("You were cursed.", True, (255, 255, 255))  # White text
        text_rect = text_surface.get_rect()
        text_rect.center = (SCREEN_WIDTH // 2, 420)
        surface.blit(text_surface, text_rect)
        self.button.draw(surface)

        # Update the display
        pygame.display.flip()

    def return_to_combat(self):
        self.game.pop_state()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            # Check if the button was clicked
            if self.button.rect.collidepoint(self.game.screen_to_surface(event.pos)):
                self.return_to_combat()

    def pickup_card(self):
        # Add a cursed card to the player's deck
        cursed_card = Card("Cursed Card")
        self.player.deck.add_card(cursed_card)
