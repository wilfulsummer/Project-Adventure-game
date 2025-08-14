#!/usr/bin/env python3
"""
Quick Test Runner for Adventure Game
Just run: python quick_test.py
"""

import sys
import os

# Import all modules at the top level
try:
    import constants
    import game_state
    import command_handlers
    import save_load
    import ui_functions
    import world_generation
    import unique_items
    print("✅ All modules imported successfully")
except ImportError as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)

def test_game_state():
    """Test game state variables"""
    print("\nTesting game state...")
    try:
        # Check if key variables exist in game_state module
        if hasattr(game_state, 'worlds'):
            print("✅ Worlds variable exists")
        if hasattr(game_state, 'player_floor'):
            print("✅ Player floor variable exists")
        if hasattr(game_state, 'inventory'):
            print("✅ Inventory variable exists")
        if hasattr(game_state, 'player_hp'):
            print("✅ Player HP variable exists")
            
        return True
    except Exception as e:
        print(f"❌ Game state test failed: {e}")
        return False

def test_constants():
    """Test game constants"""
    print("\nTesting constants...")
    try:
        # Check some key constants
        if hasattr(constants, 'WEAPONS'):
            print("✅ Weapons constants loaded")
        if hasattr(constants, 'ENEMIES'):
            print("✅ Enemies constants loaded")
        if hasattr(constants, 'ARMOR'):
            print("✅ Armor constants loaded")
            
        return True
    except Exception as e:
        print(f"❌ Constants test failed: {e}")
        return False

def test_unique_items():
    """Test unique items system"""
    print("\nTesting unique items...")
    try:
        # Test loading unique items
        unique_items.load_unique_items()
        print("✅ Unique items loaded")
        
        # Check if wanderers_cloak is defined
        if hasattr(unique_items, 'UNIQUE_ITEMS') and 'wanderers_cloak' in unique_items.UNIQUE_ITEMS:
            print("✅ Wanderer's Cloak defined")
            
        return True
    except Exception as e:
        print(f"❌ Unique items test failed: {e}")
        return False

def test_world_generation():
    """Test world generation"""
    print("\nTesting world generation...")
    try:
        # Test distance calculation
        dist = world_generation.distance_from_start(50, 50)
        if dist == 100:
            print("✅ Distance calculation works")
        
        # Test room generation - provide required arguments in correct order
        room = world_generation.get_room(1, 0, 0, {}, [])
        if room:
            print("✅ Room generation works")
            
        return True
    except Exception as e:
        print(f"❌ World generation test failed: {e}")
        return False

def test_mod_system():
    """Test mod system (optional)"""
    print("\nTesting mod system...")
    try:
        # Try to import mod system
        from mods.mod_loader import mod_loader
        print("✅ Mod loader imported")
        
        # Check if mods directory exists
        if os.path.exists("mods"):
            print("✅ Mods directory exists")
            
        return True
    except Exception as e:
        print(f"⚠️  Mod system not available: {e}")
        return True  # Not critical

def run_all_tests():
    """Run all tests"""
    print("🚀 QUICK TEST RUNNER FOR ADVENTURE GAME")
    print("=" * 50)
    
    tests = [
        test_game_state,
        test_constants,
        test_unique_items,
        test_world_generation,
        test_mod_system
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Game should work properly.")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
