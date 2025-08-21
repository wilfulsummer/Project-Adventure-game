#!/usr/bin/env python3
"""
Combat Test Runner - Runs enemy combat tests without paging issues
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def run_combat_tests():
    """Run the enemy combat tests"""
    print("Running Enemy Combat Tests...")
    print("=" * 50)
    
    try:
        # Import the test class
        from test_enemy_combat import TestEnemyCombat
        
        # Create test instance
        test = TestEnemyCombat()
        test.setUp()
        
        # Run each test method manually
        test_methods = [
            test.test_enemy_attack_mechanics,
            test.test_boss_combat_mechanics,
            test.test_enemy_special_abilities,
            test.test_spider_swarm_combat,
            test.test_enemy_combat_scenarios,
            test.test_enemy_health_and_durability,
            test.test_enemy_combat_balance
        ]
        
        passed = 0
        failed = 0
        
        for method in test_methods:
            try:
                print(f"\nRunning: {method.__name__}")
                method()
                print(f"✅ {method.__name__} PASSED")
                passed += 1
            except Exception as e:
                print(f"❌ {method.__name__} FAILED: {e}")
                failed += 1
        
        print("\n" + "=" * 50)
        print("COMBAT TEST RESULTS")
        print("=" * 50)
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(f"Total: {passed + failed}")
        
        if failed == 0:
            print("🎉 All combat tests passed!")
            return True
        else:
            print("❌ Some combat tests failed!")
            return False
            
    except ImportError as e:
        print(f"❌ Could not import combat test: {e}")
        return False
    except Exception as e:
        print(f"❌ Error running combat test: {e}")
        return False

if __name__ == "__main__":
    success = run_combat_tests()
    sys.exit(0 if success else 1)
