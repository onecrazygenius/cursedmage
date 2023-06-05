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
        path = os.path.dirname(os.path.abspath(__file__))
        self.font = pygame.font.Font(resource_path(path + '/../assets/fonts/cursed_font.tff'), 24)

        self.cards_to_show = []
        all_enemy_cards = []
        for enemy in enemies:
            all_enemy_cards += enemy.deck.cards

        cards_picked = random.sample(range(0, len(all_enemy_cards)), 2)
        self.cards_to_show = list(map(all_enemy_cards.__getitem__, cards_picked))

        self.button = Button("Back to Main Menu", SCREEN_WIDTH // 2, 300, self.back_to_main_menu)

    def draw(self, surface):
        # Green background for victory screen
        surface.fill((0, 255, 0))  # Black background for card pickup screen

        # Draw text
        text_surface = self.font.render("Victory!", True, (255, 255, 255))  # White text
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 200))
        surface.blit(text_surface, text_rect)
        self.button.draw(surface)
        
        # For each card available, draw it
        for i, card in enumerate(self.cards_to_show):
            # center the cards in the middle of the screen
            card_x = 100 + (100 + 100) * i
            card_y = 800
            # draw the card
            card.draw(surface, (card_x, card_y))

        # Update the display
        pygame.display.flip()

    def back_to_main_menu(self):
        self.game.show_main_menu()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            for i, card in enumerate(self.cards_to_show):
                card_x = 100 + (100 + 100) * i
                card_y = 800
                card_rect = pygame.Rect(card_x, card_y, 150, 225)
                if card_rect.collidepoint(self.game.screen_to_surface(event.pos)):
                    self.pickup_card(card)
            if self.button.rect.collidepoint(self.game.screen_to_surface(event.pos)):
                self.back_to_main_menu()

    def pickup_card(self, card):
        # Add the card to the player's deck
        self.player.deck.add_card(card)

        # Update the current room to be completed from player position
        player_x, player_y = self.game.dungeon.player_position
        room = self.game.dungeon.rooms[player_x][player_y]
        room.completed = True

        # Progress to the next room
        self.game.dungeon.progress_to_next_room()

        # Return to dungeon as room completed
        self.game.show_dungeon()
