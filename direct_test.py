#!/usr/bin/env python3
"""
Direct Test - Bypasses all terminal paging issues
"""

print("🚀 Starting Direct Enemy Combat Tests...")
print("=" * 60)

# Test 1: Module Imports
print("\n1️⃣ Testing Module Imports...")
try:
    from world_generation import create_enemy, create_spider_swarm
    from constants import enemy_stats, weapon_names, spells
    print("   ✅ All modules imported successfully!")
except Exception as e:
    print(f"   ❌ Import failed: {e}")
    exit(1)

# Test 2: Basic Enemy Creation
print("\n2️⃣ Testing Basic Enemy Creation...")
try:
    enemy = create_enemy(25, 25)
    print(f"   ✅ Enemy created: {enemy['name']}")
    print(f"      HP: {enemy['hp']}, Attack: {enemy['base_attack']}, Armor Pierce: {enemy['armor_pierce']}")
except Exception as e:
    print(f"   ❌ Enemy creation failed: {e}")

# Test 3: Boss Creation
print("\n3️⃣ Testing Boss Creation...")
try:
    troll = create_enemy(50, 50, force_boss="Troll")
    print(f"   ✅ Troll boss created: {troll['name']}")
    print(f"      HP: {troll['hp']}, Attack: {troll['base_attack']}, Armor Pierce: {troll['armor_pierce']}")
    print(f"      Is Boss: {troll.get('is_boss', False)}")
    
    dragon = create_enemy(75, 75, force_boss="Baby Dragon")
    print(f"   ✅ Dragon boss created: {dragon['name']}")
    print(f"      HP: {dragon['hp']}, Attack: {dragon['base_attack']}, Armor Pierce: {dragon['armor_pierce']}")
    print(f"      Is Boss: {dragon.get('is_boss', False)}")
except Exception as e:
    print(f"   ❌ Boss creation failed: {e}")

# Test 4: Spider Swarm
print("\n4️⃣ Testing Spider Swarm...")
try:
    swarm = create_spider_swarm(25, 25)
    print(f"   ✅ Spider swarm created: {len(swarm)} spiders")
    total_attack = sum(spider['base_attack'] for spider in swarm)
    print(f"      Total swarm attack power: {total_attack}")
    for i, spider in enumerate(swarm):
        print(f"      Spider {i+1}: HP {spider['hp']}, Attack {spider['base_attack']}")
except Exception as e:
    print(f"   ❌ Spider swarm failed: {e}")

# Test 5: Enemy Scaling
print("\n5️⃣ Testing Enemy Scaling...")
try:
    close_enemy = create_enemy(5, 5)
    far_enemy = create_enemy(100, 100)
    print(f"   ✅ Close enemy: {close_enemy['name']} - HP {close_enemy['hp']}, Attack {close_enemy['base_attack']}")
    print(f"   ✅ Far enemy: {far_enemy['name']} - HP {far_enemy['hp']}, Attack {far_enemy['base_attack']}")
    print(f"      Scaling check: Far enemy should be stronger")
except Exception as e:
    print(f"   ❌ Enemy scaling test failed: {e}")

# Test 6: Combat Scenarios
print("\n6️⃣ Testing Combat Scenarios...")
try:
    # Scenario 1: Unarmored player vs regular enemy
    enemy = create_enemy(30, 30)
    player_hp = 50
    player_armor = 0
    
    damage = enemy['base_attack']
    final_damage = max(1, damage - player_armor)
    player_hp -= final_damage
    
    print(f"   ✅ Scenario 1: {enemy['name']} vs unarmored player")
    print(f"      Enemy attack: {damage}, Final damage: {final_damage}, Player HP after: {player_hp}")
    
    # Scenario 2: Armored player vs boss
    boss = create_enemy(60, 60, force_boss="Troll")
    player_hp = 100
    player_armor = 8
    
    damage = boss['base_attack']
    armor_pierce = boss['armor_pierce']
    effective_armor = max(0, player_armor - armor_pierce)
    final_damage = max(1, damage - effective_armor)
    player_hp -= final_damage
    
    print(f"   ✅ Scenario 2: {boss['name']} vs armored player")
    print(f"      Boss attack: {damage}, Effective armor: {effective_armor}, Final damage: {final_damage}, Player HP after: {player_hp}")
    
except Exception as e:
    print(f"   ❌ Combat scenarios failed: {e}")

# Test 7: Special Enemy Properties
print("\n7️⃣ Testing Special Enemy Properties...")
try:
    # Test multiple enemies to find special ones
    for _ in range(10):
        enemy = create_enemy(25, 25)
        if enemy['name'] == "Rat":
            print(f"   ✅ Rat found: {enemy.get('extra_turns', 'No extra turns')} extra turns, damage {enemy['base_attack']}")
            break
        elif enemy['name'] == "Spider":
            print(f"   ✅ Spider found: Very low damage {enemy['base_attack']}")
            break
    else:
        print("   ⚠️  Special enemies not found in test sample")
        
except Exception as e:
    print(f"   ❌ Special properties test failed: {e}")

# Test 8: Available Enemy Types
print("\n8️⃣ Available Enemy Types...")
try:
    print(f"   ✅ Enemy types from constants: {list(enemy_stats.keys())}")
    print(f"   ✅ Weapon types: {weapon_names}")
    print(f"   ✅ Spell types: {list(spells.keys())}")
except Exception as e:
    print(f"   ❌ Enemy types test failed: {e}")

print("\n" + "=" * 60)
print("🎉 Direct Enemy Combat Tests Completed!")
print("=" * 60)
print("All tests run without terminal paging issues!")
print("Check the output above for any failures.")
