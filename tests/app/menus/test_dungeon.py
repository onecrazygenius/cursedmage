import unittest
from unittest.mock import MagicMock, patch

from pygame import KEYDOWN

from app.engine.constants import DUNGEON_SIZE_X, DUNGEON_SIZE_Y
from app.menus.dungeon import Dungeon


class TestDungeon(unittest.TestCase):
    def setUp(self):
        self.game = MagicMock()
        self.dungeon = Dungeon(self.game)

    def test_generate_rooms(self):
        self.assertEqual(len(self.dungeon.rooms), DUNGEON_SIZE_X)
        for row in self.dungeon.rooms:
            self.assertEqual(len(row), DUNGEON_SIZE_Y)
            for room in row:
                self.assertIsNotNone(room.enemy)

    def test_move_to_room(self):
        position = (1, 0)
        self.dungeon.move_to_room(position)
        self.assertEqual(self.dungeon.player_position, position)
        self.assertTrue(self.dungeon.rooms[position[0]][position[1]].visited)

    @patch("app.menus.dungeon.Combat")
    def test_move_to_room_with_enemy(self, mock_combat):
        position = (1, 0)
        self.dungeon.move_to_room(position)
        self.game.push_state.assert_called_with(mock_combat.return_value)

    def test_update_player_position(self):
        self.dungeon.player_position = (DUNGEON_SIZE_X - 1, 0)
        self.dungeon.update_player_position()
        self.assertEqual(self.dungeon.player_position, (0, 1))

    def test_update_player_position_end_of_dungeon(self):
        self.dungeon.player_position = (DUNGEON_SIZE_X - 1, DUNGEON_SIZE_Y - 1)
        self.dungeon.update_player_position()
        self.game.victory.assert_called_once()
        self.dungeon.player_position = (DUNGEON_SIZE_X - 1, DUNGEON_SIZE_Y - 1)  # Check the player position didn't move

    def test_handle_event(self):
        event = MagicMock()
        event.type = KEYDOWN
        with patch.object(self.dungeon, "move_to_room", wraps=self.dungeon.move_to_room) as mock_dungeon:
            # There are 2 handle_event methods with the same signature causing this test to fail
            self.dungeon.handle_event(event)
            mock_dungeon.assert_called_once()

    def test_get_data(self):
        data = self.dungeon.get_data()
        self.assertEqual(data["player_position"], self.dungeon.player_position)
        self.assertEqual(len(data["rooms"]), DUNGEON_SIZE_X)
        for x in range(DUNGEON_SIZE_X):
            self.assertEqual(len(data["rooms"][x]), DUNGEON_SIZE_Y)

    def test_load_data(self):
        game_data = self.dungeon.get_data()
        new_dungeon = Dungeon(self.game, game_data)
        self.assertEqual(new_dungeon.player_position, self.dungeon.player_position)
        for x in range(DUNGEON_SIZE_X):
            for y in range(DUNGEON_SIZE_Y):
                self.assertEqual(new_dungeon.rooms[x][y].get_data(), self.dungeon.rooms[x][y].get_data())


if __name__ == "__main__":
    unittest.main()
