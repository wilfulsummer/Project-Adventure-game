#!/usr/bin/env python3
"""
Quick Enemy Test - Simple import and function test
"""

print("Starting Quick Enemy Test...")
print("=" * 40)

try:
    print("1. Importing modules...")
    from world_generation import create_enemy, create_spider_swarm
    from constants import enemy_stats
    print("   ✅ Modules imported successfully")
    
    print("\n2. Testing enemy creation...")
    enemy = create_enemy(10, 10)
    print(f"   ✅ Enemy created: {enemy['name']} (HP: {enemy['hp']}, Attack: {enemy['base_attack']})")
    
    print("\n3. Testing boss creation...")
    troll = create_enemy(50, 50, force_boss="Troll")
    print(f"   ✅ Boss created: {troll['name']} (HP: {troll['hp']}, Attack: {troll['base_attack']})")
    
    print("\n4. Testing spider swarm...")
    swarm = create_spider_swarm(25, 25)
    print(f"   ✅ Spider swarm created: {len(swarm)} spiders")
    
    print("\n5. Testing enemy stats...")
    print(f"   Available enemy types: {list(enemy_stats.keys())}")
    
    print("\n🎉 All basic enemy spawning tests passed!")
    
except Exception as e:
    print(f"❌ Test failed: {e}")
    import traceback
    traceback.print_exc()
