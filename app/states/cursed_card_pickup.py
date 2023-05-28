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
        self.font = pygame.font.Font(resource_path("app/assets/fonts/cursed_font.tff"), 24)

        self.button = Button("OK", self.game.config.get_width() // 2, 300, self.return_to_combat)

        # Actually pickup the cursed card
        self.pickup_card()

    def draw(self, surface):
        # Red background for card pickup screen
        surface.fill((255, 0, 0))

        # Draw text
        text_surface = self.font.render("You were cursed.", True, (255, 255, 255))  # White text
        text_rect = text_surface.get_rect(center=(self.game.config.get_width() // 2, 200))
        surface.blit(text_surface, text_rect)
        self.button.draw(surface)

        # Update the display
        pygame.display.flip()

    def return_to_combat(self):
        self.game.pop_state()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            # Check if the button was clicked
            if self.button.rect.collidepoint(self.game.screen_to_canvas(event.pos)):
                self.return_to_combat()

    def pickup_card(self):
        # Add a cursed card to the player's deck
        cursed_card = Card("Cursed Card")
        self.player.deck.add_card(cursed_card)
