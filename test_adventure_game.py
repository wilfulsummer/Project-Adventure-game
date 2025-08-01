import unittest
import json
import os
import tempfile
from unittest.mock import patch, MagicMock
from io import StringIO
import sys

# Import game modules
from constants import *
from game_state import *
from command_handlers import *
from save_load import save_game, load_game
from ui_functions import *
from world_generation import get_room

# Import using_fists specifically
from game_state import using_fists

class TestAdventureGame(unittest.TestCase):
    """Test suite for the Adventure Game"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        # Reset global game state
        global worlds, player_floor, player_x, player_y, inventory, armor_inventory, equipped_armor
        global player_hp, player_max_hp, player_stamina, player_max_stamina, player_mana, player_max_mana
        global player_money, player_potions, stamina_potions, mana_potions, waypoint_scrolls
        global mysterious_keys, golden_keys, unlocked_floors, waypoints, discovered_enemies
        global learned_spells, spell_scrolls, using_fists
        
        # Initialize with default values
        worlds = {}
        player_floor = 0
        player_x = 0
        player_y = 0
        inventory = []
        armor_inventory = []
        equipped_armor = None
        player_hp = 50
        player_max_hp = 50
        player_stamina = 20
        player_max_stamina = 20
        player_mana = 20
        player_max_mana = 20
        player_money = 0
        player_potions = 0
        stamina_potions = 0
        mana_potions = 0
        waypoint_scrolls = 0
        mysterious_keys = {}
        golden_keys = 0
        unlocked_floors = set()
        waypoints = {}
        discovered_enemies = set()
        learned_spells = []
        spell_scrolls = {}
        using_fists = False
        
        # Create a temporary save file for testing
        self.temp_dir = tempfile.mkdtemp()
        self.test_save_file = os.path.join(self.temp_dir, "test_save.json")
        
    def tearDown(self):
        """Clean up after each test method"""
        # Remove temporary files
        if os.path.exists(self.test_save_file):
            os.remove(self.test_save_file)
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)

    def test_movement_commands(self):
        """Test movement commands (north, south, east, west)"""
        # Test basic movement without enemies
        current_room = {"description": "A test room"}
        
        # Test north movement
        success, new_x, new_y = handle_movement("north", current_room, 0, 0, 0, {}, [])
        self.assertTrue(success)
        self.assertEqual(new_x, 0)
        self.assertEqual(new_y, 1)
        
        # Test south movement
        success, new_x, new_y = handle_movement("south", current_room, 0, 0, 0, {}, [])
        self.assertTrue(success)
        self.assertEqual(new_x, 0)
        self.assertEqual(new_y, -1)
        
        # Test east movement
        success, new_x, new_y = handle_movement("east", current_room, 0, 0, 0, {}, [])
        self.assertTrue(success)
        self.assertEqual(new_x, 1)
        self.assertEqual(new_y, 0)
        
        # Test west movement
        success, new_x, new_y = handle_movement("west", current_room, 0, 0, 0, {}, [])
        self.assertTrue(success)
        self.assertEqual(new_x, -1)
        self.assertEqual(new_y, 0)
        
        # Test movement with regular enemy (should block)
        current_room_with_enemy = {
            "description": "A test room",
            "enemy": {"name": "Goblin", "hp": 10, "base_attack": 5}
        }
        
        success, new_x, new_y = handle_movement("north", current_room_with_enemy, 0, 0, 0, {}, [])
        self.assertFalse(success)
        self.assertEqual(new_x, 0)
        self.assertEqual(new_y, 0)
        
        # Test movement with boss enemy (should allow escape)
        current_room_with_boss = {
            "description": "A test room",
            "enemy": {"name": "Troll", "hp": 50, "base_attack": 15, "is_boss": True}
        }
        
        success, new_x, new_y = handle_movement("north", current_room_with_boss, 0, 0, 0, {}, [])
        self.assertTrue(success)
        self.assertEqual(new_x, 0)
        self.assertEqual(new_y, 1)
        
        # Test movement with training dummy (should allow movement)
        current_room_with_dummy = {
            "description": "A test room",
            "enemy": {"name": "Training Dummy", "hp": 100, "base_attack": 0, "is_training_dummy": True}
        }
        
        success, new_x, new_y = handle_movement("north", current_room_with_dummy, 0, 0, 0, {}, [])
        self.assertTrue(success)
        self.assertEqual(new_x, 0)
        self.assertEqual(new_y, 1)

    def test_attack_command(self):
        """Test attack command functionality"""
        # Test attack with no enemy
        current_room = {"description": "A test room"}
        
        with patch('builtins.print') as mock_print:
            result = handle_attack(current_room, [], 20, None, 50, set(), {}, 0, 0, [], spells, False)
            self.assertTrue(result)
            mock_print.assert_called_with("There's no enemy here to attack.")
        
        # Test attack with enemy using fists
        current_room_with_enemy = {
            "description": "A test room",
            "enemy": {"name": "Goblin", "hp": 10, "base_attack": 5}
        }
        
        with patch('builtins.print') as mock_print:
            result = handle_attack(current_room_with_enemy, [], 20, None, 50, set(), {}, 0, 0, [], spells, False)
            self.assertTrue(result)
            # Check that enemy took damage
            self.assertLess(current_room_with_enemy["enemy"]["hp"], 10)
        
        # Test attack with weapon
        weapon = {"name": "Sword", "damage": 8, "durability": 10}
        inventory = [weapon]
        
        with patch('builtins.print') as mock_print:
            result = handle_attack(current_room_with_enemy, inventory, 20, None, 50, set(), {}, 0, 0, [], spells, False)
            self.assertTrue(result)
            # Check that weapon durability decreased
            self.assertEqual(weapon["durability"], 9)
        
        # Test attack with training dummy (no durability loss)
        current_room_with_dummy = {
            "description": "A test room",
            "enemy": {"name": "Training Dummy", "hp": 100, "base_attack": 0, "is_training_dummy": True}
        }
        
        weapon = {"name": "Sword", "damage": 8, "durability": 10}
        inventory = [weapon]
        
        with patch('builtins.print') as mock_print:
            result = handle_attack(current_room_with_dummy, inventory, 20, None, 50, set(), {}, 0, 0, [], spells, False)
            self.assertTrue(result)
            # Check that weapon durability didn't decrease
            self.assertEqual(weapon["durability"], 10)

    def test_take_command(self):
        """Test take command functionality"""
        # Test take with no items
        current_room = {"description": "A test room"}
        
        with patch('builtins.print') as mock_print:
            result = handle_take(current_room, [], [], MAX_WEAPONS, MAX_ARMOR)
            self.assertTrue(result)
            mock_print.assert_called_with("There's nothing here to take.")
        
        # Test take with single weapon
        weapon = {"name": "Sword", "damage": 8, "durability": 10}
        current_room_with_weapon = {
            "description": "A test room",
            "weapons": [weapon]
        }
        
        with patch('builtins.print') as mock_print:
            result = handle_take(current_room_with_weapon, [], [], MAX_WEAPONS, MAX_ARMOR)
            self.assertTrue(result)
            mock_print.assert_called_with("You picked up the Sword!")
        
        # Test take with full inventory
        full_inventory = [
            {"name": "Sword", "damage": 8, "durability": 10},
            {"name": "Bow", "damage": 6, "durability": 8},
            {"name": "Axe", "damage": 10, "durability": 12}
        ]
        
        # Create a new room with weapon for the full inventory test
        current_room_with_weapon2 = {
            "description": "A test room",
            "weapons": [{"name": "Dagger", "damage": 5, "durability": 8}]
        }
        
        with patch('builtins.print') as mock_print:
            result = handle_take(current_room_with_weapon2, full_inventory, [], MAX_WEAPONS, MAX_ARMOR)
            self.assertTrue(result)
            mock_print.assert_called_with("Your weapon inventory is full! Drop a weapon first.")

    def test_inventory_command(self):
        """Test inventory command functionality"""
        # Test empty inventory
        with patch('builtins.print') as mock_print:
            result = handle_inventory([], False)
            self.assertTrue(result)
            mock_print.assert_any_call("You have no weapons.")
            mock_print.assert_any_call("Currently using: Fists (Damage: 3, Durability: Infinite)")
        
        # Test inventory with weapons
        inventory = [
            {"name": "Sword", "damage": 8, "durability": 10},
            {"name": "Spell Book", "durability": 5}
        ]
        
        with patch('builtins.print') as mock_print:
            result = handle_inventory(inventory, False)
            self.assertTrue(result)
            # Check that weapons are displayed
            mock_print.assert_any_call("\nYour weapons:")

    def test_armor_command(self):
        """Test armor command functionality"""
        # Test empty armor inventory
        with patch('builtins.print') as mock_print:
            result = handle_armor([], None)
            self.assertTrue(result)
            mock_print.assert_called_with("You have no armor.")
        
        # Test armor inventory with items
        armor_inventory = [
            {"name": "Leather Armor", "defense": 5, "durability": 15}
        ]
        equipped_armor = {"name": "Chain Mail", "defense": 8, "durability": 20}
        
        with patch('builtins.print') as mock_print:
            result = handle_armor(armor_inventory, equipped_armor)
            self.assertTrue(result)
            # Check that armor is displayed
            mock_print.assert_any_call("\nYour armor:")

    def test_drop_command(self):
        """Test drop command functionality"""
        # Test drop with empty inventory
        current_room = {"description": "A test room"}
        
        with patch('builtins.print') as mock_print:
            result = handle_drop([], current_room)
            self.assertTrue(result)
            mock_print.assert_called_with("You have no weapons to drop.")
        
        # Test drop with weapons
        inventory = [
            {"name": "Sword", "damage": 8, "durability": 10},
            {"name": "Bow", "damage": 6, "durability": 8}
        ]
        
        with patch('builtins.input', return_value='1'), patch('builtins.print') as mock_print:
            result = handle_drop(inventory, current_room)
            self.assertTrue(result)
            # Check that weapon was dropped
            self.assertIn("weapons", current_room)
            self.assertEqual(len(current_room["weapons"]), 1)

    def test_drop_armor_command(self):
        """Test drop_armor command functionality"""
        # Test drop_armor with empty inventory
        current_room = {"description": "A test room"}
        
        with patch('builtins.print') as mock_print:
            result = handle_drop_armor([], None, current_room)
            self.assertTrue(result)
            mock_print.assert_called_with("You have no armor to drop.")
        
        # Test drop_armor with armor
        armor_inventory = [
            {"name": "Leather Armor", "defense": 5, "durability": 15}
        ]
        
        with patch('builtins.input', return_value='1'), patch('builtins.print') as mock_print:
            result = handle_drop_armor(armor_inventory, None, current_room)
            self.assertTrue(result)
            # Check that armor was dropped
            self.assertIn("armors", current_room)
            self.assertEqual(len(current_room["armors"]), 1)

    def test_equip_command(self):
        """Test equip command functionality"""
        # Test equip with empty inventory
        with patch('builtins.print') as mock_print:
            result, equipped = handle_equip([])
            self.assertTrue(result)
            self.assertIsNone(equipped)
            mock_print.assert_called_with("You have no armor to equip.")
        
        # Test equip with armor
        armor_inventory = [
            {"name": "Leather Armor", "defense": 5, "durability": 15}
        ]
        
        with patch('builtins.input', return_value='1'), patch('builtins.print') as mock_print:
            result, equipped = handle_equip(armor_inventory)
            self.assertTrue(result)
            self.assertIsNotNone(equipped)
            self.assertEqual(equipped["name"], "Leather Armor")

    def test_switch_command(self):
        """Test switch command functionality"""
        # Test switch with empty inventory
        with patch('builtins.input', return_value='0'), patch('builtins.print') as mock_print:
            result = handle_switch([])
            self.assertTrue(result)
            mock_print.assert_called_with("You're already using your fists.")
        
        # Test switch with weapons
        inventory = [
            {"name": "Sword", "damage": 8, "durability": 10},
            {"name": "Bow", "damage": 6, "durability": 8}
        ]
        
        with patch('builtins.input', return_value='2'), patch('builtins.print') as mock_print:
            result = handle_switch(inventory)
            self.assertTrue(result)
            # Check that weapons were switched
            self.assertEqual(inventory[0]["name"], "Bow")

    def test_absorb_command(self):
        """Test absorb command functionality"""
        # Test absorb with no crystal
        current_room = {"description": "A test room"}
        
        with patch('builtins.print') as mock_print:
            result = handle_absorb(current_room, 50, 30, 15, 20, 15, 20)
            self.assertEqual(result, (50, 30, 15, 20, 15))
            mock_print.assert_called_with("There's no crystal here to absorb.")
        
        # Test absorb life crystal
        current_room_with_life_crystal = {
            "description": "A test room",
            "crystal_type": "life"
        }
        
        with patch('builtins.print') as mock_print:
            result = handle_absorb(current_room_with_life_crystal, 50, 30, 15, 20, 15, 20)
            self.assertEqual(result, (60, 50, 15, 20, 15))
            self.assertIsNone(current_room_with_life_crystal["crystal_type"])
            mock_print.assert_called_with("You absorb the life crystal! +10 max HP, +20 current HP")
        
        # Test absorb stamina crystal
        current_room_with_stamina_crystal = {
            "description": "A test room",
            "crystal_type": "stamina"
        }
        
        with patch('builtins.print') as mock_print:
            result = handle_absorb(current_room_with_stamina_crystal, 50, 30, 15, 20, 15, 20)
            self.assertEqual(result, (50, 30, 20, 20, 15))
            self.assertIsNone(current_room_with_stamina_crystal["crystal_type"])
            mock_print.assert_called_with("You absorb the stamina crystal! +10 stamina")

    def test_run_command(self):
        """Test run command functionality"""
        # Test run with no enemy
        current_room = {"description": "A test room"}
        
        with patch('builtins.print') as mock_print:
            result = handle_run(current_room, 20, 0, 0)
            self.assertEqual(result, (20, 0, 0))
            mock_print.assert_called_with("There's no enemy here to run away from.")
        
        # Test run with enemy and sufficient stamina
        current_room_with_enemy = {
            "description": "A test room",
            "enemy": {"name": "Goblin", "hp": 10, "base_attack": 5}
        }
        
        with patch('builtins.print') as mock_print:
            result = handle_run(current_room_with_enemy, 20, 0, 0)
            stamina, x, y = result
            self.assertEqual(stamina, 10)  # 20 - 10 = 10
            # Position should have changed (random direction)
            self.assertTrue(x != 0 or y != 0)
            mock_print.assert_any_call("You run away from the Goblin!")
        
        # Test run with insufficient stamina
        with patch('builtins.print') as mock_print:
            result = handle_run(current_room_with_enemy, 5, 0, 0)
            self.assertEqual(result, (5, 0, 0))
            mock_print.assert_any_call("You need 10 stamina, but you only have 5.")

    def test_save_load_commands(self):
        """Test save and load functionality"""
        # Test save game with all required parameters
        test_data = {
            "worlds": {},
            "inventory": [{"name": "Sword", "damage": 8, "durability": 10}],
            "armor_inventory": [],
            "equipped_armor": None,
            "player_floor": 1,
            "player_x": 5,
            "player_y": 3,
            "player_hp": 45,
            "player_max_hp": 50,
            "player_stamina": 20,
            "player_max_stamina": 20,
            "player_mana": 20,
            "player_max_mana": 20,
            "player_money": 100,
            "player_potions": 0,
            "stamina_potions": 0,
            "mana_potions": 0,
            "mysterious_keys": {},
            "golden_keys": 0,
            "unlocked_floors": set(),
            "waypoints": {},
            "waypoint_scrolls": 0,
            "discovered_enemies": set(),
            "learned_spells": [],
            "spell_scrolls": {},
            "using_fists": False
        }
        
        # Save the test data
        with patch('save_load.SAVE_FILE', self.test_save_file):
            save_game(**test_data)
        
        # Verify file was created
        self.assertTrue(os.path.exists(self.test_save_file))
        
        # Test load game
        with patch('save_load.SAVE_FILE', self.test_save_file):
            loaded_data = load_game()
        
        # Verify data was loaded correctly
        self.assertIsNotNone(loaded_data)
        self.assertEqual(loaded_data["player_floor"], 1)
        self.assertEqual(loaded_data["player_x"], 5)
        self.assertEqual(loaded_data["player_y"], 3)
        self.assertEqual(loaded_data["player_hp"], 45)
        self.assertEqual(loaded_data["player_money"], 100)

    def test_ui_functions(self):
        """Test UI functions"""
        # Test show_map
        with patch('builtins.print') as mock_print:
            show_map(0, 0, 0, {})
            mock_print.assert_any_call("\n=== MAP ===")
        
        # Test show_bestiary with empty discovered enemies
        with patch('builtins.print') as mock_print:
            show_bestiary(set())
            mock_print.assert_any_call("You have no enemy info!")
        
        # Test show_bestiary with discovered enemies
        discovered = {"Goblin", "Skeleton"}
        with patch('builtins.print') as mock_print:
            show_bestiary(discovered)
            mock_print.assert_any_call("\n=== BESTIARY ===")
        
        # Test show_help
        with patch('builtins.print') as mock_print:
            show_help()
            mock_print.assert_any_call("\n=== HELP SYSTEM ===")

    def test_constants(self):
        """Test game constants"""
        # Test weapon limits
        self.assertEqual(MAX_WEAPONS, 3)
        self.assertEqual(MAX_ARMOR, 2)
        self.assertEqual(MAX_PLAYER_HP, 250)
        
        # Test spell definitions
        self.assertIn("Fire", spells)
        self.assertIn("Poison", spells)
        self.assertIn("Stun", spells)
        
        # Test enemy stats
        self.assertIn("Goblin", enemy_stats)
        self.assertIn("Skeleton", enemy_stats)
        self.assertIn("Orc", enemy_stats)

    def test_edge_cases(self):
        """Test edge cases and error handling"""
        # Test movement with invalid direction
        current_room = {"description": "A test room"}
        success, new_x, new_y = handle_movement("invalid", current_room, 0, 0, 0, {}, [])
        self.assertFalse(success)
        
        # Test take with invalid choice (need multiple items to trigger choice menu)
        current_room_with_multiple_items = {
            "description": "A test room",
            "weapons": [{"name": "Sword", "damage": 8, "durability": 10}],
            "armors": [{"name": "Leather Armor", "defense": 5, "durability": 15}]
        }
        
        with patch('builtins.input', return_value='999'), patch('builtins.print') as mock_print:
            result = handle_take(current_room_with_multiple_items, [], [], MAX_WEAPONS, MAX_ARMOR)
            self.assertTrue(result)
            # The function should handle invalid input gracefully
            # Let's check what was actually printed
            print_calls = [call[0][0] for call in mock_print.call_args_list]
            self.assertIn("Invalid choice.", print_calls)
        
        # Test drop with invalid choice
        inventory = [{"name": "Sword", "damage": 8, "durability": 10}]
        current_room = {"description": "A test room"}
        
        with patch('builtins.input', return_value='999'), patch('builtins.print') as mock_print:
            result = handle_drop(inventory, current_room)
            self.assertTrue(result)
            # The function should handle invalid input gracefully
            # Let's check what was actually printed
            print_calls = [call[0][0] for call in mock_print.call_args_list]
            self.assertIn("Invalid choice.", print_calls)

    def test_combat_mechanics(self):
        """Test combat mechanics in detail"""
        # Test weapon breaking
        weapon = {"name": "Sword", "damage": 8, "durability": 1}
        inventory = [weapon]
        current_room = {
            "description": "A test room",
            "enemy": {"name": "Goblin", "hp": 5, "base_attack": 3}
        }
        
        with patch('builtins.print') as mock_print:
            result = handle_attack(current_room, inventory, 20, None, 50, set(), {}, 0, 0, [], spells, False)
            self.assertTrue(result)
            # Weapon should be removed from inventory when durability reaches 0
            self.assertEqual(len(inventory), 0)
            mock_print.assert_any_call("Your Sword breaks!")
        
        # Test armor breaking
        armor = {"name": "Leather Armor", "defense": 5, "durability": 1}
        current_room = {
            "description": "A test room",
            "enemy": {"name": "Goblin", "hp": 10, "base_attack": 8}
        }
        
        with patch('builtins.print') as mock_print:
            result = handle_attack(current_room, [], 20, armor, 50, set(), {}, 0, 0, [], spells, False)
            self.assertTrue(result)
            # Armor should be set to None when durability reaches 0
            self.assertEqual(armor["durability"], 0)
            # The function should handle armor breaking internally

    def test_spell_book_functionality(self):
        """Test Spell Book functionality"""
        # Test Spell Book without learned spells
        spell_book = {"name": "Spell Book", "durability": 5}
        inventory = [spell_book]
        current_room = {
            "description": "A test room",
            "enemy": {"name": "Goblin", "hp": 10, "base_attack": 5}
        }
        
        with patch('builtins.print') as mock_print:
            result = handle_attack(current_room, inventory, 20, None, 50, set(), {}, 0, 0, [], spells, False)
            self.assertTrue(result)
            mock_print.assert_any_call("You have a Spell Book but don't know any spells!")
        
        # Test Spell Book with learned spells
        learned_spells = ["Fire", "Poison"]
        
        with patch('builtins.input', return_value='1'), patch('builtins.print') as mock_print:
            result = handle_attack(current_room, inventory, 20, None, 50, set(), {}, 0, 0, learned_spells, spells, False)
            self.assertTrue(result)
            # Should show spell selection menu
            mock_print.assert_any_call("Which spell do you want to cast?")

if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2) 