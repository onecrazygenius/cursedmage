import os
import random

from app.constants import *
from app.states.components.button import Button
from app.states.state import State


class CardPickupScreen(State):
    def __init__(self, game, player, enemies):
        super().__init__(game)
        self.game = game
        self.player = player
        self.enemies = enemies
        self.font = pygame.font.Font(relative_resource_path('app/assets/fonts/cursed_font.tff'), 24)

        self.cards_to_show = []
        all_enemy_cards = []
        for enemy in enemies:
            all_enemy_cards += enemy.deck.cards

        # If the enemy only has 1 card in the JSON file - this will break!
        cards_picked = random.sample(range(0, len(all_enemy_cards)), 2)
        self.cards_to_show = list(map(all_enemy_cards.__getitem__, cards_picked))

        self.button = Button("Back to Main Menu", SCREEN_WIDTH // 2, 950, self.back_to_main_menu)

    def draw(self, surface):
        # Set background as background image
        background = pygame.image.load(relative_resource_path("app/assets/images/backgrounds/combat_victory.png"))
        # scale background image to fit screen
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        surface.blit(background, (0, 0))

        # Draw text
        victory_font = pygame.font.Font(relative_resource_path('app/assets/fonts/cursed_font.tff'), 72)
        pickup_font = pygame.font.Font(relative_resource_path('app/assets/fonts/cursed_font.tff'), 40)

        text_surface = victory_font.render("Victory!", True, (255, 255, 255))  # White text
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 400))
        surface.blit(text_surface, text_rect)

        text_surface = pickup_font.render("Pickup an Enemy Card", True, (255, 255, 255))  # White text
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 450))
        surface.blit(text_surface, text_rect)
        self.button.draw(surface)

        # For each card available, draw it
        for i, card in enumerate(self.cards_to_show):
            # center the cards in the middle of the screen
            card_x = 785 + (100 + 100) * i
            card_y = 650
            # draw the card
            card.draw(surface, (card_x, card_y))

        # Update the display
        pygame.display.flip()

    def back_to_main_menu(self):
        self.game.show_main_menu()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            for i, card in enumerate(self.cards_to_show):
                card_x = 785 + (100 + 100) * i
                card_y = 650
                card_rect = pygame.Rect(card_x, card_y, 150, 225)
                if card_rect.collidepoint(self.game.screen_to_surface(event.pos)):
                    self.pickup_card(card)
            if self.button.rect.collidepoint(self.game.screen_to_surface(event.pos)):
                self.back_to_main_menu()

    def pickup_card(self, card):
        # Add the card to the player's deck
        self.player.deck.add_card(card)

        self.game.dungeon.progress_to_next_room()

        # Return to dungeon as room completed
        self.game.show_dungeon()
