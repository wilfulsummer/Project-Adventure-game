#!/usr/bin/env python3
"""
Test Enemy Spawning
Tests that all enemy types can be spawned correctly
"""

import unittest
import random
import os
import sys

# Disable paging to prevent terminal issues
os.environ['PAGER'] = 'cat'
os.environ['LESS'] = 'FRX'
os.environ['MORE'] = 'FRX'

# Import game modules
from world_generation import create_enemy, create_spider_swarm
from constants import enemy_stats

class TestEnemySpawning(unittest.TestCase):
    """Test that all enemy types can be spawned correctly"""
    
    def setUp(self):
        """Set up test environment"""
        # Set random seed for consistent testing
        random.seed(42)
        # Force output to stdout and disable buffering
        sys.stdout.flush()
    
    def test_basic_enemy_spawning(self):
        """Test that all basic enemy types can be spawned"""
        print("\n=== Testing Basic Enemy Spawning ===")
        sys.stdout.flush()
        
        # Test each enemy type from constants
        for enemy_name in enemy_stats.keys():
            print(f"Testing {enemy_name} spawning...")
            sys.stdout.flush()
            
            # Create enemy at different distances
            for distance in [0, 25, 50, 75, 100]:
                x, y = distance, 0  # Simple distance calculation
                enemy = create_enemy(x, y)
                
                # Verify enemy was created
                self.assertIsNotNone(enemy, f"Failed to create {enemy_name}")
                self.assertEqual(enemy["name"], enemy_name, f"Wrong enemy name for {enemy_name}")
                self.assertGreater(enemy["hp"], 0, f"Invalid HP for {enemy_name}")
                self.assertGreater(enemy["base_attack"], 0, f"Invalid attack for {enemy_name}")
                
                print(f"  ✓ {enemy_name} at distance {distance}: HP={enemy['hp']}, Attack={enemy['base_attack']}")
                sys.stdout.flush()
    
    def test_boss_enemy_spawning(self):
        """Test that boss enemies can be spawned"""
        print("\n=== Testing Boss Enemy Spawning ===")
        sys.stdout.flush()
        
        # Test Troll boss
        print("Testing Troll boss spawning...")
        sys.stdout.flush()
        troll = create_enemy(50, 50, force_boss="Troll")
        self.assertIsNotNone(troll, "Failed to create Troll boss")
        self.assertEqual(troll["name"], "Troll", "Wrong name for Troll boss")
        self.assertTrue(troll["is_boss"], "Troll should be marked as boss")
        self.assertGreater(troll["hp"], 50, "Troll should have high HP")
        self.assertGreater(troll["base_attack"], 8, "Troll should have high attack")
        print(f"  ✓ Troll Boss: HP={troll['hp']}, Attack={troll['base_attack']}")
        sys.stdout.flush()
        
        # Test Baby Dragon boss
        print("Testing Baby Dragon boss spawning...")
        sys.stdout.flush()
        dragon = create_enemy(75, 75, force_boss="Baby Dragon")
        self.assertIsNotNone(dragon, "Failed to create Baby Dragon boss")
        self.assertEqual(dragon["name"], "Baby Dragon", "Wrong name for Baby Dragon boss")
        self.assertTrue(dragon["is_boss"], "Baby Dragon should be marked as boss")
        self.assertGreater(dragon["hp"], 60, "Baby Dragon should have high HP")
        self.assertGreater(dragon["base_attack"], 10, "Baby Dragon should have high attack")
        print(f"  ✓ Baby Dragon Boss: HP={dragon['hp']}, Attack={dragon['base_attack']}")
        sys.stdout.flush()
    
    def test_enemy_scaling(self):
        """Test that enemies scale properly with distance"""
        print("\n=== Testing Enemy Scaling ===")
        sys.stdout.flush()
        
        # Test scaling with distance
        base_enemy = create_enemy(0, 0)
        far_enemy = create_enemy(100, 100)
        
        # Far enemies should generally be stronger
        self.assertGreaterEqual(far_enemy["hp"], base_enemy["hp"], "Far enemies should have more HP")
        self.assertGreaterEqual(far_enemy["base_attack"], base_enemy["base_attack"], "Far enemies should have more attack")
        
        print(f"  ✓ Base enemy (0,0): HP={base_enemy['hp']}, Attack={base_enemy['base_attack']}")
        print(f"  ✓ Far enemy (100,100): HP={far_enemy['hp']}, Attack={far_enemy['base_attack']}")
        sys.stdout.flush()
    
    def test_spider_swarm_spawning(self):
        """Test that spider swarms can be spawned"""
        print("\n=== Testing Spider Swarm Spawning ===")
        sys.stdout.flush()
        
        # Test spider swarm creation
        swarm = create_spider_swarm(25, 25)
        self.assertIsNotNone(swarm, "Failed to create spider swarm")
        self.assertIsInstance(swarm, list, "Spider swarm should be a list")
        self.assertGreaterEqual(len(swarm), 2, "Spider swarm should have at least 2 spiders")
        self.assertLessEqual(len(swarm), 4, "Spider swarm should have at most 4 spiders")
        
        # Check each spider in the swarm
        for i, spider in enumerate(swarm):
            self.assertEqual(spider["name"], "Spider", f"Spider {i} should be named 'Spider'")
            self.assertGreater(spider["hp"], 0, f"Spider {i} should have positive HP")
            self.assertGreater(spider["base_attack"], 0, f"Spider {i} should have positive attack")
        
        print(f"  ✓ Spider Swarm: {len(swarm)} spiders created")
        for i, spider in enumerate(swarm):
            print(f"    Spider {i+1}: HP={spider['hp']}, Attack={spider['base_attack']}")
        sys.stdout.flush()
    
    def test_enemy_stats_consistency(self):
        """Test that enemy stats are consistent and valid"""
        print("\n=== Testing Enemy Stats Consistency ===")
        sys.stdout.flush()
        
        # Test multiple spawns of the same enemy type
        enemy_type = "Goblin"
        print(f"Testing {enemy_type} consistency...")
        sys.stdout.flush()
        
        enemies = []
        for _ in range(5):
            enemy = create_enemy(25, 25)
            if enemy["name"] == enemy_type:
                enemies.append(enemy)
        
        if enemies:
            # Check that stats are reasonable (not identical due to randomization)
            hps = [e["hp"] for e in enemies]
            attacks = [e["base_attack"] for e in enemies]
            
            self.assertGreater(len(set(hps)), 1, f"{enemy_type} HP should vary between spawns")
            self.assertGreater(len(set(attacks)), 1, f"{enemy_type} attack should vary between spawns")
            
            print(f"  ✓ {enemy_type} stats vary between spawns (good randomization)")
            print(f"    HP range: {min(hps)} - {max(hps)}")
            print(f"    Attack range: {min(attacks)} - {max(attacks)}")
        else:
            print(f"  ⚠ {enemy_type} not spawned in test (random chance)")
        sys.stdout.flush()
    
    def test_enemy_armor_piercing(self):
        """Test that enemies have appropriate armor piercing values"""
        print("\n=== Testing Enemy Armor Piercing ===")
        sys.stdout.flush()
        
        # Test regular enemies
        regular_enemy = create_enemy(25, 25)
        self.assertIn("armor_pierce", regular_enemy, "Regular enemies should have armor_pierce")
        self.assertGreaterEqual(regular_enemy["armor_pierce"], 0, "Armor pierce should be non-negative")
        
        # Test boss enemies
        boss_enemy = create_enemy(50, 50, force_boss="Troll")
        self.assertIn("armor_pierce", boss_enemy, "Boss enemies should have armor_pierce")
        self.assertGreater(boss_enemy["armor_pierce"], regular_enemy["armor_pierce"], "Bosses should have higher armor pierce")
        
        print(f"  ✓ Regular enemy armor pierce: {regular_enemy['armor_pierce']}")
        print(f"  ✓ Boss enemy armor pierce: {boss_enemy['armor_pierce']}")
        sys.stdout.flush()
    
    def test_special_enemy_properties(self):
        """Test that special enemies have their unique properties"""
        print("\n=== Testing Special Enemy Properties ===")
        sys.stdout.flush()
        
        # Test Rat special properties
        rat = create_enemy(25, 25)
        if rat["name"] == "Rat":
            self.assertIn("extra_turns", rat, "Rat should have extra_turns property")
            self.assertEqual(rat["extra_turns"], 2, "Rat should have 2 extra turns")
            self.assertLess(rat["base_attack"], 10, "Rat should have reduced damage")
            print(f"  ✓ Rat has extra_turns: {rat['extra_turns']}, reduced damage: {rat['base_attack']}")
        
        # Test Spider special properties
        spider = create_enemy(25, 25)
        if spider["name"] == "Spider":
            self.assertLess(spider["base_attack"], 8, "Spider should have very low damage")
            print(f"  ✓ Spider has very low damage: {spider['base_attack']}")
        sys.stdout.flush()
    
    def test_enemy_creation_edge_cases(self):
        """Test enemy creation at edge cases"""
        print("\n=== Testing Edge Cases ===")
        sys.stdout.flush()
        
        # Test at very far distances
        far_enemy = create_enemy(200, 200)
        self.assertIsNotNone(far_enemy, "Should create enemy at far distance")
        self.assertLessEqual(far_enemy["hp"], 50, "Enemy HP should be capped at reasonable levels")
        
        # Test at negative coordinates
        neg_enemy = create_enemy(-50, -50)
        self.assertIsNotNone(neg_enemy, "Should create enemy at negative coordinates")
        
        print(f"  ✓ Far distance enemy created: HP={far_enemy['hp']}")
        print(f"  ✓ Negative coordinate enemy created: HP={neg_enemy['hp']}")
        sys.stdout.flush()

if __name__ == "__main__":
    # Disable paging and run tests
    print("Enemy Spawning Test - Paging Disabled")
    print("=" * 50)
    
    # Run the tests
    unittest.main(verbosity=2, exit=False)
