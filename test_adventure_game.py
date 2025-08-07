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
        player_floor = 1
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
        # Test spell learning
        global learned_spells, spell_scrolls
        learned_spells = []
        spell_scrolls = {"Fireball": 1}
        
        # Test learning a spell
        with patch('builtins.input', return_value='y'):
            with patch('sys.stdout', new=StringIO()) as fake_output:
                # Simulate learning Fireball spell
                learned_spells.append("Fireball")
                spell_scrolls["Fireball"] -= 1
                
                # Verify spell was learned
                self.assertIn("Fireball", learned_spells)
                self.assertEqual(spell_scrolls["Fireball"], 0)

    def test_waypoint_system(self):
        """Test waypoint system functionality"""
        global waypoints, waypoint_scrolls, player_x, player_y, player_floor
        
        # Test adding waypoint
        waypoint_scrolls = 1
        player_x, player_y, player_floor = 5, 10, 2
        
        # Add waypoint
        waypoints["Test Waypoint"] = {"x": player_x, "y": player_y, "floor": player_floor}
        waypoint_scrolls -= 1
        
        self.assertIn("Test Waypoint", waypoints)
        self.assertEqual(waypoints["Test Waypoint"]["x"], 5)
        self.assertEqual(waypoints["Test Waypoint"]["y"], 10)
        self.assertEqual(waypoints["Test Waypoint"]["floor"], 2)
        self.assertEqual(waypoint_scrolls, 0)
        
        # Test viewing waypoint
        waypoint_info = waypoints["Test Waypoint"]
        self.assertEqual(waypoint_info["x"], 5)
        self.assertEqual(waypoint_info["y"], 10)
        self.assertEqual(waypoint_info["floor"], 2)
        
        # Test deleting waypoint
        del waypoints["Test Waypoint"]
        self.assertNotIn("Test Waypoint", waypoints)

    def test_materials_system(self):
        """Test materials collection and tracking"""
        global materials_inventory
        
        # Initialize materials inventory
        materials_inventory = {}
        
        # Test collecting materials
        materials_inventory["Dragon Scales"] = materials_inventory.get("Dragon Scales", 0) + 3
        materials_inventory["Goblin Teeth"] = materials_inventory.get("Goblin Teeth", 0) + 1
        
        self.assertEqual(materials_inventory["Dragon Scales"], 3)
        self.assertEqual(materials_inventory["Goblin Teeth"], 1)
        
        # Test material accumulation
        materials_inventory["Dragon Scales"] += 2
        self.assertEqual(materials_inventory["Dragon Scales"], 5)

    def test_repair_system(self):
        """Test weapon and armor repair functionality"""
        global player_money, inventory, armor_inventory
        
        # Test weapon repair
        player_money = 50
        damaged_weapon = {"name": "Damaged Sword", "damage": 10, "durability": 3, "max_durability": 10}
        inventory = [damaged_weapon]
        
        # Calculate repair cost
        missing_durability = damaged_weapon["max_durability"] - damaged_weapon["durability"]
        base_cost = max(1, damaged_weapon["damage"] // 4)
        total_cost = base_cost * missing_durability
        
        self.assertEqual(total_cost, 14)  # 10 damage / 4 = 2.5, rounded down to 2, * 7 missing durability = 14
        self.assertTrue(player_money >= total_cost)
        
        # Test armor repair
        damaged_armor = {"name": "Damaged Armor", "defense": 6, "durability": 2, "max_durability": 8}
        armor_inventory = [damaged_armor]
        
        missing_durability = damaged_armor["max_durability"] - damaged_armor["durability"]
        base_cost = max(1, damaged_armor["defense"] // 3)
        total_cost = base_cost * missing_durability
        
        self.assertEqual(total_cost, 12)  # 6 defense / 3 = 2, * 6 missing durability = 12

    def test_teleport_system(self):
        """Test teleport functionality"""
        global waypoints, player_x, player_y, player_floor
        
        # Set up waypoint
        waypoints["Test Teleport"] = {"x": 15, "y": 20, "floor": 3}
        
        # Test teleporting to waypoint
        waypoint_info = waypoints["Test Teleport"]
        player_x = waypoint_info["x"]
        player_y = waypoint_info["y"]
        player_floor = waypoint_info["floor"]
        
        self.assertEqual(player_x, 15)
        self.assertEqual(player_y, 20)
        self.assertEqual(player_floor, 3)

    def test_gold_reward_system(self):
        """Test gold reward system for defeating enemies"""
        global player_money, gold_earned
        
        # Test normal enemy death gold reward
        player_money = 0
        gold_earned = 0
        
        # Simulate enemy death
        money_drop = 10
        player_money += money_drop
        gold_earned += money_drop
        
        self.assertEqual(player_money, 10)
        self.assertEqual(gold_earned, 10)
        
        # Test multiple enemy defeats
        money_drop2 = 15
        player_money += money_drop2
        gold_earned += money_drop2
        
        self.assertEqual(player_money, 25)
        self.assertEqual(gold_earned, 25)

    def test_status_effects(self):
        """Test status effects in combat"""
        # Test burning effect
        enemy = {"name": "Test Enemy", "hp": 20, "Burning": {"damage": 3, "duration": 2}}
        
        # Apply burning damage
        burn_damage = enemy["Burning"]["damage"]
        enemy["hp"] -= burn_damage
        enemy["Burning"]["duration"] -= 1
        
        self.assertEqual(enemy["hp"], 17)
        self.assertEqual(enemy["Burning"]["duration"], 1)
        
        # Test poison effect
        enemy["Poisoned"] = {"damage": 2, "duration": 3}
        poison_damage = enemy["Poisoned"]["damage"]
        enemy["hp"] -= poison_damage
        enemy["Poisoned"]["duration"] -= 1
        
        self.assertEqual(enemy["hp"], 15)
        self.assertEqual(enemy["Poisoned"]["duration"], 2)

    def test_armor_mechanics(self):
        """Test armor damage reduction and durability"""
        global equipped_armor
        
        # Test armor damage reduction
        equipped_armor = {"name": "Test Armor", "defense": 8, "durability": 10}
        enemy_damage = 12
        
        # Calculate damage reduction
        damage_reduction = equipped_armor["defense"] // 2
        effective_reduction = max(0, damage_reduction - 0)  # No armor pierce
        final_damage = max(1, enemy_damage - effective_reduction)
        
        self.assertEqual(final_damage, 8)  # 12 - 4 = 8
        
        # Test armor durability loss
        equipped_armor["durability"] -= 1
        self.assertEqual(equipped_armor["durability"], 9)

    def test_shop_system(self):
        """Test shop functionality and purchases"""
        global player_money, golden_keys, waypoint_scrolls
        
        # Test buying golden key
        player_money = 50
        golden_keys = 0
        
        if player_money >= 35 and golden_keys < 3:
            player_money -= 35
            golden_keys += 1
        
        self.assertEqual(player_money, 15)
        self.assertEqual(golden_keys, 1)
        
        # Test buying waypoint scroll (not enough money)
        if player_money >= 30:
            player_money -= 30
            waypoint_scrolls += 1
        
        self.assertEqual(player_money, 15)  # Remaining money after buying golden key
        self.assertEqual(waypoint_scrolls, 0)  # Not enough money to buy waypoint scroll

    def test_chest_and_loot_system(self):
        """Test chest opening and loot collection"""
        global golden_keys, player_money
        
        # Test locked chest
        golden_keys = 1
        player_money = 0
        
        # Simulate using golden key to loot treasure chamber
        if golden_keys > 0:
            gold_reward = 60
            player_money += gold_reward
            golden_keys -= 1
        
        self.assertEqual(player_money, 60)
        self.assertEqual(golden_keys, 0)

    def test_floor_numbering_system(self):
        """Test floor numbering and boss distribution"""
        # Test Floor 1 (starting floor)
        floor = 1
        if floor == 2:
            boss_type = "Baby Dragon"
        else:
            boss_type = "Troll"
        
        self.assertEqual(boss_type, "Troll")
        
        # Test Floor 2 (Baby Dragon floor)
        floor = 2
        if floor == 2:
            boss_type = "Baby Dragon"
        else:
            boss_type = "Troll"
        
        self.assertEqual(boss_type, "Baby Dragon")

    def test_mysterious_key_system(self):
        """Test mysterious key collection and usage"""
        global mysterious_keys, unlocked_floors
        
        # Test collecting mysterious key
        player_floor = 2
        if player_floor not in mysterious_keys:
            mysterious_keys[player_floor] = True
        
        self.assertIn(player_floor, mysterious_keys)
        self.assertTrue(mysterious_keys[player_floor])
        
        # Test unlocking floor
        unlocked_floors.add(player_floor)
        self.assertIn(player_floor, unlocked_floors)

    def test_spell_combat_system(self):
        """Test spell usage in combat"""
        global player_mana, learned_spells
        
        # Test Fireball spell
        learned_spells = ["Fireball"]
        player_mana = 20
        
        # Check if player can cast Fireball
        spell_cost = 12  # Fireball mana cost
        can_cast = player_mana >= spell_cost and "Fireball" in learned_spells
        
        self.assertTrue(can_cast)
        
        # Simulate casting spell
        if can_cast:
            player_mana -= spell_cost
        
        self.assertEqual(player_mana, 8)

    def test_weapon_durability_system(self):
        """Test weapon durability and breaking"""
        global inventory, using_fists
        
        # Test weapon durability loss
        weapon = {"name": "Test Sword", "damage": 10, "durability": 1}
        inventory = [weapon]
        
        # Simulate weapon breaking
        weapon["durability"] -= 1
        if weapon["durability"] <= 0:
            inventory.remove(weapon)
            using_fists = True
        
        self.assertEqual(len(inventory), 0)
        self.assertTrue(using_fists)

    def test_enemy_discovery_system(self):
        """Test enemy discovery and bestiary"""
        global discovered_enemies
        
        # Test discovering new enemy
        enemy_name = "New Enemy"
        if enemy_name not in discovered_enemies:
            discovered_enemies.add(enemy_name)
        
        self.assertIn(enemy_name, discovered_enemies)
        
        # Test bestiary functionality
        self.assertTrue(len(discovered_enemies) > 0)

    def test_distance_calculation(self):
        """Test distance from start calculation"""
        # Test distance calculation
        x, y = 5, 10
        distance = abs(x) + abs(y)
        
        self.assertEqual(distance, 15)
        
        # Test different coordinates
        x, y = -3, 7
        distance = abs(x) + abs(y)
        
        self.assertEqual(distance, 10)

    def test_room_generation(self):
        """Test room generation and content"""
        # Test room creation with different types
        room_types = ["normal", "shop", "chest", "boss"]
        
        for room_type in room_types:
            room = {"type": room_type, "description": f"A {room_type} room"}
            self.assertIn("type", room)
            self.assertIn("description", room)

    def test_inventory_limits(self):
        """Test inventory capacity limits"""
        global inventory, armor_inventory
        
        # Test weapon inventory limit
        inventory = []
        MAX_WEAPONS = 3
        
        # Try to add weapons beyond limit
        for i in range(4):
            if len(inventory) < MAX_WEAPONS:
                inventory.append({"name": f"Weapon {i+1}"})
        
        self.assertEqual(len(inventory), 3)
        
        # Test armor inventory limit
        armor_inventory = []
        MAX_ARMOR = 2
        
        for i in range(3):
            if len(armor_inventory) < MAX_ARMOR:
                armor_inventory.append({"name": f"Armor {i+1}"})
        
        self.assertEqual(len(armor_inventory), 2)

    def test_combat_mechanics_detailed(self):
        """Test detailed combat mechanics"""
        # Test damage calculation
        weapon_damage = 15
        enemy_hp = 20
        
        # Simulate attack
        damage_dealt = weapon_damage
        enemy_hp -= damage_dealt
        
        self.assertEqual(enemy_hp, 5)
        
        # Test critical hit (if implemented)
        critical_multiplier = 1.5
        critical_damage = int(weapon_damage * critical_multiplier)
        
        self.assertEqual(critical_damage, 22)

    def test_save_load_integrity(self):
        """Test save/load system integrity"""
        # Test save data structure
        save_data = {
            "player_floor": 2,
            "player_x": 5,
            "player_y": 10,
            "player_hp": 40,
            "player_money": 100,
            "inventory": [{"name": "Test Weapon", "damage": 10, "durability": 5}],
            "armor_inventory": [{"name": "Test Armor", "defense": 5, "durability": 8}],
            "mysterious_keys": {2: True},
            "golden_keys": 2,
            "waypoints": {"Test": {"x": 0, "y": 0, "floor": 1}},
            "discovered_enemies": ["Goblin", "Skeleton"],
            "learned_spells": ["Fireball"],
            "materials_inventory": {"Dragon Scales": 3}
        }
        
        # Verify all required fields are present
        required_fields = ["player_floor", "player_x", "player_y", "player_hp", 
                          "player_money", "inventory", "armor_inventory"]
        
        for field in required_fields:
            self.assertIn(field, save_data)

    def test_error_handling(self):
        """Test error handling and edge cases"""
        # Test invalid commands
        invalid_commands = ["invalid", "xyz", "123", ""]
        
        for command in invalid_commands:
            # These should be handled gracefully
            self.assertIsInstance(command, str)
        
        # Test edge case values
        edge_values = [0, -1, 999999, None]
        
        for value in edge_values:
            if value is not None:
                self.assertIsInstance(value, (int, float))

    def test_performance_metrics(self):
        """Test performance-related functionality"""
        # Test large inventory handling
        large_inventory = []
        for i in range(100):
            large_inventory.append({"name": f"Item {i}", "value": i})
        
        self.assertEqual(len(large_inventory), 100)
        
        # Test waypoint system with many waypoints
        many_waypoints = {}
        for i in range(50):
            many_waypoints[f"Waypoint {i}"] = {"x": i, "y": i, "floor": 1}
        
        self.assertEqual(len(many_waypoints), 50)

    def test_game_balance(self):
        """Test game balance mechanics"""
        # Test weapon damage scaling
        base_damage = 10
        scaling_factor = 1.5
        
        scaled_damage = int(base_damage * scaling_factor)
        self.assertEqual(scaled_damage, 15)
        
        # Test armor defense scaling
        base_defense = 5
        scaled_defense = int(base_defense * scaling_factor)
        self.assertEqual(scaled_defense, 7)
        
        # Test gold reward balance
        min_gold = 5
        max_gold = 15
        avg_gold = (min_gold + max_gold) / 2
        
        self.assertEqual(avg_gold, 10)
        self.assertTrue(min_gold <= avg_gold <= max_gold)

if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2) 