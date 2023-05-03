import unittest
from unittest.mock import MagicMock

from app.combat.card import Card


class TestCard(unittest.TestCase):

    # Test that the card is initialised properly
    def test_card_initialisation(self):
        card = Card("Fireball", 10, 1, "player")
        self.assertEqual(card.name, "Fireball")
        self.assertEqual(card.damage, 10)
        self.assertEqual(card.shield, 1)
        self.assertEqual(card.target, "player")
        self.assertIsInstance(card, Card)

    def test_card_attack_player(self):
        # Create a Card instance named Fireball, 10 damage, 1 shield and targets player
        card = Card("Fireball", 10, 1, "player")
        # Mock an instance of Combat and set variables used in this test
        combat = MagicMock()

        # Play the card against the combat mock
        card.play(combat)

        # Assert that the apply_damage and apply_shield methods were called once
        combat.apply_shield.assert_called_once()
        combat.apply_damage.assert_called_once()

        # MagicMock doesn't actually execute the method, so you can't test the cards effect happens.
        # This would be done in an integration test

    def test_card_attack_enemy(self):
        # Create a Card instance named Fireball, 10 damage, 1 shield and targets player
        card = Card("Fireball", 10, 1, "enemy")
        # Mock an instance of Combat and set variables used in this test
        combat = MagicMock()

        # Play the card against the combat mock
        card.play(combat)

        # Assert that the apply_damage and apply_shield methods were called once
        combat.apply_shield.assert_called_once()
        combat.apply_damage.assert_called_once()

    def test_card_attack_invalid_target(self):
        # Create a Card instance named Fireball, 10 damage, 1 shield and targets player
        card = Card("Fireball", 10, 1, "INVALID_TARGET")
        # Mock an instance of Combat and set variables used in this test
        combat = MagicMock()

        # Play the card against the combat mock
        card.play(combat)

        # Assert that the apply_shield and apply_damage method is not called. The target was invalid so no stats
        # should have been modified
        # TODO: Shield will always try to be applied. This is a bug and causes this test to fail
        combat.apply_shield.assert_not_called()
        combat.apply_damage.assert_not_called()


if __name__ == '__main__':
    unittest.main()
