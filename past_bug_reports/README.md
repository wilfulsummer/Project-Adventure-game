# Past Bug Reports

This folder contains bug reports that have been resolved and are no longer active issues.

## Purpose
- Archive resolved bugs for reference
- Track bug fixing history
- Document solutions for future developers
- Keep active bug_reports folder clean

## Current Archive
- `bug_report_20250816_133223.txt` - Set assignment bug (resolved)
  - **Issue**: Trying to use `discovered_enemies[enemy_name] = True` on a set
  - **Solution**: Changed to `discovered_enemies.add(enemy_name)`
  - **Lesson**: Sets use `.add()` method, not dictionary-style assignment

- `bug_report_20250816_135748.txt` - Shop system broken (resolved)
  - **Issue**: `buy` command not recognized despite game instructions to use it
  - **Root Cause**: Missing `buy` command handler in main.py
  - **Solution**: Added complete shop system implementation to main.py
  - **Lesson**: Ensure all referenced commands are actually implemented

- `bug_report_20250818_152151.txt` - Spider swarm display bug (resolved)
  - **Issue**: `'list' object has no attribute 'get'` error in show_room function
  - **Root Cause**: Spider swarms return lists but show_room expected single enemy dictionaries
  - **Solution**: Updated show_room() to handle both single enemies and enemy lists
  - **Lesson**: Data structure consistency is crucial - handle all possible formats

- `bug_report_20250818_145022.txt` - armor_broken NameError (resolved)
  - **Issue**: `name 'armor_broken' is not defined` error in stats command
  - **Root Cause**: Missing `armor_broken` variable in game_state.py
  - **Solution**: Added `armor_broken = 0` to game_state.py statistics section
  - **Lesson**: Ensure all referenced variables are properly declared in game_state.py

- `bug_report_20250818_151925.txt` - AttributeError in enemy handling (resolved)
  - **Issue**: `'list' object has no attribute 'get'` error in show_room function
  - **Root Cause**: UI code trying to call .get() on enemy data that could be list or dict
  - **Solution**: Enhanced enemy data validation with type checking and safety measures
  - **Lesson**: Always validate data types before calling methods on polymorphic structures

- `bug_report_20250821_132649.txt` - EOF Error in main game loop (resolved)
  - **Issue**: `EOF when reading a line` error when input stream is interrupted
  - **Root Cause**: Unprotected input() calls in main game loop and menus
  - **Solution**: Added try-catch blocks for EOFError and KeyboardInterrupt handling
  - **Lesson**: Protect all input() calls in long-running programs with proper exception handling

- `bug_report_20250823_121157.txt` - Shop variable UnboundLocalError (resolved)
  - **Issue**: `local variable 'shop' referenced before assignment` error in show_room function
  - **Root Cause**: Conditional logic error where shop variable accessed outside its scope
  - **Solution**: Fixed nested conditional structure to ensure proper variable scope
  - **Lesson**: Always ensure variables are defined before use, especially in conditional blocks

- `bug_report_gold_tracking.txt` - Missing Gold Tracking from Enemies (resolved)
  - **Issue**: Gold from enemies not being tracked in gold_earned statistic
  - **Root Cause**: handle_attack function missing gold_earned tracking logic
  - **Solution**: Added gold tracking and statistics return system to command handlers
  - **Lesson**: Ensure statistics tracking is maintained across function boundaries when refactoring

- `bug_report_gold_not_updating.txt` - Player Money Not Updating in UI (resolved)
  - **Issue**: Game reports finding gold but player's gold count in status display remains at 0
  - **Root Cause**: player_money not included in updated_stats dictionary returned from handle_attack
  - **Solution**: Added player_money to updated_stats and updated main.py to handle the returned value
  - **Lesson**: When functions modify multiple global variables, ensure ALL modified values are included in return data

- `bug_report_gold_not_updating_ui.txt` - Gold Not Updating in Player Status Display (resolved)
  - **Issue**: Gold earned from enemies not reflected in player status display after combat
  - **Root Cause**: Missing updated_stats['player_money'] updates in multiple locations within handle_attack function
  - **Solution**: Added player_money updates to all gold drop locations and return statements in command_handlers.py
  - **Lesson**: When returning multiple statistics from functions, ensure ALL relevant values are included in the returned data structure

- `bug_report_index_error_pop.txt` - IndexError pop index out of range in Spell Book attacks (resolved)
  - **Issue**: Game crashes with IndexError when using Spell Book weapon to attack enemies
  - **Root Cause**: Variable scope conflict - two 'choice' variables overwriting each other (enemy selection vs spell selection)
  - **Solution**: Renamed spell selection variable from 'choice' to 'spell_choice' to avoid conflicts
  - **Lesson**: Always use unique variable names within the same function scope, especially for user input selections

- `bug_report_double_enemy_death.txt` - Double Enemy Death Bug - Multiple Enemies Dying from Single Attack (resolved)
  - **Issue**: Spider swarms causing multiple enemies to die from one attack with confusing "dies from the effects" message
  - **Root Cause**: Two enemies.pop(choice) calls using same index, causing wrong enemy removal after list indices shifted
  - **Solution**: Changed second pop to use enemies.index(target_enemy) for accurate enemy removal
  - **Lesson**: When removing items from a list being modified, use current item position not cached indices

- `bug_report_persistent_double_death.txt` - Persistent Double Enemy Death Bug - Status Effect Logic Issue (resolved)
  - **Issue**: Double enemy death bug persisted even after fixing the pop() indexing issue
  - **Root Cause**: Combat function continued processing status effects on defeated enemies, creating "ghost enemy" scenarios
  - **Solution**: Added early return after enemy defeat to prevent status effect processing on removed enemies
  - **Lesson**: Sometimes root causes are deeper than initially apparent - trace complete execution flow to identify invalid object references

- `bug_report_index_error_pop_20250826_RESOLVED.txt` - IndexError pop index out of range in handle_attack function (resolved)
  - **Issue**: Game crashes with IndexError: "pop index out of range" when attacking enemies
  - **Root Cause**: Using cached 'choice' variable for enemies.pop() after enemy list modification caused index shifts
  - **Solution**: Replaced enemies.pop(choice) with enemies.index(target_enemy) and proper error handling
  - **Lesson**: When removing items from a modified list, use current item position rather than cached indices
