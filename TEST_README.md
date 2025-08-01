# Adventure Game Unit Test Suite

This directory contains a comprehensive unit test suite for the Adventure Game. The tests cover all major game commands and functionality to ensure the game works correctly.

## Files

- `test_adventure_game.py` - Main test suite with all unit tests
- `run_tests.py` - Test runner script for easy execution
- `TEST_README.md` - This documentation file

## Running the Tests

### Run All Tests
```bash
python run_tests.py
```

### Run a Specific Test
```bash
python run_tests.py test_movement_commands
```

### Run Tests with Python's unittest directly
```bash
python -m unittest test_adventure_game.py -v
```

## Test Coverage

The test suite covers the following areas:

### 1. Movement Commands (`test_movement_commands`)
- Basic movement (north, south, east, west)
- Movement blocked by regular enemies
- Movement allowed past boss enemies
- Movement allowed past training dummies

### 2. Combat Commands (`test_attack_command`)
- Attack with no enemy present
- Attack with fists (no weapons)
- Attack with weapons
- Weapon durability loss
- Training dummy (no durability loss)
- Enemy defeat and rewards

### 3. Inventory Management (`test_take_command`, `test_inventory_command`)
- Taking items from rooms
- Inventory limits (max 3 weapons, max 2 armor)
- Displaying inventory contents
- Handling full inventory

### 4. Armor System (`test_armor_command`, `test_drop_armor_command`, `test_equip_command`)
- Displaying armor inventory
- Equipping armor
- Dropping armor
- Armor durability system

### 5. Item Management (`test_drop_command`, `test_switch_command`)
- Dropping weapons
- Switching between weapons
- Using fists as weapon option

### 6. Resource System (`test_absorb_command`)
- Absorbing life crystals
- Absorbing stamina crystals
- Absorbing mana crystals
- Crystal combinations

### 7. Escape Mechanics (`test_run_command`)
- Running from enemies
- Stamina cost for running
- Insufficient stamina handling

### 8. Save/Load System (`test_save_load_commands`)
- Saving game state
- Loading game state
- Data integrity verification

### 9. UI Functions (`test_ui_functions`)
- Map display
- Bestiary display
- Help system

### 10. Game Constants (`test_constants`)
- Weapon limits
- Spell definitions
- Enemy statistics

### 11. Edge Cases (`test_edge_cases`)
- Invalid input handling
- Error conditions
- Boundary conditions

### 12. Combat Mechanics (`test_combat_mechanics`)
- Weapon breaking
- Armor breaking
- Damage calculations

### 13. Spell System (`test_spell_book_functionality`)
- Spell Book usage
- Learned spells
- Mana requirements

## Test Structure

Each test method follows this pattern:
1. **Setup** - Prepare test data and mock objects
2. **Execution** - Call the function being tested
3. **Verification** - Assert expected outcomes
4. **Cleanup** - Reset state for next test

## Mocking

The tests use Python's `unittest.mock` to:
- Mock user input (`input()` calls)
- Mock print output for verification
- Mock file system operations
- Mock random number generation where needed

## Test Data

Tests use realistic game data:
- Sample weapons with proper stats
- Sample enemies with appropriate HP/attack values
- Sample rooms with various configurations
- Sample player states

## Running Tests During Development

When developing new features:

1. **Write tests first** - Follow Test-Driven Development (TDD)
2. **Run tests frequently** - Use `python run_tests.py` to check your changes
3. **Test edge cases** - Add tests for error conditions and boundary cases
4. **Keep tests focused** - Each test should verify one specific behavior

## Adding New Tests

To add tests for new functionality:

1. Add a new test method to the `TestAdventureGame` class
2. Follow the naming convention: `test_functionality_name`
3. Include setup, execution, and verification steps
4. Use descriptive assertions
5. Mock external dependencies appropriately

Example:
```python
def test_new_feature(self):
    """Test new feature functionality"""
    # Setup
    test_data = {...}
    
    # Execution
    with patch('builtins.print') as mock_print:
        result = new_function(test_data)
    
    # Verification
    self.assertTrue(result)
    mock_print.assert_called_with("Expected output")
```

## Continuous Integration

The test suite is designed to run automatically in CI/CD pipelines:
- All tests are independent and can run in any order
- Tests clean up after themselves
- No external dependencies required
- Clear pass/fail results

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure all game modules are in the same directory
2. **Mock Issues**: Check that mocks are properly configured for the function being tested
3. **State Pollution**: Ensure `setUp()` and `tearDown()` properly reset game state
4. **File System**: Tests use temporary files that are cleaned up automatically

### Debugging Tests

To debug a failing test:
1. Run the specific test: `python run_tests.py test_name`
2. Add debug prints in the test method
3. Check mock configurations
4. Verify test data setup

## Test Quality Guidelines

- **Isolation**: Each test should be independent
- **Clarity**: Test names and assertions should be descriptive
- **Coverage**: Test both success and failure cases
- **Maintainability**: Keep tests simple and focused
- **Performance**: Tests should run quickly

## Future Enhancements

Potential improvements to the test suite:
- Integration tests for full game flow
- Performance benchmarks
- Property-based testing with hypothesis
- Visual regression tests for UI
- Load testing for save/load operations 