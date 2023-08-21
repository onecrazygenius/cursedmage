import random

from app.constants import *
from app.logic.combat.deck.card import Card
from app.states.components.button import Button
from app.states.state import State


class UpgradeCardScreen(State):
    def __init__(self, game, player):
        super().__init__(game)
        self.game = game
        self.player = player
        self.font = pygame.font.Font(relative_resource_path('app/assets/fonts/cursed_font.tff'), 24)

        self.cards_to_show = []
        self.hovered_card = None

        filtered_cards = [card for card in player.deck.cards if card.cursed or (card.upgrades_to != "MAXLEVEL" and card.upgrades_to != "None")]
        self.cards_to_show = filtered_cards  # This means if there is less than 4 cards, all are picked
        if len(filtered_cards) >= 4:
            self.cards_to_show = random.sample(filtered_cards, 4)

        self.button = Button("Back to Main Menu", SCREEN_WIDTH // 2, 950, self.back_to_main_menu)

    def draw(self, surface):
        # Set background as background image
        background = pygame.image.load(relative_resource_path("app/assets/images/backgrounds/brick.png"))
        # scale background image to fit screen
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        surface.blit(background, (0, 0))

        # Draw text
        victory_font = pygame.font.Font(relative_resource_path('app/assets/fonts/cursed_font.tff'), 72)

        text_surface = victory_font.render("Choose a Card to Upgrade", True, (255, 255, 255))  # White text
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
        surface.blit(text_surface, text_rect)

        self.button.draw(surface)

        # For each card available, draw it
        for i, card in enumerate(self.cards_to_show):
            # center the cards in the middle of the screen
            card_x = 585 + (100 + 100) * i
            card_y = 450
            # Draw the Card. If the card can be upgraded show the upgraded card
            if i == self.hovered_card:
                if card.cursed:
                    card.draw(surface, (card_x, card_y), 1.2, opacity=0.6)
                else:
                    card = Card(card.upgrades_to)
                    card.draw(surface, (card_x, card_y), 1.2)
            else:
                # These are cursed cards
                card.draw(surface, (card_x, card_y))

        # Update the display
        pygame.display.flip()

    def back_to_main_menu(self):
        self.game.show_main_menu()

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            # Make the card bigger when the mouse is over it
            # set self.hovered_card to the card that is being hovered over
            for i, card in enumerate(self.cards_to_show):
                card_x = 585 + (100 + 100) * i
                card_y = 450
                card_rect = pygame.Rect(card_x, card_y, 150, 225)
                if card_rect.collidepoint(self.game.screen_to_surface(event.pos)):
                    self.hovered_card = i
                    break
            # if the card is no longer being hovered over, set self.hovered_card to None
            else:
                self.hovered_card = None

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            for i, card in enumerate(self.cards_to_show):
                card_x = 585 + (100 + 100) * i
                card_y = 450
                card_rect = pygame.Rect(card_x, card_y, 150, 225)
                if card_rect.collidepoint(self.game.screen_to_surface(event.pos)):
                    self.upgrade_card(card)
            if self.button.rect.collidepoint(self.game.screen_to_surface(event.pos)):
                self.back_to_main_menu()

    def upgrade_card(self, card):
        # Remove the old card and add the new card to the players deck
        # If they clicked a cursed card just remove it
        if card.cursed:
            self.player.deck.remove_card(card)
        else:
            self.player.deck.remove_card(card)
            self.player.deck.add_card(Card(card.upgrades_to))

        self.game.dungeon.progress_to_next_room()

        # Return to dungeon as room completed
        self.game.show_dungeon()
