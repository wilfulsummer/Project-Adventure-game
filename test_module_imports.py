#!/usr/bin/env python3
"""
Module Import Test - Simple test to verify modules can be imported
"""

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing module imports...")
    
    try:
        # Test world_generation imports
        from world_generation import create_enemy, create_spider_swarm
        print("✅ world_generation module imported successfully")
        
        # Test constants imports
        from constants import enemy_stats, weapon_names, spells
        print("✅ constants module imported successfully")
        
        # Test basic function calls
        enemy = create_enemy(10, 10)
        print(f"✅ create_enemy() works: {enemy['name']}")
        
        swarm = create_spider_swarm(15, 15)
        print(f"✅ create_spider_swarm() works: {len(swarm)} spiders")
        
        print(f"✅ enemy_stats: {list(enemy_stats.keys())}")
        print(f"✅ weapon_names: {weapon_names}")
        print(f"✅ spells: {list(spells.keys())}")
        
        print("\n🎉 All module imports and basic functions work!")
        return True
        
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_imports()
    if success:
        print("\nModule test completed successfully!")
    else:
        print("\nModule test failed!")
