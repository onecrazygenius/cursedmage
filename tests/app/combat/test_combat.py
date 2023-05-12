import unittest
from unittest.mock import MagicMock, call
from unittest.mock import patch

import pygame
import pytest

from app.combat.deck.card import Card
from app.states.combat import Combat
from app.constants import HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT, PLAYER_HEALTH_COLOR, ENEMY_HEALTH_COLOR, \
    SCREEN_WIDTH, CARD_START_X, CARD_START_Y
from app.states.main_menu import MainMenu
from app.menus.victory_screen import VictoryScreen


class TestCombat(unittest.TestCase):

    def setUp(self):
        self.dungeon = MagicMock(player_position=(0, 0))
        self.game = MagicMock()
        self.game.dungeon = self.dungeon
        self.player = MagicMock(max_health=100, hand=[
            Card(target="enemy", damage=5, shield=0, name="Fireball"),
            Card(target="player", damage=3, shield=0, name="Meteor"),
            Card(target="enemy", damage=8, shield=0, name="Eruption"),
            Card(target="player", damage=0, shield=4, name="Shield Of Fate"),
            Card(target="enemy", damage=0, shield=6, name="Shield Of Destiny"),
        ])
        self.enemy = MagicMock(max_health=100)
        self.combat = Combat(self.game, self.player, self.enemy)

    def test_apply_damage_to_enemy(self):
        self.combat.apply_damage(20, 'enemy')
        self.assertEqual(self.combat.enemy_health, 80)

    def test_apply_damage_to_enemy_stacked(self):
        self.combat.apply_damage(20, 'enemy')
        self.assertEqual(self.combat.enemy_health, 80)
        self.combat.apply_damage(35, 'enemy')
        self.assertEqual(self.combat.enemy_health, 45)

    def test_apply_damage_to_player(self):
        self.combat.apply_damage(25, 'player')
        self.assertEqual(self.combat.player_health, 75)

    def test_apply_damage_to_player_stacked(self):
        self.combat.apply_damage(25, 'player')
        self.assertEqual(self.combat.player_health, 75)
        self.combat.apply_damage(5, 'player')
        self.assertEqual(self.combat.player_health, 70)

    def test_apply_damage_to_player_and_enemy(self):
        self.combat.apply_damage(25, 'player')
        self.assertEqual(self.combat.player_health, 75)
        self.assertEqual(self.combat.enemy_health, 100)
        self.combat.apply_damage(5, 'enemy')
        self.assertEqual(self.combat.player_health, 75)
        self.assertEqual(self.combat.enemy_health, 95)

    def test_apply_damage_to_player_and_enemy_stacked(self):
        self.combat.apply_damage(15, 'player')
        self.assertEqual(self.combat.player_health, 85)
        self.assertEqual(self.combat.enemy_health, 100)
        self.combat.apply_damage(15, 'enemy')
        self.assertEqual(self.combat.player_health, 85)
        self.assertEqual(self.combat.enemy_health, 85)
        self.combat.apply_damage(20, 'enemy')
        self.assertEqual(self.combat.player_health, 85)
        self.assertEqual(self.combat.enemy_health, 65)
        self.combat.apply_damage(30, 'player')
        self.assertEqual(self.combat.player_health, 55)
        self.assertEqual(self.combat.enemy_health, 65)
        self.assertEqual(self.combat.player_shield, 0)
        self.assertEqual(self.combat.enemy_shield, 0)
        self.assertEqual(len(self.combat.player_hand), 5)

    def test_apply_damage_to_player_exceeds_health(self):
        self.assertEqual(self.combat.player_health, 100)
        self.combat.apply_damage(99, 'player')
        self.assertEqual(self.combat.player_health, 1)
        self.combat.apply_damage(1, 'player')
        self.assertEqual(self.combat.player_health, 0)
        self.combat.apply_damage(10, 'player')
        self.assertEqual(self.combat.player_health, 0)

    def test_apply_damage_to_player_exceeds_health_in_one(self):
        self.assertEqual(self.combat.player_health, 100)
        self.combat.apply_damage(110, 'player')
        self.assertEqual(self.combat.player_health, 0)

    def test_apply_shield_to_player(self):
        self.combat.apply_shield(10)
        self.assertEqual(self.combat.player_shield, 10)

    def test_apply_shield_to_player_stacked(self):
        self.combat.apply_shield(20)
        self.assertEqual(self.combat.player_shield, 20)
        self.combat.apply_shield(13)
        self.assertEqual(self.combat.player_shield, 33)

    def test_shield_breaks_correctly_and_damage_applied_on_player(self):
        self.combat.apply_shield(10)
        self.combat.apply_damage(3, 'player')
        self.assertEqual(self.combat.player_shield, 7)
        self.assertEqual(self.combat.player_health, 100)
        self.combat.apply_damage(13, 'player')
        self.assertEqual(self.combat.player_shield, 0)
        self.assertEqual(self.combat.player_health, 94)
        self.combat.apply_shield(15)
        self.assertEqual(self.combat.player_shield, 15)
        self.assertEqual(self.combat.player_health, 94)
        self.combat.apply_damage(19, 'player')
        self.assertEqual(self.combat.player_shield, 0)
        self.assertEqual(self.combat.player_health, 90)

    def test_apply_shield_to_enemy(self):
        self.fail('[INCOMPLETE FEATURE] Unable to apply shield to an enemy')
        # TODO: When this feature is completed, uncomment the test below and confirm it works
        # self.combat.apply_shield(15, 'enemy')
        # self.assertEqual(self.combat.enemy_shield, 10)

    def test_apply_shield_to_enemy_stacked(self):
        self.fail('[INCOMPLETE FEATURE] Unable to apply shield to an enemy')
        # TODO: When this feature is completed, uncomment the test below and confirm it works
        # self.combat.apply_shield(20, 'enemy')
        # self.assertEqual(self.combat.enemy_shield, 20)
        # self.combat.apply_shield(13, 'enemy')
        # self.assertEqual(self.combat.enemy_shield, 33)

    def test_shield_breaks_correctly_and_damage_applied_on_enemy(self):
        self.fail('[INCOMPLETE FEATURE] Unable to apply shield to an enemy')
        # TODO: When this feature is completed, uncomment the test below and confirm it works
        # self.combat.apply_shield(10, 'enemy')
        # self.combat.apply_damage(3, 'enemy')
        # self.assertEqual(self.combat.enemy_shield, 7)
        # self.assertEqual(self.combat.enemy_health, 100)
        # self.combat.apply_damage(13, 'enemy')
        # self.assertEqual(self.combat.enemy_shield, 0)
        # self.assertEqual(self.combat.enemy_health, 94)
        # self.combat.apply_shield(15, 'enemy')
        # self.assertEqual(self.combat.enemy_shield, 15)
        # self.assertEqual(self.combat.enemy_health, 94)
        # self.combat.apply_damage(19, 'enemy')
        # self.assertEqual(self.combat.enemy_shield, 0)
        # self.assertEqual(self.combat.enemy_health, 90)

    def test_enemy_death(self):
        self.combat.enemy_health = 0
        self.combat.check_win_condition()

        # As the player is not at the dungeon, make sure the Victory Screen is not pushed
        self.game.push_state.assert_not_called()
        # Check if the game state is popped
        self.game.pop_state.assert_called_once()

    def test_enemy_death_completed_dungeon(self):
        # Set the player's position to the end of the dungeon
        self.dungeon = MagicMock(player_position=(4, 4))
        self.game.dungeon = self.dungeon
        self.combat.enemy_health = 0
        self.combat.check_win_condition()

        # Check if an instance of VictoryScreen is pushed to the game state when the enemy dies
        self.combat.game.push_state.assert_called_once()
        called_args, _ = self.combat.game.push_state.call_args
        assert isinstance(called_args[0], VictoryScreen)

        # Check if the game state is popped
        self.combat.game.pop_state.assert_called_once()

    def test_player_death(self):
        self.combat.player_health = 0
        self.combat.check_win_condition()

        # Check if the player dies the change state method is called and sends you back to the MainMenu
        self.game.change_state.assert_called_once()
        called_args, _ = self.combat.game.change_state.call_args
        assert isinstance(called_args[0], MainMenu)

    def test_both_alive(self):
        self.combat.enemy_health = 50
        self.combat.player_health = 50
        self.combat.check_win_condition()
        self.game.change_state.assert_not_called()
        self.game.push_state.assert_not_called()
        self.game.pop_state.assert_not_called()

    def test_play_card_functionality(self):
        # Iterate through all cards and play each one
        for card in self.player.hand:
            # Patch the apply_damage and apply_shield methods as mocks for this test to check they are called
            with patch.object(self.combat, 'apply_damage') as mock_apply_damage, \
                    patch.object(self.combat, 'apply_shield') as mock_apply_shield:
                card.play(self.combat)

                # Check if the correct methods are called with the correct arguments
                if card.target in ["enemy", "player"]:
                    mock_apply_damage.assert_called_with(card.damage, card.target)
                    mock_apply_shield.assert_called_with(card.shield)
                else:
                    mock_apply_damage.assert_not_called()
                    mock_apply_shield.assert_not_called()

    def test_play_card_valid_index(self):
        # Mock the play method to assert that it doesn't get called
        with patch.object(Card, 'play') as mock_play:
            self.combat.play_card(2)
            mock_play.assert_called_once()

    # TODO: This will fail because the play_card method doesn't have a lower bound
    def test_play_card_invalid_index(self):
        # Mock the play method to assert that it doesn't get called
        with patch.object(Card, 'play') as mock_play:
            self.combat.play_card(-1)
            self.combat.play_card(len(self.player.hand))
            mock_play.assert_not_called()

    def test_update_health_bars(self):
        # Set the player and enemy health
        self.combat.player_health = 50
        self.combat.enemy_health = 80

        with patch('app.combat.combat.pygame.draw.rect') as rect_mock:
            self.combat.update_health_bars()

            # Calculate expected bar widths
            player_bar_width = int((self.combat.player_health / self.player.max_health) * HEALTH_BAR_WIDTH) # Should be 100
            enemy_bar_width = int((self.combat.enemy_health / self.enemy.max_health) * HEALTH_BAR_WIDTH) # Should be 160

            # Assert that pygame.draw.rect is called with the correct arguments
            rect_mock.assert_has_calls([
                call(self.game.screen, PLAYER_HEALTH_COLOR, (50, 50, player_bar_width, HEALTH_BAR_HEIGHT)),
                call(self.game.screen, ENEMY_HEALTH_COLOR, (SCREEN_WIDTH - 50 - enemy_bar_width, 50, enemy_bar_width, HEALTH_BAR_HEIGHT))
            ])

    # These are unit tests so user input and rendering are not tested. This tests that the appropriate methods are
    # called when a player event happens
    def test_handle_event_player_turn(self):
        # Create a mock event
        event = MagicMock()
        event.type = pygame.MOUSEBUTTONUP
        event.button = 1
        event.pos = (CARD_START_X, CARD_START_Y)

        # Set player_turn to True
        self.combat.player_turn = True

        # Mock the methods that should be called
        with patch.object(self.combat, 'play_card') as play_card_mock, \
             patch.object(self.combat, 'enemy_turn') as enemy_turn_mock, \
             patch.object(self.combat, 'check_win_condition') as check_win_condition_mock:

            # Call handle_event
            self.combat.handle_event(event)

            # Assert that the appropriate methods are called
            play_card_mock.assert_called_once_with(0)  # Check the 0 index card is played based on the event position
            enemy_turn_mock.assert_called_once()
            check_win_condition_mock.assert_called_once()

# Set up an instance of Combat for the repeated test
@pytest.fixture
def combat():
    game = MagicMock()
    player = MagicMock(max_health=100, hand=[])
    enemy = MagicMock(max_health=100)
    return Combat(game, player, enemy)

@pytest.mark.repeat(5)
@patch('app.combat.combat.random.randint')
def test_enemy_turn(randint_mock, combat):
    # Create a testcase to perform unittest assertions
    test_case = unittest.TestCase()

    # Set the player's initial health and shield
    initial_health = 100
    initial_shield = 3
    combat.player_health = initial_health
    combat.player_shield = initial_shield

    # Mock the damage value generated by random.randint
    damage = 7
    randint_mock.return_value = damage

    # Call the enemy_turn method
    combat.enemy_turn()

    # Assert that the player's health and shield are updated correctly
    test_case.assertEqual(combat.player_health, 96)
    test_case.assertEqual(combat.player_shield, 0)
    test_case.assertTrue(combat.player_turn)

if __name__ == '__main__':
    unittest.main()
