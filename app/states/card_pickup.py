import pygame, os
from pygame.locals import *
from app.logic.combat.deck.card import Card
from app.states.components.button import Button
from app.constants import *
from app.states.state import State

class CardPickupScreen(State):
    def __init__(self, game, player):
        super().__init__(game)

        self.game = game
        self.player = player
        path = os.path.dirname(os.path.abspath(__file__))
        self.font = pygame.font.Font(os.path.join(path + '/../assets/fonts/cursed_font.tff'), 24)

        self.cards = [
            Card("Enemy's Card 1", 5, 0, "enemy"),
            Card("Enemy's Card 2", 50, 0, "enemy"),
        ]

        self.button = Button("Back to Main Menu", self.game.config.get_width() // 2, 300, self.back_to_main_menu)

    def draw(self, surface):
        # Green background for victory screen
        surface.fill((0, 255, 0))  # Black background for card pickup screen

        # Draw text
        text_surface = self.font.render("Victory!", True, (255, 255, 255))  # White text
        text_rect = text_surface.get_rect(center=(self.game.config.get_width() // 2, 200))
        surface.blit(text_surface, text_rect)
        self.button.draw(surface)
        
        # Draw cards
        for i, card in enumerate(self.cards):
            card_x = 100 + (100 + 100) * i
            card_y = 100
            pygame.draw.rect(surface, (255, 255, 255), pygame.Rect(card_x, card_y, 100, 100))
            text_surface = self.font.render(card.name, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(card_x + 100 // 2, card_y + 100 // 2))
            surface.blit(text_surface, text_rect)

        # Update the display
        pygame.display.flip()

    def back_to_main_menu(self):
        self.game.show_main_menu()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            for i, card in enumerate(self.cards):
                card_x = 100 + (100 + 100) * i
                card_y = 100
                card_rect = pygame.Rect(card_x, card_y, 100, 100)
                if card_rect.collidepoint(self.game.screen_to_canvas(event.pos)):
                    print("Picked up card")
                    self.pickup_card(card)
            if self.button.rect.collidepoint(self.game.screen_to_canvas(event.pos)):
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
