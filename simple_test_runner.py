#!/usr/bin/env python3
"""
Simple Test Runner - Bypasses paging issues
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def run_enemy_spawning_test():
    """Run the enemy spawning test without paging issues"""
    print("Running Enemy Spawning Test...")
    print("=" * 50)
    
    try:
        # Import the test class
        from test_enemy_spawning import TestEnemySpawning
        
        # Create test instance
        test = TestEnemySpawning()
        test.setUp()
        
        # Run each test method manually
        test_methods = [
            test.test_basic_enemy_spawning,
            test.test_boss_enemy_spawning,
            test.test_enemy_scaling,
            test.test_spider_swarm_spawning,
            test.test_enemy_stats_consistency,
            test.test_enemy_armor_piercing,
            test.test_special_enemy_properties,
            test.test_enemy_creation_edge_cases
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
        print("TEST RESULTS")
        print("=" * 50)
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(f"Total: {passed + failed}")
        
        if failed == 0:
            print("🎉 All tests passed!")
            return True
        else:
            print("❌ Some tests failed!")
            return False
            
    except ImportError as e:
        print(f"❌ Could not import test: {e}")
        return False
    except Exception as e:
        print(f"❌ Error running test: {e}")
        return False

if __name__ == "__main__":
    success = run_enemy_spawning_test()
    sys.exit(0 if success else 1)
