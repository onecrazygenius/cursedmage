import pygame, os
from pygame.locals import *
from app.combat.card import Card
from app.engine.components.button import Button
from app.engine.constants import *

class CardPickupScreen():
    def __init__(self, game, player):
        self.game = game
        self.player = player
        path = os.path.dirname(os.path.abspath(__file__))
        self.font = pygame.font.Font(os.path.join(path + '/../assets/fonts/cursed_font.tff'), 24)
        self.cards = [
            Card("Enemy's Card 1", 5, 0, "enemy"),
            Card("Enemy's Card 2", 50, 0, "enemy"),
        ]
        self.button = Button("Back to Main Menu", self.game.config.get_width() // 2, 300, self.back_to_main_menu)

    def draw(self):
        # Green background for victory screen
        self.game.screen.fill((0, 255, 0))  # Black background for card pickup screen

        # Draw text
        text_surface = self.font.render("Victory!", True, (255, 255, 255))  # White text
        text_rect = text_surface.get_rect(center=(self.game.config.get_width() // 2, 200))
        self.game.screen.blit(text_surface, text_rect)
        self.button.draw(self.game.screen)
        
        # Draw cards
        for i, card in enumerate(self.cards):
            card_x = CARD_START_X + (CARD_WIDTH + CARD_GAP) * i
            card_y = CARD_START_Y
            pygame.draw.rect(self.game.screen, (255, 255, 255), pygame.Rect(card_x, card_y, CARD_WIDTH, CARD_HEIGHT))
            text_surface = self.font.render(card.name, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(card_x + CARD_WIDTH // 2, card_y + CARD_HEIGHT // 2))
            self.game.screen.blit(text_surface, text_rect)

        # Update the display
        pygame.display.flip()

    def back_to_main_menu(self):
        self.game.show_main_menu()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, card in enumerate(self.cards):
                card_x = CARD_START_X + (CARD_WIDTH + CARD_GAP) * i
                card_y = CARD_START_Y
                card_rect = pygame.Rect(card_x, card_y, CARD_WIDTH, CARD_HEIGHT)
                if card_rect.collidepoint(event.pos):
                    self.pickup_card(card)
                elif self.button.rect.collidepoint(event.pos):
                    self.back_to_main_menu()

    def pickup_card(self, card):
        self.player.add_card(card)
        #Go back to dungeon screen
        self.game.pop_state()