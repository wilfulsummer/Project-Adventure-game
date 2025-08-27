#!/usr/bin/env python3
"""
Enemy Combat Tests
Tests enemy behavior, attacks, and combat mechanics without running the full game
"""

import unittest
import random
from world_generation import create_enemy, create_spider_swarm
from constants import enemy_stats

class TestEnemyCombat(unittest.TestCase):
    """Test enemy combat behavior and mechanics"""
    
    def setUp(self):
        """Set up test environment"""
        random.seed(42)  # Consistent testing
    
    def test_enemy_attack_mechanics(self):
        """Test that enemies can attack and deal damage"""
        print("\n=== Testing Enemy Attack Mechanics ===")
        
        # Create a regular enemy
        enemy = create_enemy(25, 25)
        print(f"Testing {enemy['name']} attack mechanics...")
        
        # Test basic attack properties
        self.assertIn('base_attack', enemy, "Enemy should have base_attack")
        self.assertIn('armor_pierce', enemy, "Enemy should have armor_pierce")
        self.assertGreater(enemy['base_attack'], 0, "Enemy should have positive attack")
        self.assertGreaterEqual(enemy['armor_pierce'], 0, "Enemy should have non-negative armor pierce")
        
        print(f"  ✅ {enemy['name']}: Attack {enemy['base_attack']}, Armor Pierce {enemy['armor_pierce']}")
        
        # Test that attack scales with distance
        close_enemy = create_enemy(5, 5)
        far_enemy = create_enemy(100, 100)
        
        self.assertGreaterEqual(far_enemy['base_attack'], close_enemy['base_attack'], 
                               "Far enemies should have higher attack")
        
        print(f"  ✅ Attack scaling: Close {close_enemy['base_attack']} vs Far {far_enemy['base_attack']}")
    
    def test_boss_combat_mechanics(self):
        """Test boss enemy combat mechanics"""
        print("\n=== Testing Boss Combat Mechanics ===")
        
        # Test Troll boss
        troll = create_enemy(50, 50, force_boss="Troll")
        print(f"Testing {troll['name']} boss mechanics...")
        
        self.assertTrue(troll['is_boss'], "Troll should be marked as boss")
        self.assertGreater(troll['hp'], 50, "Troll should have high HP")
        self.assertGreater(troll['base_attack'], 8, "Troll should have high attack")
        self.assertGreater(troll['armor_pierce'], 1, "Boss should have significant armor pierce")
        
        print(f"  ✅ {troll['name']}: HP {troll['hp']}, Attack {troll['base_attack']}, Armor Pierce {troll['armor_pierce']}")
        
        # Test Baby Dragon boss
        dragon = create_enemy(75, 75, force_boss="Baby Dragon")
        print(f"Testing {dragon['name']} boss mechanics...")
        
        self.assertTrue(dragon['is_boss'], "Dragon should be marked as boss")
        self.assertGreater(dragon['hp'], 60, "Dragon should have high HP")
        self.assertGreater(dragon['base_attack'], 10, "Dragon should have high attack")
        
        print(f"  ✅ {dragon['name']}: HP {dragon['hp']}, Attack {dragon['base_attack']}, Armor Pierce {dragon['armor_pierce']}")
    
    def test_enemy_special_abilities(self):
        """Test special enemy abilities and properties"""
        print("\n=== Testing Enemy Special Abilities ===")
        
        # Test Rat special properties
        rat = create_enemy(25, 25)
        if rat['name'] == "Rat":
            print(f"Testing {rat['name']} special abilities...")
            self.assertIn('extra_turns', rat, "Rat should have extra_turns")
            self.assertEqual(rat['extra_turns'], 2, "Rat should have 2 extra turns")
            self.assertLess(rat['base_attack'], 10, "Rat should have reduced damage")
            print(f"  ✅ {rat['name']}: {rat['extra_turns']} extra turns, reduced damage {rat['base_attack']}")
        
        # Test Spider special properties
        spider = create_enemy(25, 25)
        if spider['name'] == "Spider":
            print(f"Testing {spider['name']} special abilities...")
            self.assertLess(spider['base_attack'], 8, "Spider should have very low damage")
            print(f"  ✅ {spider['name']}: Very low damage {spider['base_attack']}")
    
    def test_spider_swarm_combat(self):
        """Test spider swarm combat mechanics"""
        print("\n=== Testing Spider Swarm Combat ===")
        
        swarm = create_spider_swarm(25, 25)
        print(f"Testing spider swarm with {len(swarm)} spiders...")
        
        # Test swarm properties
        self.assertIsInstance(swarm, list, "Swarm should be a list")
        self.assertGreaterEqual(len(swarm), 2, "Swarm should have at least 2 spiders")
        self.assertLessEqual(len(swarm), 4, "Swarm should have at most 4 spiders")
        
        # Test each spider in swarm
        total_attack = 0
        for i, spider in enumerate(swarm):
            self.assertEqual(spider['name'], 'Spider', f"Spider {i} should be named 'Spider'")
            self.assertGreater(spider['hp'], 0, f"Spider {i} should have positive HP")
            self.assertGreater(spider['base_attack'], 0, f"Spider {i} should have positive attack")
            total_attack += spider['base_attack']
            print(f"  Spider {i+1}: HP {spider['hp']}, Attack {spider['base_attack']}")
        
        print(f"  ✅ Swarm total attack power: {total_attack}")
    
    def test_enemy_combat_scenarios(self):
        """Test realistic combat scenarios"""
        print("\n=== Testing Combat Scenarios ===")
        
        # Scenario 1: Player with no armor vs regular enemy
        enemy = create_enemy(30, 30)
        player_hp = 50
        player_armor = 0
        
        # Simulate enemy attack
        damage = enemy['base_attack']
        final_damage = max(1, damage - player_armor)  # Minimum 1 damage
        player_hp -= final_damage
        
        print(f"Scenario 1: {enemy['name']} vs unarmored player")
        print(f"  Enemy attack: {damage}")
        print(f"  Player armor: {player_armor}")
        print(f"  Final damage: {final_damage}")
        print(f"  Player HP after: {player_hp}")
        
        self.assertGreater(final_damage, 0, "Player should take damage")
        self.assertLess(player_hp, 50, "Player HP should decrease")
        
        # Scenario 2: Player with armor vs boss
        boss = create_enemy(60, 60, force_boss="Troll")
        player_hp = 100
        player_armor = 8  # Good armor
        
        # Simulate boss attack with armor piercing
        damage = boss['base_attack']
        armor_pierce = boss['armor_pierce']
        effective_armor = max(0, player_armor - armor_pierce)
        final_damage = max(1, damage - effective_armor)
        player_hp -= final_damage
        
        print(f"\nScenario 2: {boss['name']} vs armored player")
        print(f"  Boss attack: {damage}")
        print(f"  Player armor: {player_armor}")
        print(f"  Boss armor pierce: {armor_pierce}")
        print(f"  Effective armor: {effective_armor}")
        print(f"  Final damage: {final_damage}")
        print(f"  Player HP after: {player_hp}")
        
        self.assertGreater(final_damage, 0, "Player should take damage even with armor")
        self.assertLess(player_hp, 100, "Player HP should decrease")
    
    def test_enemy_health_and_durability(self):
        """Test enemy health and combat durability"""
        print("\n=== Testing Enemy Health & Durability ===")
        
        # Test enemy health scaling
        enemies = []
        for distance in [10, 25, 50, 75, 100]:
            enemy = create_enemy(distance, distance)
            enemies.append((distance, enemy))
        
        print("Enemy health scaling with distance:")
        for distance, enemy in enemies:
            print(f"  Distance {distance}: {enemy['name']} HP {enemy['hp']}")
        
        # Health should generally increase with distance
        for i in range(1, len(enemies)):
            prev_hp = enemies[i-1][1]['hp']
            curr_hp = enemies[i][1]['hp']
            # Allow some variation due to randomization
            self.assertGreaterEqual(curr_hp, prev_hp * 0.8, 
                                  f"Enemy at distance {enemies[i][0]} should not have much lower HP")
    
    def test_enemy_combat_balance(self):
        """Test that enemy combat is reasonably balanced"""
        print("\n=== Testing Combat Balance ===")
        
        # Test that regular enemies aren't too strong
        regular_enemy = create_enemy(25, 25)
        self.assertLess(regular_enemy['base_attack'], 20, "Regular enemies shouldn't be too strong")
        self.assertLess(regular_enemy['hp'], 50, "Regular enemies shouldn't have too much HP")
        
        # Test that bosses are appropriately challenging
        boss = create_enemy(50, 50, force_boss="Troll")
        self.assertGreater(boss['base_attack'], regular_enemy['base_attack'], "Bosses should be stronger")
        self.assertGreater(boss['hp'], regular_enemy['hp'], "Bosses should have more HP")
        
        print(f"  ✅ Regular enemy: Attack {regular_enemy['base_attack']}, HP {regular_enemy['hp']}")
        print(f"  ✅ Boss enemy: Attack {boss['base_attack']}, HP {boss['hp']}")
        print(f"  ✅ Boss is {boss['base_attack'] / regular_enemy['base_attack']:.1f}x stronger in attack")
        print(f"  ✅ Boss has {boss['hp'] / regular_enemy['hp']:.1f}x more HP")

if __name__ == "__main__":
    print("Enemy Combat Test Suite")
    print("=" * 50)
    unittest.main(verbosity=2, exit=False)
