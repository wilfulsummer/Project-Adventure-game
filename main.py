import random
import os
from constants import *
from game_state import *
from world_generation import get_room
from ui_functions import *
from save_load import save_game, load_game
from command_handlers import *

def handle_player_death():
    """Handle player death and restart option"""
    global player_floor, player_x, player_y, player_hp, player_max_hp, player_stamina, player_max_stamina
    global player_mana, player_max_mana, player_money, player_potions, stamina_potions, mana_potions
    global waypoint_scrolls, mysterious_keys, golden_keys, unlocked_floors, waypoints, discovered_enemies
    global learned_spells, spell_scrolls, using_fists, inventory, armor_inventory, equipped_armor, armor_broken
    global player_level, player_xp, player_xp_to_next, player_skill_points, enemies_defeated, bosses_defeated
    global total_damage_dealt, total_damage_taken, critical_hits, attack_count, rooms_explored, floors_visited
    global move_count, items_collected, weapons_broken, gold_earned, discovered_uniques
    
    print("\n=== GAME OVER ===")
    print("Your adventure has ended...")
    
    while True:
        choice = input("\nWould you like to restart? (yes/no): ").lower().strip()
        if choice in ['yes', 'y']:
            print("\nRestarting game...")
            # Reset all game state variables for complete new save
            player_floor = 1
            player_x = 0
            player_y = 0
            player_hp = 50
            player_max_hp = 50
            player_stamina = 100
            player_max_stamina = 100
            player_mana = 50
            player_max_mana = 50
            player_money = 0
            player_potions = 0
            stamina_potions = 0
            mana_potions = 0
            waypoint_scrolls = 0
            mysterious_keys = {}
            golden_keys = 0
            unlocked_floors = set()
            waypoints = {}
            discovered_enemies = set()
            learned_spells = []
            spell_scrolls = {}
            using_fists = True
            inventory = []
            armor_inventory = []
            equipped_armor = None
            armor_broken = 0
            
            # Reset leveling system
            player_level = 1
            player_xp = 0
            player_xp_to_next = 100
            player_skill_points = 0
            
            # Reset all statistics
            enemies_defeated = 0
            bosses_defeated = 0
            total_damage_dealt = 0
            total_damage_taken = 0
            critical_hits = 0
            attack_count = 0
            rooms_explored = 0
            floors_visited = set()
            move_count = 0
            items_collected = 0
            weapons_broken = 0
            gold_earned = 0
            
            # Reset unique items
            discovered_uniques = {}
            
            # Auto-save current state before clearing (in case they want to recover)
            try:
                from save_load import auto_save_game
                auto_save_game(worlds, inventory, armor_inventory, equipped_armor, player_floor, player_x, player_y,
                             player_hp, player_max_hp, player_stamina, player_max_stamina, player_mana, player_max_mana,
                             player_money, player_potions, stamina_potions, mana_potions, mysterious_keys, golden_keys,
                             unlocked_floors, waypoints, waypoint_scrolls, discovered_enemies, learned_spells, spell_scrolls, using_fists,
                             player_level, player_xp, player_xp_to_next, player_skill_points, enemies_defeated, bosses_defeated, total_damage_dealt,
                             total_damage_taken, critical_hits, attack_count, rooms_explored, floors_visited, move_count,
                             items_collected, weapons_broken, gold_earned)
                print("(Auto-saved current state before restart!)")
            except Exception as e:
                print(f"(Auto-save failed: {e})")
            
            # Clear any save files for fresh start
            from save_load import list_save_files, delete_save
            save_files = list_save_files()
            if save_files:
                print("Clearing save files for fresh start...")
                for save_name, _ in save_files:
                    delete_save(save_name)
                print("All save files cleared!")
            
            print("New character created! Starting fresh adventure...")
            print("=" * 50)
            return True  # Return True to indicate restart
        elif choice in ['no', 'n']:
            print("Thanks for playing! Goodbye!")
            return False  # Return False to indicate exit
        else:
            print("Please answer 'yes' or 'no'.")

def main():
    global worlds, player_floor, player_x, player_y, inventory, armor_inventory, equipped_armor
    global player_hp, player_max_hp, player_stamina, player_max_stamina, player_mana, player_max_mana
    global player_money, player_potions, stamina_potions, mana_potions, waypoint_scrolls
    global mysterious_keys, golden_keys, unlocked_floors, waypoints, discovered_enemies
    global learned_spells, spell_scrolls, using_fists
    global attack_count, critical_hits, total_damage_dealt, total_damage_taken, armor_broken
    global discovered_uniques
    global player_level, player_xp, player_xp_to_next, player_skill_points
    global enemies_defeated, bosses_defeated, rooms_explored, floors_visited, move_count
    global items_collected, weapons_broken, gold_earned
    
    # Initialize bug reporting system
    try:
        from bug_reporting import setup_global_exception_handler
        setup_global_exception_handler()
        print("🐛 Bug reporting system initialized")
    except Exception as e:
        print(f"⚠️  Bug reporting system failed to initialize: {e}")
    
    # Initialize unique items system
    from unique_items import load_unique_items
    load_unique_items()
    
    # Initialize mod system
    from mods.mod_loader import mod_loader
    mod_loader.load_mods()
    mod_loader.call_startup_hooks()
    
    print("\n=== ADVENTURE GAME ===")
    print("Welcome to the Adventure Game!")
    print("Type 'guide' to see available info on how to play!")

    # Check for existing saves
    from save_load import list_save_files
    save_files = list_save_files()
    
    if save_files:
        print("\nExisting save files found!")
        for i, (file_name, display_name) in enumerate(save_files, 1):
            print(f"  {i}. {display_name}")
        
        answer = input("\nLoad previous save? (yes/no/delete): ").lower()
        if answer == "yes":
            loaded_data = load_game()
            if loaded_data:
                # Update all global variables
                for key, value in loaded_data.items():
                    globals()[key] = value
                
                # Update unique items system with loaded data
                if "discovered_uniques" in loaded_data:
                    from unique_items import discovered_uniques as ui_discovered_uniques
                    ui_discovered_uniques.clear()
                    ui_discovered_uniques.update(loaded_data["discovered_uniques"])
                    print("Unique items progress restored!")
        elif answer == "delete":
            print("\nSelect save file to delete:")
            for i, (file_name, display_name) in enumerate(save_files, 1):
                print(f"  {i}. {display_name}")
            
            while True:
                try:
                    choice = input(f"Enter number (1-{len(save_files)}) or press Enter to cancel: ").strip()
                    if not choice:
                        print("Delete cancelled.")
                        break
                    elif choice.isdigit():
                        choice_num = int(choice)
                        if 1 <= choice_num <= len(save_files):
                            save_name = save_files[choice_num - 1][0]
                            confirm = input(f"Are you sure you want to delete '{save_name}'? (yes/no): ").lower().strip()
                            if confirm in ['yes', 'y']:
                                from save_load import delete_save
                                delete_save(save_name)
                            break
                        else:
                            print(f"Please enter a number between 1 and {len(save_files)}")
                    else:
                        print("Please enter a valid number or press Enter to cancel.")
                except ValueError:
                    print("Please enter a valid number.")

    while True:
        current_room = get_room(player_floor, player_x, player_y, worlds, learned_spells)
        show_room(current_room, player_floor, player_x, player_y, inventory, player_hp, player_max_hp,
                  player_stamina, player_max_stamina, player_mana, player_max_mana, player_money,
                  player_potions, stamina_potions, mana_potions, waypoint_scrolls, mysterious_keys,
                  golden_keys, equipped_armor, spell_scrolls, learned_spells, discovered_enemies, unlocked_floors,
                  player_level, player_xp, player_xp_to_next)

        command = input("\nWhat do you do? ").lower().strip()
        print("=" * 50)  # Add separator line after command input

        if command == "quit":
            # Auto-save before quitting
            try:
                from save_load import auto_save_game
                auto_save_game(worlds, inventory, armor_inventory, equipped_armor, player_floor, player_x, player_y,
                             player_hp, player_max_hp, player_stamina, player_max_stamina, player_mana, player_max_mana,
                             player_money, player_potions, stamina_potions, mana_potions, mysterious_keys, golden_keys,
                             unlocked_floors, waypoints, waypoint_scrolls, discovered_enemies, learned_spells, spell_scrolls, using_fists,
                             player_level, player_xp, player_xp_to_next, player_skill_points, enemies_defeated, bosses_defeated, total_damage_dealt,
                             total_damage_taken, critical_hits, attack_count, rooms_explored, floors_visited, move_count,
                             items_collected, weapons_broken, gold_earned)
                print("(Auto-saved before exit!)")
            except Exception as e:
                print(f"(Auto-save failed: {e})")
            
            print("Game over!")
            print("Thanks for playing!")
            break

        # Add your command handlers here
        # This is where you'll implement all the game logic
        # For now, just a basic structure
        elif command == "save":
            save_name = input("Enter save name (or press Enter for default): ").strip()
            if not save_name:
                save_name = "default"
            save_game(save_name, worlds, inventory, armor_inventory, equipped_armor, player_floor, player_x, player_y,
                     player_hp, player_max_hp, player_stamina, player_max_stamina, player_mana, player_max_mana,
                     player_money, player_potions, stamina_potions, mana_potions, mysterious_keys, golden_keys,
                     unlocked_floors, waypoints, waypoint_scrolls, discovered_enemies, learned_spells, spell_scrolls, using_fists,
                     player_level, player_xp, player_xp_to_next, player_skill_points, enemies_defeated, bosses_defeated, total_damage_dealt,
                     total_damage_taken, critical_hits, attack_count, rooms_explored, floors_visited, move_count,
                     items_collected, weapons_broken, gold_earned)
        elif command == "load":
            loaded_data = load_game()
            if loaded_data:
                for key, value in loaded_data.items():
                    globals()[key] = value
                
                # Update unique items system with loaded data
                if "discovered_uniques" in loaded_data:
                    from unique_items import discovered_uniques as ui_discovered_uniques
                    ui_discovered_uniques.clear()
                    ui_discovered_uniques.update(loaded_data["discovered_uniques"])
                    print("Unique items progress restored!")
                
                # Update leveling system with loaded data
                if "player_level" in loaded_data:
                    player_level = loaded_data["player_level"]
                    player_xp = loaded_data["player_xp"]
                    player_xp_to_next = loaded_data["player_xp_to_next"]
                    player_skill_points = loaded_data.get("player_skill_points", 0)
                    print(f"Leveling progress restored! Level {player_level}")
                    print(f"Skill points restored: {player_skill_points}")
                
                # Update stats with loaded data
                if "enemies_defeated" in loaded_data:
                    enemies_defeated = loaded_data["enemies_defeated"]
                    bosses_defeated = loaded_data["bosses_defeated"]
                    total_damage_dealt = loaded_data["total_damage_dealt"]
                    total_damage_taken = loaded_data["total_damage_taken"]
                    critical_hits = loaded_data["critical_hits"]
                    attack_count = loaded_data["attack_count"]
                    rooms_explored = loaded_data["rooms_explored"]
                    floors_visited = set(loaded_data.get("floors_visited", []))
                    move_count = loaded_data["move_count"]
                    items_collected = loaded_data["items_collected"]
                    weapons_broken = loaded_data["weapons_broken"]
                    gold_earned = loaded_data["gold_earned"]
                    print("Statistics restored!")
        
        elif command == "saves":
            from save_load import list_save_files, show_save_info
            save_files = list_save_files()
            
            if not save_files:
                print("No save files found.")
            else:
                print("\nAvailable save files:")
                for i, (file_name, display_name) in enumerate(save_files, 1):
                    print(f"  {i}. {display_name}")
                
                while True:
                    choice = input("\nEnter save number to view info, 'all' to show all info, or press Enter to continue: ").strip()
                    
                    if not choice:
                        break
                    elif choice.lower() == "all":
                        for file_name, _ in save_files:
                            show_save_info(file_name)
                        break
                    elif choice.isdigit():
                        choice_num = int(choice)
                        if 1 <= choice_num <= len(save_files):
                            show_save_info(save_files[choice_num - 1][0])
                            break
                        else:
                            print(f"Please enter a number between 1 and {len(save_files)}")
                    else:
                        print("Please enter a valid number, 'all', or press Enter to continue.")
        
        elif command == "delete_save":
            from save_load import list_save_files, delete_save
            save_files = list_save_files()
            
            if not save_files:
                print("No save files found.")
            else:
                print("\nAvailable save files:")
                for i, (file_name, display_name) in enumerate(save_files, 1):
                    print(f"  {i}. {display_name}")
                
                while True:
                    choice = input("\nEnter save number to delete, or press Enter to cancel: ").strip()
                    
                    if not choice:
                        print("Delete cancelled.")
                        break
                    elif choice.isdigit():
                        choice_num = int(choice)
                        if 1 <= choice_num <= len(save_files):
                            save_name = save_files[choice_num - 1][0]
                            confirm = input(f"Are you sure you want to delete '{save_name}'? (yes/no): ").lower().strip()
                            if confirm in ['yes', 'y']:
                                delete_save(save_name)
                            break
                        else:
                            print(f"Please enter a number between 1 and {len(save_files)}")
                    else:
                        print("Please enter a valid number or press Enter to cancel.")
        elif command == "bug_report":
            try:
                from bug_reporting import handle_error_with_report, capture_game_state
                # Create a test error for demonstration
                test_error = Exception("This is a test bug report to demonstrate the system")
                test_traceback = "Traceback (most recent call last):\n  File 'test', line 1, in <module>\n    test_function()\nNameError: name 'test_function' is not defined"
                game_state = capture_game_state()
                
                handle_error_with_report(
                    test_error, Exception, test_error, test_traceback, game_state
                )
                print("\n✅ Test bug report generated successfully!")
                print("💡 This was just a test - no actual error occurred")
            except Exception as e:
                print(f"❌ Failed to generate test bug report: {e}")
        elif command == "guide":
            show_help()
        elif command.startswith("guide "):
            section = command[6:].lower().strip()
            if section == "combat":
                show_combat_help()
            elif section == "movement":
                show_movement_help()
            elif section == "items":
                show_items_help()
            elif section == "resources":
                show_resources_help()
            elif section == "progression":
                show_progression_help()
            elif section == "utility":
                show_utility_help()
            elif section == "developer":
                # Show developer help if developer mod is loaded and enabled
                try:
                    from mods.developer_mod.mod import is_developer_mode_enabled
                    if is_developer_mode_enabled():
                        show_developer_help()
                    else:
                        print("Developer mode is not enabled.")
                        print("Enable developer mode at startup to access developer tools.")
                except ImportError:
                    print("Developer mod is not loaded.")
                    print("Developer tools are not available.")
            elif section == "all":
                show_all_help()
            else:
                # Check if this is a mod guide section
                try:
                    from mods.mod_loader import mod_loader
                    mod_guides = mod_loader.get_mod_guides()
                    
                    guide_found = False
                    for guide_id, guide_data in mod_guides.items():
                        try:
                            if guide_data.get('name') == section:
                                guide_found = True
                                mod_name = guide_id.split('.')[0]
                                
                                # Check if guide requires permission and if it's granted
                                requires_permission = guide_data.get('requires_permission', False)
                                if requires_permission:
                                    if mod_name == "developer_mod":
                                        try:
                                            from mods.developer_mod.mod import is_developer_mode_enabled
                                            if not is_developer_mode_enabled():
                                                print(f"Access to '{section}' guide requires permission.")
                                                print("Enable developer mode to access this guide.")
                                                continue
                                        except ImportError:
                                            print(f"Could not verify permission for '{section}' guide.")
                                            continue
                                
                                # Show the guide
                                guide_function = guide_data.get('function')
                                if guide_function and callable(guide_function):
                                    try:
                                        guide_function()
                                        break  # Found and displayed the guide, exit the loop
                                    except Exception as e:
                                        print(f"Error displaying guide '{section}': {e}")
                                        print("The guide may be corrupted or have invalid content.")
                                        # Generate bug report for the crash
                                        try:
                                            from bug_reporting import manual_bug_report
                                            manual_bug_report(e, f"Guide display: {section}")
                                        except:
                                            pass  # Don't crash the bug reporting system
                                        break  # Exit the loop after error
                                else:
                                    print(f"Guide '{section}' is not properly configured.")
                                    break  # Exit the loop after error
                        except Exception as e:
                            print(f"Warning: Could not process guide '{guide_id}': {e}")
                            # Generate bug report for guide processing errors
                            try:
                                from bug_reporting import manual_bug_report
                                manual_bug_report(e, f"Guide processing: {guide_id}")
                            except:
                                pass  # Don't crash the bug reporting system
                            continue
                    
                    # If we get here, no mod guide was found
                    if not guide_found:
                        print(f"Unknown guide section: '{section}'")
                        available_sections = ["combat", "movement", "items", "resources", "progression", "utility", "all"]
                        
                        # Add mod guide sections
                        try:
                            for guide_id, guide_data in mod_guides.items():
                                try:
                                    guide_name = guide_data.get('name', 'unknown')
                                    if guide_name not in available_sections:
                                        available_sections.insert(-1, guide_name)
                                except Exception as e:
                                    print(f"Warning: Could not process guide '{guide_id}': {e}")
                                    continue
                        except Exception as e:
                            print(f"Warning: Could not load mod guide sections: {e}")
                            # Generate bug report for mod guides loading errors
                            try:
                                from bug_reporting import manual_bug_report
                                manual_bug_report(e, "Mod guides loading")
                            except:
                                pass  # Don't crash the bug reporting system
                        
                        print(f"Available sections: {', '.join(available_sections)}")
                    
                except ImportError:
                    print(f"Unknown guide section: '{section}'")
                    print("Available sections: combat, movement, items, resources, progression, utility, all")
        elif command == "map":
            show_map(player_floor, player_x, player_y, waypoints)
        elif command == "bestiary":
            show_bestiary(discovered_enemies)
        
        elif command == "uniques":
            from unique_items import show_unique_collection
            show_unique_collection()
        
        elif command == "level":
            try:
                from leveling_system import get_level_progress, get_level_bonuses
                
                current_xp, xp_needed, progress = get_level_progress(player_xp, player_level)
                total_hp_bonus, total_max_hp_bonus = get_level_bonuses(player_level)
                
                print(f"\n=== LEVEL STATUS ===")
                print(f"Level: {player_level}/100")
                print(f"XP: {current_xp}/{xp_needed}")
                print(f"Progress: {progress:.1f}%")
                
                if player_level >= 100:
                    print("🏆 MAXIMUM LEVEL REACHED!")
                else:
                    print(f"XP to next level: {xp_needed - current_xp}")
                
                print(f"\nLevel Bonuses:")
                print(f"  +{total_hp_bonus} current HP")
                print(f"  +{total_max_hp_bonus} max HP")
                print(f"  Total HP: {player_hp}/{player_max_hp}")
                print("==================")
                
            except ImportError:
                print("Leveling system not available.")
        
        elif command == "stats":
            print(f"\n=== DETAILED STATISTICS ===")
            print(f"Combat Stats:")
            print(f"  Enemies Defeated: {enemies_defeated}")
            print(f"  Bosses Defeated: {bosses_defeated}")
            print(f"  Total Damage Dealt: {total_damage_dealt}")
            print(f"  Total Damage Taken: {total_damage_taken}")
            print(f"  Critical Hits: {critical_hits}")
            print(f"  Attacks Made: {attack_count}")
            
            print(f"\nExploration Stats:")
            print(f"  Rooms Explored: {rooms_explored}")
            print(f"  Floors Visited: {len(floors_visited)}")
            print(f"  Moves Made: {move_count}")
            
            print(f"\nItem Stats:")
            print(f"  Items Collected: {items_collected}")
            print(f"  Weapons Broken: {weapons_broken}")
            print(f"  Armor Broken: {armor_broken}")
            
            print(f"\nResource Stats:")
            print(f"  Gold Earned: {gold_earned}")
            print(f"  Health Potions Used: {player_potions}")
            print(f"  Stamina Potions Used: {stamina_potions}")
            print(f"  Mana Potions Used: {mana_potions}")
            
            print(f"\nProgression Stats:")
            print(f"  Mysterious Keys Found: {len(mysterious_keys)}")
            print(f"  Golden Keys Found: {golden_keys}")
            print(f"  Waypoints Set: {len(waypoints)}")
            print(f"  Spells Learned: {len(learned_spells)}")
            print(f"  Enemies Discovered: {len(discovered_enemies)}")
            
            print(f"\nCharacter Stats:")
            print(f"  Level: {player_level}/100")
            print(f"  XP: {player_xp}/{player_xp_to_next}")
            print(f"  Skill Points: {player_skill_points}")
            print(f"  HP: {player_hp}/{player_max_hp}")
            print(f"  Stamina: {player_stamina}/{player_max_stamina}")
            print(f"  Mana: {player_mana}/{player_max_mana}")
            print(f"  Gold: {player_money}")
            print("==========================")
        
        elif command == "mods":
            from mods.mod_loader import mod_loader
            loaded_mods = mod_loader.list_mods()
            if loaded_mods:
                print("\n=== LOADED MODS ===")
                for mod_name in loaded_mods:
                    mod_info = mod_loader.get_mod_info(mod_name)
                    if mod_info:
                        print(f"  • {mod_info['name']} v{mod_info['version']} by {mod_info['author']}")
                        print(f"    {mod_info['description']}")
                        print(f"    Content: {mod_info['unique_items']} uniques, {mod_info['enemies']} enemies, {mod_info['weapons']} weapons, {mod_info['armors']} armors, {mod_info['spells']} spells, {mod_info['commands']} commands")
                        print()
                print("===================")
            else:
                print("No mods are currently loaded.")
        
        # Handle mod commands
        elif command.startswith("dev_"):
            from mods.mod_loader import mod_loader
            # Split command into parts
            cmd_parts = command.split()
            cmd_name = cmd_parts[0]
            cmd_args = cmd_parts[1:] if len(cmd_parts) > 1 else []
            
            # Look for the command in loaded mods
            mod_command = None
            for mod_name in mod_loader.list_mods():
                if mod_name == "developer_mod":
                    # Import the developer mod to access its command handlers
                    try:
                        from mods.developer_mod.mod import admin_commands
                        if cmd_name in admin_commands:
                            mod_command = admin_commands[cmd_name]
                            break
                    except ImportError:
                        continue
            
            if mod_command:
                mod_command(cmd_args)
            else:
                print(f"Unknown developer command: {cmd_name}")
                print("Type 'dev_info' for available developer commands.")
        
        # Movement commands
        elif command in ["north", "south", "east", "west"]:
            success, new_x, new_y = handle_movement(command, current_room, player_floor, player_x, player_y, worlds, learned_spells)
            if success:
                player_x = new_x
                player_y = new_y
                
                # Auto-save every 3 rooms moved
                from save_load import auto_save_game
                
                # Increment room counter for auto-save
                if not hasattr(main, 'room_count'):
                    main.room_count = 0
                main.room_count += 1
                
                if main.room_count >= 3:
                    try:
                        auto_save_game(worlds, inventory, armor_inventory, equipped_armor, player_floor, 
                                     new_x, new_y, player_hp, player_max_hp, player_stamina, 
                                     player_max_stamina, player_mana, player_max_mana, player_money, 
                                     player_potions, stamina_potions, mana_potions, mysterious_keys, 
                                     golden_keys, unlocked_floors, waypoints, waypoint_scrolls, 
                                     discovered_enemies, learned_spells, spell_scrolls, using_fists,
                                     player_level, player_xp, player_xp_to_next, player_skill_points, enemies_defeated, bosses_defeated,
                                     total_damage_dealt, total_damage_taken, critical_hits, attack_count,
                                     rooms_explored, floors_visited, move_count, items_collected, weapons_broken, gold_earned)
                        print("(Auto-saved!)")
                        main.room_count = 0  # Reset counter
                    except Exception as e:
                        print(f"(Auto-save failed: {e})")
                        main.room_count = 0  # Reset counter even on failure
        
        # Combat commands
        elif command == "attack":
            # Use the proper handle_attack function that handles multiple enemies correctly
            success = handle_attack(current_room, inventory, player_mana, equipped_armor, player_hp, 
                                  discovered_enemies, mysterious_keys, player_floor, player_money, learned_spells, spells, using_fists,
                                  attack_count, critical_hits, total_damage_dealt, total_damage_taken, 
                                  enemies_defeated, bosses_defeated, weapons_broken, armor_broken)
            
            if not success:
                # Player was defeated
                handle_player_death()
                break
        
        elif command == "run":
            player_stamina, player_x, player_y = handle_run(current_room, player_stamina, player_x, player_y)
        
        # Inventory commands
        elif command == "take":
            handle_take(current_room, inventory, armor_inventory, MAX_WEAPONS, MAX_ARMOR, mysterious_keys, golden_keys)
        
        elif command == "equipment":
            handle_equipment(inventory, armor_inventory, equipped_armor, using_fists)
        
        elif command == "drop":
            handle_drop(inventory, armor_inventory, equipped_armor, current_room)
        
        elif command == "equip":
            success, new_equipped_armor = handle_equip(armor_inventory)
            if success and new_equipped_armor:
                equipped_armor = new_equipped_armor
        
        elif command == "switch":
            success, new_using_fists = handle_switch(inventory)
            if success:
                using_fists = new_using_fists
        
        # Resource commands
        elif command == "consume":
            player_max_hp, player_hp, player_stamina, player_max_mana, player_mana = handle_consume(
                current_room, player_max_hp, player_hp, player_stamina, player_max_stamina, 
                player_mana, player_max_mana, player_potions, stamina_potions, mana_potions)
        
        elif command == "buy":
            if current_room.get("type") == "shop" and current_room.get("shop"):
                shop = current_room["shop"]
                
                # Check if shop has any items
                has_items = (len(shop.get("items", [])) > 0 or 
                           shop.get("armor") or 
                           shop.get("has_key") or 
                           shop.get("life_crystal") or 
                           shop.get("stamina_potions", 0) > 0 or 
                           shop.get("mana_potions", 0) > 0 or 
                           shop.get("waypoint_scrolls", 0) > 0)
                
                if not has_items:
                    print("The shop is empty and closed.")
                    continue
                
                print("\nShop inventory:")
                for i, item in enumerate(shop.get("items", [])):
                    print(f"  {i+1}. {item['name']} (Damage: {item['damage']}, Durability: {item['durability']}) - {item['cost']} gold (1 left)")
                if shop.get("armor"):
                    armor = shop["armor"]
                    armor_price = 14 if not shop.get("is_discount_shop") else int(14 * shop.get("spell_scroll_discount", 1.0))
                    print(f"  R. {armor['name']} (Defense: {armor['defense']}, Durability: {armor['durability']}) - {armor_price} gold (1 left)")
                print(f"  P. Health Potion - {shop.get('potion_price', 15)} gold ({shop.get('health_potions', 0)} left)")
                if shop.get("stamina_potions", 0) > 0:
                    print(f"  S. Stamina Potion - {shop.get('stamina_potion_price', 15)} gold ({shop.get('stamina_potions', 0)} left)")
                if shop.get("mana_potions", 0) > 0:
                    print(f"  M. Mana Potion - {shop.get('mana_potion_price', 15)} gold ({shop.get('mana_potions', 0)} left)")
                if shop.get("golden_keys", 0) > 0:
                    key_price = 35 if not shop.get("is_discount_shop") else int(35 * shop.get("spell_scroll_discount", 1.0))
                    print(f"  K. Golden Key - {key_price} gold ({shop.get('golden_keys', 0)} left)")
                if shop.get("life_crystal"):
                    crystal_price = 21 if not shop.get("is_discount_shop") else int(21 * shop.get("spell_scroll_discount", 1.0))
                    print(f"  L. Life Crystal - {crystal_price} gold (1 left)")
                if shop.get("stamina_crystal"):
                    crystal_price = 21 if not shop.get("is_discount_shop") else int(21 * shop.get("spell_scroll_discount", 1.0))
                    print(f"  T. Stamina Crystal - {crystal_price} gold (1 left)")
                if shop.get("mana_crystal"):
                    crystal_price = 21 if not shop.get("is_discount_shop") else int(21 * shop.get("spell_scroll_discount", 1.0))
                    print(f"  N. Mana Crystal - {crystal_price} gold (1 left)")
                if shop.get("waypoint_scrolls", 0) > 0:
                    waypoint_price = shop.get('waypoint_scroll_price', 25)
                    print(f"  W. Waypoint Scroll - {waypoint_price} gold ({shop.get('waypoint_scrolls', 0)} left)")
                
                # Show spell scrolls
                if shop.get("spell_scrolls"):
                    print("Spell Scrolls:")
                    for i, (spell_name, count) in enumerate(shop["spell_scrolls"].items()):
                        price = shop.get("spell_scroll_prices", {}).get(spell_name, 40)
                        print(f"  {chr(65 + i)}. {spell_name} Scroll - {price} gold ({count} left)")
                
                choice = input("What would you like to buy? (or 'cancel'): ").strip()
                
                if choice == "cancel":
                    print("You leave the shop.")
                elif choice.lower() == "p":
                    if shop.get("health_potions", 0) > 0:
                        if player_money >= shop.get("potion_price", 15):
                            player_money -= shop.get("potion_price", 15)
                            player_potions += 1
                            shop["health_potions"] = shop.get("health_potions", 0) - 1
                            print("You bought a health potion!")
                        else:
                            print("You don't have enough gold.")
                    else:
                        print("No health potions available.")
                elif choice.lower() == "s" and shop.get("stamina_potions", 0) > 0:
                    if player_money >= shop.get("stamina_potion_price", 15):
                        player_money -= shop.get("stamina_potion_price", 15)
                        stamina_potions += 1
                        shop["stamina_potions"] = shop.get("stamina_potions", 0) - 1
                        print("You bought a stamina potion!")
                    else:
                        print("You don't have enough gold.")
                elif choice.lower() == "m" and shop.get("mana_potions", 0) > 0:
                    if player_money >= shop.get("mana_potion_price", 15):
                        player_money -= shop.get("mana_potion_price", 15)
                        mana_potions += 1
                        shop["mana_potions"] = shop.get("mana_potions", 0) - 1
                        print("You bought a mana potion!")
                    else:
                        print("You don't have enough gold.")
                elif choice.lower() == "k" and shop.get("golden_keys", 0) > 0:
                    key_price = 35 if not shop.get("is_discount_shop") else int(35 * shop.get("spell_scroll_discount", 1.0))
                    if player_money >= key_price:
                        if golden_keys < 3:
                            player_money -= key_price
                            golden_keys += 1
                            shop["golden_keys"] = shop.get("golden_keys", 0) - 1
                            print(f"You bought a golden key! (You now have {golden_keys})")
                        else:
                            print("You can only carry 3 golden keys maximum!")
                    else:
                        print("You don't have enough gold.")
                elif choice.lower() == "l" and shop.get("life_crystal"):
                    crystal_price = 21 if not shop.get("is_discount_shop") else int(21 * shop.get("spell_scroll_discount", 1.0))
                    if player_money >= crystal_price:
                        player_money -= crystal_price
                        player_max_hp += 10
                        player_hp = min(player_hp + 20, player_max_hp)
                        shop["life_crystal"] = False  # Remove the crystal from shop
                        print("You bought and absorbed a life crystal! +10 max HP, +20 current HP")
                    else:
                        print("You don't have enough gold.")
                elif choice.lower() == "t" and shop.get("stamina_crystal"):
                    crystal_price = 21 if not shop.get("is_discount_shop") else int(21 * shop.get("spell_scroll_discount", 1.0))
                    if player_money >= crystal_price:
                        player_money -= crystal_price
                        player_max_stamina += 20
                        player_stamina = min(player_stamina + 40, player_max_stamina)
                        shop["stamina_crystal"] = False  # Remove the crystal from shop
                        print("You bought and absorbed a stamina crystal! +20 max stamina, +40 current stamina")
                    else:
                        print("You don't have enough gold.")
                elif choice.lower() == "n" and shop.get("mana_crystal"):
                    crystal_price = 21 if not shop.get("is_discount_shop") else int(21 * shop.get("spell_scroll_discount", 1.0))
                    if player_money >= crystal_price:
                        player_money -= crystal_price
                        player_max_mana += 20
                        player_mana = min(player_mana + 40, player_max_mana)
                        shop["mana_crystal"] = False  # Remove the crystal from shop
                        print("You bought and absorbed a mana crystal! +20 max mana, +40 current mana")
                    else:
                        print("You don't have enough gold.")
                elif choice.lower() == "w" and shop.get("waypoint_scrolls", 0) > 0:
                    waypoint_price = shop.get("waypoint_scroll_price", 25)
                    if player_money >= waypoint_price:
                        player_money -= waypoint_price
                        waypoint_scrolls += 1
                        shop["waypoint_scrolls"] = shop.get("waypoint_scrolls", 0) - 1
                        print("You bought a waypoint scroll!")
                    else:
                        print("You don't have enough gold.")
                elif choice.lower() == "r" and shop.get("armor"):
                    armor_price = 14 if not shop.get("is_discount_shop") else int(14 * shop.get("spell_scroll_discount", 1.0))
                    if player_money >= armor_price:
                        if len(armor_inventory) < MAX_ARMOR:
                            player_money -= armor_price
                            armor_inventory.append(shop["armor"])
                            shop["armor"] = None  # Remove armor from shop
                            print(f"You bought the {armor_inventory[-1]['name']}!")
                        else:
                            print("Your armor inventory is full! Drop some armor first.")
                    else:
                        print("You don't have enough gold.")
                elif choice.isdigit():
                    choice_num = int(choice) - 1
                    if 0 <= choice_num < len(shop.get("items", [])):
                        item = shop["items"][choice_num]
                        if player_money >= item["cost"]:
                            if len(inventory) < MAX_WEAPONS:
                                player_money -= item["cost"]
                                inventory.append(item)
                                shop["items"].pop(choice_num)  # Remove item from shop
                                print(f"You bought the {item['name']}!")
                            else:
                                print("Your weapon inventory is full! Drop a weapon first.")
                        else:
                            print("You don't have enough gold.")
                    else:
                        print("Invalid choice.")
                elif choice.isalpha() and len(choice) == 1:
                    # Handle spell scrolls
                    scroll_index = ord(choice.upper()) - ord('A')
                    if shop.get("spell_scrolls") and 0 <= scroll_index < len(shop["spell_scrolls"]):
                        spell_name = list(shop["spell_scrolls"].keys())[scroll_index]
                        count = shop["spell_scrolls"][spell_name]
                        if count > 0:
                            price = shop.get("spell_scroll_prices", {}).get(spell_name, 40)
                            if player_money >= price:
                                player_money -= price
                                if spell_name not in spell_scrolls:
                                    spell_scrolls[spell_name] = 0
                                spell_scrolls[spell_name] += 1
                                shop["spell_scrolls"][spell_name] -= 1
                                print(f"You bought a {spell_name} scroll!")
                            else:
                                print("You don't have enough gold.")
                        else:
                            print("No more of that scroll available.")
                    else:
                        print("Invalid choice.")
                else:
                    print("Invalid choice.")
            else:
                print("There's no shop here.")
        
        elif command.startswith("waypoint"):
            command_parts = command.split()
            waypoints, waypoint_scrolls = handle_waypoint(command_parts, waypoints, waypoint_scrolls, player_floor, player_x, player_y)
        
        # Shop commands
        elif command in ["repair", "Repair"]:
            success, new_player_money = handle_repair(current_room, inventory, armor_inventory, player_money)
            if success:
                player_money = new_player_money
        
        # Descend command - go down stairwells to new floors
        elif command == "descend":
            if current_room.get("type") == "stairwell" and current_room.get("requires_mysterious_key"):
                if player_floor in mysterious_keys or player_floor in unlocked_floors:
                    # Use mysterious key if player has one for this floor
                    if player_floor in mysterious_keys:
                        del mysterious_keys[player_floor]
                        unlocked_floors.add(player_floor)
                        print(f"You use your mysterious key for Floor {player_floor} to unlock the stairwell!")
                        print("The key dissolves into the lock, permanently unlocking this floor's stairwells.")
                        
                        # Remove any mysterious keys from this floor's rooms since they're no longer useful
                        if player_floor in worlds:
                            for room in worlds[player_floor].values():
                                if room.get("mysterious_key"):
                                    room["mysterious_key"] = None
                    
                    # Descend to next floor
                    player_floor += 1
                    player_x = 0
                    player_y = 0
                    print(f"You descend to Floor {player_floor}!")
                else:
                    print(f"You need a mysterious key for Floor {player_floor} to unlock this stairwell!")
            else:
                print("There's no stairwell here to descend.")
        
        # Use command - handle spell scrolls, waypoint scrolls, and potions
        elif command == "use" or command == "use_scroll":
            # Check what types of items the player has
            has_spell_scrolls = bool(spell_scrolls)
            has_waypoint_scrolls = waypoint_scrolls > 0
            has_potions = player_potions > 0 or stamina_potions > 0 or mana_potions > 0
            
            if not has_spell_scrolls and not has_waypoint_scrolls and not has_potions:
                print("You don't have any scrolls or potions to use.")
                return
            
            print("What would you like to use?")
            
            if has_spell_scrolls:
                print("  1. Spell Scroll - Learn a new spell")
            
            if has_waypoint_scrolls:
                print(f"  2. Waypoint Scroll - Teleport to a waypoint ({waypoint_scrolls} available)")
            
            if has_potions:
                print("  3. Potion - Use health, stamina, or mana potions")
            
            try:
                choice = input("Enter your choice: ").strip()
                
                if choice == "1" and has_spell_scrolls:
                    # Handle spell scrolls
                    print("\nWhich spell scroll do you want to use?")
                    for i, (spell_name, count) in enumerate(spell_scrolls.items(), 1):
                        print(f"  {i}. {spell_name} Scroll ({count} available)")
                    
                    spell_choice = input("Enter spell number: ").strip()
                    if spell_choice.isdigit():
                        spell_choice_num = int(spell_choice) - 1
                        spell_list = list(spell_scrolls.items())
                        if 0 <= spell_choice_num < len(spell_list):
                            spell_name, count = spell_list[spell_choice_num]
                            if spell_name in learned_spells:
                                print(f"You already know the {spell_name} spell!")
                            else:
                                learned_spells.append(spell_name)
                                spell_scrolls[spell_name] -= 1
                                if spell_scrolls[spell_name] <= 0:
                                    del spell_scrolls[spell_name]
                                print(f"You learned the {spell_name} spell!")
                                print(f"Description: {spells[spell_name]['description']}")
                        else:
                            print("Invalid spell choice.")
                    else:
                        print("Please enter a valid number.")
                
                elif choice == "2" and has_waypoint_scrolls:
                    # Handle waypoint scrolls
                    if not waypoints:
                        print("You don't have any waypoints set to teleport to!")
                        print("Use 'waypoint add <name>' to create a waypoint first.")
                    else:
                        print("\nAvailable waypoints:")
                        for i, (name, (floor, x, y)) in enumerate(waypoints.items(), 1):
                            print(f"  {i}. {name}: Floor {floor} ({x}, {y})")
                        
                        waypoint_choice = input("Enter waypoint number to teleport to: ").strip()
                        if waypoint_choice.isdigit():
                            waypoint_choice_num = int(waypoint_choice) - 1
                            waypoint_list = list(waypoints.items())
                            if 0 <= waypoint_choice_num < len(waypoint_list):
                                name, (floor, x, y) = waypoint_list[waypoint_choice_num]
                                waypoint_scrolls -= 1
                                player_floor = floor
                                player_x = x
                                player_y = y
                                print(f"You use a waypoint scroll to teleport to '{name}'!")
                                print(f"You are now at Floor {player_floor} ({player_x}, {player_y})")
                                print(f"Waypoint scrolls remaining: {waypoint_scrolls}")
                            else:
                                print("Invalid waypoint choice.")
                        else:
                            print("Please enter a valid number.")
                
                elif choice == "3" and has_potions:
                    # Handle potions
                    available_potions = []
                    if player_potions > 0:
                        available_potions.append(("health", player_potions))
                    if stamina_potions > 0:
                        available_potions.append(("stamina", stamina_potions))
                    if mana_potions > 0:
                        available_potions.append(("mana", mana_potions))
                    
                    if len(available_potions) == 1:
                        # Only one type of potion, use it automatically
                        potion_type, count = available_potions[0]
                        if potion_type == "health":
                            heal_amount = 30
                            old_hp = player_hp
                            player_hp = min(player_hp + heal_amount, player_max_hp)
                            player_potions -= 1
                            actual_heal = player_hp - old_hp
                            print(f"You use a health potion and recover {actual_heal} HP!")
                            print(f"You now have {player_hp}/{player_max_hp} HP and {player_potions} health potions remaining.")
                        elif potion_type == "stamina":
                            old_stamina = player_stamina
                            player_stamina = min(player_stamina + 10, player_max_stamina)
                            stamina_potions -= 1
                            actual_regen = player_stamina - old_stamina
                            print(f"You use a stamina potion and recover {actual_regen} stamina!")
                            print(f"You now have {player_stamina}/{player_max_stamina} stamina and {stamina_potions} stamina potions remaining.")
                        else:  # mana
                            old_mana = player_mana
                            player_mana = min(player_mana + 15, player_max_mana)
                            mana_potions -= 1
                            actual_regen = player_mana - old_mana
                            print(f"You use a mana potion and recover {actual_regen} mana!")
                            print(f"You now have {player_mana}/{player_max_mana} mana and {mana_potions} mana potions remaining.")
                    else:
                        # Multiple potion types, let player choose
                        print("Which potion do you want to use?")
                        for i, (potion_type, count) in enumerate(available_potions, 1):
                            if potion_type == "health":
                                print(f"  {i}. Health Potion ({count} available)")
                            elif potion_type == "stamina":
                                print(f"  {i}. Stamina Potion ({count} available)")
                            else:  # mana
                                print(f"  {i}. Mana Potion ({count} available)")
                        
                        try:
                            potion_choice = int(input("Enter number: ")) - 1
                            if 0 <= potion_choice < len(available_potions):
                                potion_type, count = available_potions[potion_choice]
                                if potion_type == "health":
                                    heal_amount = 30
                                    old_hp = player_hp
                                    player_hp = min(player_hp + heal_amount, player_max_hp)
                                    player_potions -= 1
                                    actual_heal = player_hp - old_hp
                                    print(f"You use a health potion and recover {actual_heal} HP!")
                                    print(f"You now have {player_hp}/{player_max_hp} HP and {player_potions} health potions remaining.")
                                elif potion_type == "stamina":
                                    old_stamina = player_stamina
                                    player_stamina = min(player_stamina + 10, player_max_stamina)
                                    stamina_potions -= 1
                                    actual_regen = player_stamina - old_stamina
                                    print(f"You use a stamina potion and recover {actual_regen} stamina!")
                                    print(f"You now have {player_stamina}/{player_max_stamina} stamina and {stamina_potions} stamina potions remaining.")
                                else:  # mana
                                    old_mana = player_mana
                                    player_mana = min(player_mana + 15, player_max_mana)
                                    mana_potions -= 1
                                    actual_regen = player_mana - old_mana
                                    print(f"You use a mana potion and recover {actual_regen} mana!")
                                    print(f"You now have {player_mana}/{player_max_mana} mana and {mana_potions} mana potions remaining.")
                            else:
                                print("Invalid choice.")
                        except ValueError:
                            print("Please enter a valid number.")
                
                else:
                    print("Invalid choice. Please enter 1, 2, or 3.")
                    
            except Exception as e:
                print(f"Error using item: {e}")
        
        # Take key command - pick up mysterious keys
        elif command == "take_key":
            if current_room.get("mysterious_key"):
                key = current_room["mysterious_key"]
                if player_floor in mysterious_keys or player_floor in unlocked_floors:
                    print(f"You already have a mysterious key for Floor {player_floor} or this floor is already unlocked!")
                    print("Maybe you should use it instead of picking up another one.")
                else:
                    mysterious_keys[player_floor] = True
                    current_room["mysterious_key"] = None
                    print(f"You picked up the {key['name']}!")
            else:
                print("There's no mysterious key here to take.")
        
        # Loot command - open treasure chambers with golden keys
        elif command == "loot":
            if current_room.get("type") == "key_door" and not current_room.get("enemy") and not current_room.get("treasure_looted"):
                if golden_keys <= 0:
                    print("You need a golden key to access the treasure chamber!")
                    print("You can buy one from shops for 35 gold.")
                else:
                    # Boss room treasure rewards
                    gold_reward = 60
                    potion_reward = random.randint(2, 4)
                    
                    player_money += gold_reward
                    player_potions += potion_reward
                    
                    print(f"You use your golden key to unlock the treasure chamber!")
                    print(f"Found {gold_reward} gold!")
                    print(f"Found {potion_reward} health potions!")
                    
                    # Add Troll Hide armor to treasure room
                    if len(armor_inventory) < MAX_ARMOR:
                        from world_generation import create_troll_hide_armor
                        troll_hide = create_troll_hide_armor(player_x, player_y)
                        armor_inventory.append(troll_hide)
                        print(f"Found {troll_hide['name']} (Defense: {troll_hide['defense']}, Durability: {troll_hide['durability']})!")
                    else:
                        # Store Troll Hide in the room for later pickup
                        from world_generation import create_troll_hide_armor
                        troll_hide = create_troll_hide_armor(player_x, player_y)
                        if "armors" not in current_room:
                            current_room["armors"] = []
                        current_room["armors"].append(troll_hide)
                        print("Your armor inventory is full! The Troll Hide was left behind.")
                        print("You can pick it up later by dropping some armor first.")
                    
                    if player_floor not in mysterious_keys:
                        mysterious_keys[player_floor] = True
                        print(f"Found a mysterious key for Floor {player_floor}!")
                    else:
                        print(f"Found a mysterious key for Floor {player_floor}, but you already have one!")
                    
                    golden_keys -= 1  # Golden key is consumed
                    current_room["treasure_looted"] = True
                    print("The treasure chamber has been emptied.")
            else:
                print("There's nothing to loot here.")
        
        # Open command - open chests
        elif command == "open":
            if current_room.get("chest"):
                chest = current_room["chest"]
                if chest.get("locked", False):
                    if golden_keys <= 0:
                        print("This chest is locked! You need a golden key to open it.")
                        print("You can buy golden keys from shops for 35 gold.")
                    else:
                        golden_keys -= 1
                        chest["locked"] = False
                        print("You use a golden key to unlock the chest!")
                        
                        # Add weapons to room
                        if chest.get("weapons"):
                            if "weapons" not in current_room:
                                current_room["weapons"] = []
                            current_room["weapons"].extend(chest["weapons"])
                            print(f"Found {len(chest['weapons'])} weapons in the chest!")
                        
                        # Add armor to room
                        if chest.get("armor"):
                            if "armors" not in current_room:
                                current_room["armors"] = []
                            current_room["armors"].append(chest["armor"])
                            print(f"Found {chest['armor']['name']} in the chest!")
                        
                        # Add potions
                        if chest.get("potions", 0) > 0:
                            player_potions += chest["potions"]
                            print(f"Found {chest['potions']} health potions in the chest!")
                        
                        # Add life crystal
                        if chest.get("life_crystal", False):
                            player_max_hp += 10
                            player_hp = min(player_hp + 20, player_max_hp)
                            print("Found a life crystal in the chest! +10 max HP, +20 current HP")
                        
                        # Mark chest as opened
                        chest["opened"] = True
                        print("The chest has been opened and looted.")
                else:
                    print("This chest is already unlocked. Use 'take' to collect the items.")
            else:
                print("There's no chest here to open.")
        
        # Waypoint command - manage waypoints
        elif command.startswith("waypoint"):
            command_parts = command.split()
            if len(command_parts) == 1:
                # Show waypoint help
                print("Waypoint commands:")
                print("  waypoint add <name> - Add a waypoint at current location")
                print("  waypoint view - Show all waypoints")
                print("  waypoint delete <name> - Delete a waypoint")
                print("  waypoint teleport <name> - Teleport to a waypoint (costs 1 scroll)")
            elif command_parts[1] == "add" and len(command_parts) == 3:
                name = command_parts[2]
                if len(waypoints) >= 10:
                    print("You can only have 10 waypoints maximum!")
                elif name in waypoints:
                    print(f"A waypoint named '{name}' already exists!")
                else:
                    waypoints[name] = (player_floor, player_x, player_y)
                    print(f"Waypoint '{name}' added at Floor {player_floor} ({player_x}, {player_y})")
            elif command_parts[1] == "view":
                if not waypoints:
                    print("You don't have any waypoints set.")
                else:
                    print("Your waypoints:")
                    for name, (floor, x, y) in waypoints.items():
                        print(f"  {name}: Floor {floor} ({x}, {y})")
            elif command_parts[1] == "delete" and len(command_parts) == 3:
                name = command_parts[2]
                if name in waypoints:
                    del waypoints[name]
                    print(f"Waypoint '{name}' deleted.")
                else:
                    print(f"No waypoint named '{name}' found.")
            elif command_parts[1] == "teleport" and len(command_parts) == 3:
                name = command_parts[2]
                if name not in waypoints:
                    print(f"No waypoint named '{name}' found.")
                elif waypoint_scrolls <= 0:
                    print("You need a waypoint scroll to teleport!")
                else:
                    floor, x, y = waypoints[name]
                    waypoint_scrolls -= 1
                    player_floor = floor
                    player_x = x
                    player_y = y
                    print(f"You teleport to waypoint '{name}'!")
                    print(f"You are now at Floor {player_floor} ({player_x}, {player_y})")
                    print(f"Waypoint scrolls remaining: {waypoint_scrolls}")
            else:
                print("Invalid waypoint command. Use 'waypoint' for help.")
        
        # Drop mysterious key command
        elif command == "drop_mysterious_key":
            if player_floor in mysterious_keys:
                confirm = input("Are you sure you want to drop your mysterious key? (yes/no): ").lower().strip()
                if confirm == "yes":
                    print("Maybe you should use it instead of dropping it...")
                    confirm2 = input("Really drop it? (yes/no): ").lower().strip()
                    if confirm2 == "yes":
                        del mysterious_keys[player_floor]
                        current_room["mysterious_key"] = {
                            "floor": player_floor,
                            "name": f"Mysterious Key (Floor {player_floor})"
                        }
                        print(f"You dropped your mysterious key for Floor {player_floor}.")
                    else:
                        print("You decide to keep your mysterious key.")
                else:
                    print("You decide to keep your mysterious key.")
            else:
                print("You don't have a mysterious key to drop.")
        
        # Add more command handlers here as needed
        else:
            print(f"Command not recognized: '{command}'")
            print("Type 'guide' to see available help sections.")

if __name__ == "__main__":
    main() 