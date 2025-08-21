# Adventure Game TODO List

## Completed Tasks ✅

### Bestiary Enhancement
- [x] Modify bestiary to display all enemies when developer mode is enabled
- [x] Show all enemies from constants.enemy_stats and hardcoded special enemies
- [x] Update help text to reflect developer mode bestiary

### Auto-Save Bug Fix
- [x] Fix 'int' object is not iterable error in save_game function
- [x] Add robust type checking for floors_visited, unlocked_floors, and discovered_enemies
- [x] Ensure auto_save_game converts sets to lists before calling save_game
- [x] Add backward compatibility for old save formats

### use_scroll Command Enhancement
- [x] Add waypoint scroll teleportation functionality
- [x] Integrate spell scroll learning with spellbook weapon
- [x] Create menu system for choosing between spell and waypoint scrolls
- [x] Update help text to reflect dual functionality

### Merge use and use_scroll Commands
- [x] Unify use and use_scroll commands into single "use" command
- [x] Integrate potion usage logic from adventure_game.py
- [x] Create unified menu system for scrolls and potions
- [x] Update all help text references from use_scroll to use

### Broken Weapons Enhancement
- [x] Remove pickup restrictions for broken weapons and armor
- [x] Allow players to pick up broken items for repair
- [x] Add informative messages about broken item benefits
- [x] Enhance broken weapon stats: +50% damage, +25% crit chance, +50% crit damage, -25% mana cost
- [x] Update weapon generation to apply stat bonuses when weapons spawn broken
- [x] Add crit_chance and crit_damage properties to all weapons
- [x] Prevent broken weapons from being used in combat (pickup only for repair)

### Crystal System Improvements
- [x] Fix crystal spawning rates: 17.5% for dual crystals, 4.5% for triple crystals
- [x] Remove crystals from normal rooms (crystals only spawn in special crystal rooms)
- [x] Update both world_generation.py and adventure_game.py

## Pending Tasks 🔄

### Repair System Integration
- [x] Integrate broken weapons with repair shop system
- [x] Ensure repair costs scale appropriately with enhanced broken weapon stats
- [x] Add repair success/failure messages
- [x] Restore normal stats when broken weapons are repaired

### Combat System Updates
- [x] Integrate new crit_chance and crit_damage properties into combat calculations
- [x] Update damage display to show critical hit information
- [x] Ensure broken weapons maintain enhanced stats during combat
- [x] Add enhanced critical hit messages for broken weapons

### Testing and Balance
- [x] Test broken weapon pickup and repair flow
- [x] Verify crystal room generation rates
- [x] Test unified use command with all item types
- [x] Ensure save compatibility with new weapon properties

## Summary of Major Accomplishments 🎯

### ✅ **All Major Tasks Completed Successfully!**

The adventure game has been significantly enhanced with:

1. **Unified Command System**: Merged `use` and `use_scroll` into a single, intuitive command
2. **Enhanced Broken Weapons**: Broken weapons have enhanced stats but cannot be used in combat - they must be repaired first
3. **Improved Combat System**: Integrated new crit system with enhanced messages for broken weapons
4. **Fixed Crystal System**: Corrected spawning rates (17.5% dual, 4.5% triple) and removed crystals from normal rooms
5. **Auto-Save Bug Fix**: Resolved critical save/load compatibility issues
6. **Developer Mode Bestiary**: Full enemy list when developer mode is enabled
7. **Repair System Integration**: Broken weapons can be picked up, used with enhanced stats, and repaired to normal

### 🔧 **Technical Improvements Made:**
- Added `crit_chance` and `crit_damage` properties to all weapons
- Enhanced weapon generation with broken weapon stat bonuses
- Updated combat calculations to use weapon-specific crit properties
- Improved inventory display to show broken weapon status and enhanced stats
- Enhanced repair system to restore normal stats when broken weapons are fixed
- Added combat restrictions to prevent broken weapons from being used

## Future Enhancements 🚀

### Advanced Weapon System
- [ ] Add weapon rarity tiers
- [ ] Implement weapon enchantment system
- [ ] Add special weapon abilities

### Crystal System Expansion
- [ ] Add new crystal types (experience, luck, etc.)
- [ ] Implement crystal crafting/combining
- [ ] Add crystal-based quests

### Quality of Life
- [ ] Add item comparison tooltips
- [ ] Implement auto-sort inventory
- [ ] Add item filtering options
