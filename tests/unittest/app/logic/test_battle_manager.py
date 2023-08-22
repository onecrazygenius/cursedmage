import unittest

from requests import patch
from app.logic.battle_manager import BattleManager
from app.logic.combat.characters.character import Character
from app.logic.combat.characters.enemy import Enemy
from app.logic.combat.deck.deck import Deck
from app.logic.combat.deck.card import Card

class TestBattleManager(unittest.TestCase):

    def test_apply_cost(self):
        player  = Character("Warrior")
        self.assertEqual(player.name, "Warrior") 
        self.assertEqual(player.max_health, 500)
        self.assertEqual(player.attack, 3)
        self.assertEqual(player.defense, 4)
        self.assertEqual(player.cost, 3)
        enemies = []
        battle_manager = BattleManager(player, enemies)

        card =Card("Fireball")
        battle_manager.apply_cost(card)

        assert battle_manager.current_turn.cost == 2
        



    def test_play_card(self):
        player = Character("Warrior")
        enemy = Enemy("Goblin")
        enemies = [enemy]
        battle_manager = BattleManager(player, enemies)

        card1 = Card("Fireball")
        battle_manager.current_turn.deck.hand.append(card1)  # Add the card to the hand
        self.assertTrue(battle_manager.play_card(card1))
        self.assertEqual(battle_manager.current_turn.cost, 2)



    def test_check_floor_cleared(self):
        player  = Character("Warrior")
        self.assertEqual(player.name, "Warrior") 
        self.assertEqual(player.max_health, 500)
        self.assertEqual(player.attack, 3)
        self.assertEqual(player.defense, 4)
        self.assertEqual(player.cost, 3)

        enemy  = Enemy("Goblin")
        self.assertEqual(enemy.name, "Goblin") 
        self.assertEqual(enemy.max_health, 100)
        self.assertEqual(enemy.attack, 3)
        self.assertEqual(enemy.defense, 4)
        self.assertEqual(enemy.cost, 3)
        self.assertIsNotNone(enemy.sprite)

        enemy2  = Enemy("Goblin")
        self.assertEqual(enemy2.name, "Goblin") 
        self.assertEqual(enemy2.max_health, 100)
        self.assertEqual(enemy2.attack, 3)
        self.assertEqual(enemy2.defense, 4)
        self.assertEqual(enemy2.cost, 3)
        self.assertIsNotNone(enemy2.sprite)
        enemies = [enemy, enemy2]
        battle_manager = BattleManager(player, enemies)

        enemy.cur_health = 10
        self.assertEqual(battle_manager.check_floor_cleared(), False)

        enemy.cur_health = 0
        enemy2.cur_health = 0

        self.assertEqual(battle_manager.check_floor_cleared(), True)

    def test_apply_heal(self):
            player  = Character("Warrior")
            self.assertEqual(player.name, "Warrior") 
            self.assertEqual(player.max_health, 500)
            self.assertEqual(player.attack, 3)
            self.assertEqual(player.defense, 4)
            self.assertEqual(player.cost, 3)
            enemies = []
            battle_manager = BattleManager(player, enemies)

            player.cur_health 
            card2 = Card("Heal")
            card2.target = player
            self.assertEqual(battle_manager.apply_heal(card2) , False) # max health

            player.cur_health = 1

            card1 = Card("Heal")
            card1.target = player
            self.assertTrue(card1.is_heal)
            self.assertEqual(player.cur_health,1)
            self.assertTrue(battle_manager.apply_heal(card1))


            #IF STATEMENT IN APPLY HEAL IS INCORRECT ALWAYS TRUE BASICALLY CUZ PLACED SHIT
            #APPLIES HEAL NO MATTER WHAT
        




def test_simulate_enemy_turn(self):
    player = Character("Warrior")
    enemy = Enemy("Goblin")
    enemies = [enemy]
    battle_manager = BattleManager(player, enemies)
    game_difficulty = 1

    turn_result = battle_manager.simulate_enemy_turn(enemy, game_difficulty)

    assert turn_result in [battle_manager.FAILED, battle_manager.END_TURN, battle_manager.GAME_OVER, battle_manager.CONTINUE, battle_manager.FLOOR_COMPLETE]

    def test_check_cost(self):
        player  = Character("Warrior")
        self.assertEqual(player.name, "Warrior") 
        self.assertEqual(player.max_health, 500)
        self.assertEqual(player.attack, 3)
        self.assertEqual(player.defense, 4)
        self.assertEqual(player.cost, 3)
        enemies = []
        battle_manager = BattleManager(player, enemies)

        card1 = Card("Heal")
        #battle_manager.play_card("Heal")
        self.assertEqual(battle_manager.check_cost(card1), 1)

    @patch('pygame.event.post')  # Mock the pygame.event.post function
    def test_next_turn(self, mock_event_post):
        player = Character("Warrior")
        enemy = Enemy("Goblin")
        enemy2 = Enemy("Goblin")
        enemies = [enemy, enemy2]
        battle_manager = BattleManager(player, enemies)

        battle_manager.next_turn()
        self.assertEqual(battle_manager.current_turn, enemy)

        battle_manager.next_turn()
        self.assertEqual(battle_manager.current_turn, enemy2)

        battle_manager.next_turn()
        self.assertEqual(battle_manager.current_turn, player)

    def test_check_player_dead(self):
        player  = Character("Warrior")
        self.assertEqual(player.name, "Warrior") 
        self.assertEqual(player.max_health, 500)
        self.assertEqual(player.attack, 3)
        self.assertEqual(player.defense, 4)
        self.assertEqual(player.cost, 3)

        enemy  = Enemy("Goblin")
        self.assertEqual(enemy.name, "Goblin") 
        self.assertEqual(enemy.max_health, 100)
        self.assertEqual(enemy.attack, 3)
        self.assertEqual(enemy.defense, 4)
        self.assertEqual(enemy.cost, 3)
        self.assertIsNotNone(enemy.sprite)
        enemies = []
        battle_manager = BattleManager(player, enemies)

        battle_manager.player.is_dead == False
        self.assertEqual(battle_manager.check_player_dead, False) 


if __name__ == '__main__':
    unittest.main()







       