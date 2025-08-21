#!/usr/bin/env python3
"""
Test runner for Adventure Game unit tests
"""

import unittest
import sys
import os

# Disable paging to prevent terminal issues
os.environ['PAGER'] = 'cat'
os.environ['LESS'] = 'FRX'
os.environ['MORE'] = 'FRX'

# Add the current directory to the path so we can import game modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def run_tests():
    """Run all unit tests for the adventure game"""
    print("=" * 60)
    print("ADVENTURE GAME UNIT TEST SUITE")
    print("=" * 60)
    print("Paging disabled to prevent terminal issues")
    print("=" * 60)
    
    # Discover and run tests
    loader = unittest.TestLoader()
    suite = loader.discover('.', pattern='test_*.py')
    
    # Use a custom runner that handles output better
    runner = unittest.TextTestRunner(
        verbosity=2,
        stream=sys.stdout,  # Force output to stdout
        buffer=False  # Disable output buffering
    )
    
    try:
        result = runner.run(suite)
    except Exception as e:
        print(f"\n❌ Error running tests: {e}")
        return 1
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    
    if result.failures:
        print("\nFAILURES:")
        for test, traceback in result.failures:
            print(f"\n{test}:")
            print(traceback)
    
    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            print(f"\n{test}:")
            print(traceback)
    
    if result.wasSuccessful():
        print("\n✅ All tests passed!")
        return 0
    else:
        print("\n❌ Some tests failed!")
        return 1

def run_specific_test(test_name):
    """Run a specific test by name"""
    print(f"Running specific test: {test_name}")
    
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromName(f"test_adventure_game.TestAdventureGame.{test_name}")
    
    runner = unittest.TextTestRunner(
        verbosity=2,
        stream=sys.stdout,
        buffer=False
    )
    result = runner.run(suite)
    
    return 0 if result.wasSuccessful() else 1

def run_enemy_spawning_test():
    """Run the enemy spawning test specifically"""
    print("Running Enemy Spawning Test...")
    
    try:
        # Import and run the enemy spawning test
        from test_enemy_spawning import TestEnemySpawning
        
        suite = unittest.TestLoader().loadTestsFromTestCase(TestEnemySpawning)
        runner = unittest.TextTestRunner(
            verbosity=2,
            stream=sys.stdout,
            buffer=False
        )
        result = runner.run(suite)
        
        return 0 if result.wasSuccessful() else 1
        
    except ImportError as e:
        print(f"❌ Could not import enemy spawning test: {e}")
        return 1
    except Exception as e:
        print(f"❌ Error running enemy spawning test: {e}")
        return 1

if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Run specific test
        test_name = sys.argv[1]
        if test_name == "enemy_spawning":
            exit_code = run_enemy_spawning_test()
        else:
            exit_code = run_specific_test(test_name)
    else:
        # Run all tests
        exit_code = run_tests()
    
    sys.exit(exit_code) 