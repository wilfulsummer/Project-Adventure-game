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
    print("\n=== GAME OVER ===")
    print("Your adventure has ended...")
    
    while True:
        choice = input("\nWould you like to restart? (yes/no): ").lower().strip()
        if choice in ['yes', 'y']:
            print("\nRestarting game...")
            # Reset all game state variables
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
            mysterious_keys = 0
            golden_keys = 0
            unlocked_floors = 1
            waypoints = []
            discovered_enemies = {}
            learned_spells = []
            spell_scrolls = 0
            using_fists = True
            inventory = []
            armor_inventory = []
            equipped_armor = None
            armor_broken = 0
            
            # Auto-save current state before clearing (in case they want to recover)
            try:
                from save_load import auto_save_game
                auto_save_game(worlds, inventory, armor_inventory, equipped_armor, player_floor, player_x, player_y,
                             player_hp, player_max_hp, player_stamina, player_max_stamina, player_mana, player_max_mana,
                             player_money, player_potions, stamina_potions, mana_potions, mysterious_keys, golden_keys,
                             unlocked_floors, waypoints, waypoint_scrolls, discovered_enemies, learned_spells, spell_scrolls, using_fists,
                             player_level, player_xp, player_xp_to_next, enemies_defeated, bosses_defeated, total_damage_dealt,
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
    global player_level, player_xp, player_xp_to_next
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
                             player_level, player_xp, player_xp_to_next, enemies_defeated, bosses_defeated, total_damage_dealt,
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
                     player_level, player_xp, player_xp_to_next, enemies_defeated, bosses_defeated, total_damage_dealt,
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
                    print(f"Leveling progress restored! Level {player_level}")
                
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
                return
            elif section == "movement":
                show_movement_help()
                return
            elif section == "items":
                show_items_help()
                return
            elif section == "resources":
                show_resources_help()
                return
            elif section == "progression":
                show_progression_help()
                return
            elif section == "utility":
                show_utility_help()
                return
            elif section == "developer":
                # Show developer help if developer mod is loaded and enabled
                try:
                    from mods.developer_mod.mod import is_developer_mode_enabled
                    if is_developer_mode_enabled():
                        show_developer_help()
                    else:
                        print("Developer mode is not enabled.")
                        print("Enable developer mode at startup to access developer tools.")
                    return
                except ImportError:
                    print("Developer mod is not loaded.")
                    print("Developer tools are not available.")
                    return
            elif section == "all":
                show_all_help()
                return
            else:
                # Check if this is a mod guide section
                try:
                    from mods.mod_loader import mod_loader
                    mod_guides = mod_loader.get_mod_guides()
                    
                    for guide_id, guide_data in mod_guides.items():
                        try:
                            if guide_data.get('name') == section:
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
                                                return
                                        except ImportError:
                                            print(f"Could not verify permission for '{section}' guide.")
                                            return
                                
                                # Show the guide
                                guide_function = guide_data.get('function')
                                if guide_function and callable(guide_function):
                                    try:
                                        guide_function()
                                        return
                                    except Exception as e:
                                        print(f"Error displaying guide '{section}': {e}")
                                        print("The guide may be corrupted or have invalid content.")
                                        # Generate bug report for the crash
                                        try:
                                            from bug_reporting import manual_bug_report
                                            manual_bug_report(e, f"Guide display: {section}")
                                        except:
                                            pass  # Don't crash the bug reporting system
                                        return
                                else:
                                    print(f"Guide '{section}' is not properly configured.")
                                    return
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
                        pass
                    
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
                                     player_level, player_xp, player_xp_to_next, enemies_defeated, bosses_defeated,
                                     total_damage_dealt, total_damage_taken, critical_hits, attack_count,
                                     rooms_explored, floors_visited, move_count, items_collected, weapons_broken, gold_earned)
                        print("(Auto-saved!)")
                        main.room_count = 0  # Reset counter
                    except Exception as e:
                        print(f"(Auto-save failed: {e})")
                        main.room_count = 0  # Reset counter even on failure
        
        # Combat commands
        elif command == "attack":
            # Use the complete attack logic from adventure_game.py instead of incomplete command_handlers
            attack_count = 0
            critical_hits = 0
            total_damage_dealt = 0
            total_damage_taken = 0
            armor_broken = 0

            if current_room.get("enemy"):
                enemy = current_room["enemy"]
                
                # Check if using fists first
                if using_fists:
                    # Use fists (4 damage, infinite durability) - buffed from 3 to 4
                    damage = 4
                    weapon_name = "fists"
                    
                    # Check for critical hits (fists can crit too!)
                    crit_chance = 0.05  # Base 5% crit chance
                    crit_multiplier = 2.0  # Base 2x damage
                    
                    # Roll for critical hit
                    if random.random() < crit_chance:
                        original_damage = damage
                        damage = int(damage * crit_multiplier)
                        print(f"*** CRITICAL HIT! *** Your fists strike true! {original_damage} → {damage} damage!")
                    else:
                        print(f"You attack the {enemy['name']} with your {weapon_name} for {damage} damage!")
                elif not inventory:
                    # Use fists if no weapons available (4 damage, infinite durability) - buffed from 3 to 4
                    damage = 4
                    weapon_name = "fists"
                    
                    # Check for critical hits (fists can crit too!)
                    crit_chance = 0.05  # Base 5% crit chance
                    crit_multiplier = 2.0  # Base 2x damage
                    
                    # Roll for critical hit
                    if random.random() < crit_chance:
                        original_damage = damage
                        damage = int(damage * crit_multiplier)
                        print(f"*** CRITICAL HIT! *** Your fists strike true! {original_damage} → {damage} damage!")
                    else:
                        print(f"You attack the {enemy['name']} with your {weapon_name} for {damage} damage!")
                else:
                    # Use the first weapon in inventory
                    weapon = inventory[0]
                    weapon_name = weapon["name"]
                    
                    # Special handling for Spell Book
                    if weapon_name == "Spell Book":
                        if not learned_spells:
                            print("You have a Spell Book but don't know any spells!")
                            print("Buy spell scrolls from shops and use 'use_scroll' to learn them.")
                            continue
                        
                        print("Which spell do you want to cast?")
                        for i, spell_name in enumerate(learned_spells, 1):
                            spell = spells[spell_name]
                            print(f"  {i}. {spell_name} - {spell['mana_cost']} mana: {spell['description']}")
                        
                        try:
                            choice = int(input("Enter number: ")) - 1
                            if 0 <= choice < len(learned_spells):
                                spell_name = learned_spells[choice]
                                spell = spells[spell_name]
                                
                                # Check mana
                                if player_mana < spell["mana_cost"]:
                                    print(f"You need {spell['mana_cost']} mana to cast {spell_name}, but you only have {player_mana} mana!")
                                    continue
                                
                                # Cast spell
                                player_mana -= spell["mana_cost"]
                                damage = spell["damage"]
                                
                                print(f"You cast {spell_name} for {damage} damage! (Mana used: {spell['mana_cost']})")
                                
                                # Apply spell effects
                                if spell.get("effect"):
                                    if spell["effect"] in ["Burning", "Poisoned"]:
                                        enemy[spell["effect"]] = {
                                            "damage": spell["effect_damage"],
                                            "duration": spell["effect_duration"]
                                        }
                                        print(f"The {enemy['name']} is {spell['effect']}!")
                                    elif spell["effect"] == "Stunned":
                                        enemy["Stunned"] = spell["effect_duration"]
                                        print(f"The {enemy['name']} is Stunned!")
                            else:
                                print("Invalid choice.")
                                continue
                        except ValueError:
                            print("Please enter a valid number.")
                            continue
                    else:
                        # Regular weapon attack
                        damage = weapon["damage"]
                        
                        # Check if weapon requires mana (staff)
                        if weapon.get("requires_mana"):
                            mana_cost = weapon.get("mana_cost", 10)
                            if player_mana < mana_cost:
                                print(f"You need {mana_cost} mana to use the {weapon_name}, but you only have {player_mana} mana!")
                                print("You can't attack with this weapon.")
                                continue
                            else:
                                player_mana -= mana_cost
                        
                        # Check for critical hits
                        crit_chance = 0.05  # Base 5% crit chance
                        crit_multiplier = 2.0  # Base 2x damage
                        
                        # Daggers get bonus crit chance and damage
                        if weapon_name == "Dagger":
                            crit_chance += 0.075  # +7.5% chance (total 12.5%)
                            crit_multiplier = 2.6  # 2.6x damage
                        
                        # Axes get bonus critical damage (heavier, more powerful hits)
                        elif weapon_name == "Axe":
                            crit_multiplier = 2.8  # 2.8x damage (higher than base 2.0x)
                        
                        # Roll for critical hit
                        if random.random() < crit_chance:
                            original_damage = damage
                            damage = int(damage * crit_multiplier)
                            critical_hits += 1
                            if weapon_name == "Dagger":
                                print(f"*** CRITICAL HIT! *** Your dagger strikes true! {original_damage} → {damage} damage!")
                            elif weapon_name == "Axe":
                                print(f"*** CRITICAL HIT! *** Your axe delivers a devastating blow! {original_damage} → {damage} damage!")
                            else:
                                print(f"*** CRITICAL HIT! *** {original_damage} → {damage} damage!")
                        else:
                            # Normal attack message
                            if weapon.get("requires_mana"):
                                print(f"You attack the {enemy['name']} with your {weapon_name} for {damage} damage! (Mana used: {mana_cost})")
                            else:
                                print(f"You attack the {enemy['name']} with your {weapon_name} for {damage} damage!")
                        
                        # Reduce weapon durability (except for training dummy)
                        if enemy.get("name") != "Training Dummy":
                            weapon["durability"] -= 1
                            if weapon["durability"] <= 0:
                                print(f"Your {weapon_name} breaks!")
                                inventory.remove(weapon)
                                if not inventory:
                                    using_fists = True
                                    print("You're back to using your fists!")
                
                # Apply damage to enemy
                enemy["hp"] -= damage
                total_damage_dealt += damage
                
                # Check if enemy is defeated
                if enemy["hp"] <= 0:
                    print(f"You defeated the {enemy['name']}!")
                    
                    # XP reward for defeating enemies
                    try:
                        from leveling_system import calculate_xp_reward, add_xp_and_level_up
                        
                        # Calculate XP reward based on enemy location and type
                        xp_gained = calculate_xp_reward(enemy["name"], player_x, player_y, player_floor)
                        player_xp += xp_gained
                        print(f"You gained {xp_gained} XP!")
                        
                        # Check for level up
                        new_xp, new_level, new_hp, new_max_hp, levels_gained, new_xp_to_next = add_xp_and_level_up(
                            player_xp, player_level, player_hp, player_max_hp
                        )
                        
                        if levels_gained > 0:
                            player_xp = new_xp
                            player_level = new_level
                            player_hp = new_hp
                            player_max_hp = new_max_hp
                            player_xp_to_next = new_xp_to_next
                            
                            print(f"🎉 LEVEL UP! You are now level {player_level}!")
                            print(f"Health increased! HP: {player_hp}/{player_max_hp}")
                            
                            if player_level >= 100:
                                print("🏆 MAXIMUM LEVEL REACHED! You are a legendary warrior!")
                            else:
                                print(f"XP to next level: {player_xp}/{player_xp_to_next}")
                        else:
                            # Update XP to next level
                            player_xp_to_next = new_xp_to_next
                            
                    except ImportError:
                        print("Leveling system not available.")
                    
                    # Gold reward for defeating enemies
                    if enemy.get("is_boss"):
                        gold_reward = random.randint(15, 25)
                        player_money += gold_reward
                        print(f"Boss defeated! You earned {gold_reward} gold!")
                    else:
                        gold_reward = random.randint(5, 15)
                        player_money += gold_reward
                        print(f"Enemy defeated! You earned {gold_reward} gold!")
                    
                    # Discover enemy for bestiary
                    if enemy["name"] not in discovered_enemies:
                        discovered_enemies.add(enemy["name"])
                        print(f"New enemy discovered: {enemy['name']}!")
                    
                    # Remove enemy from room
                    current_room["enemy"] = None
                    continue
                
                # Enemy attack (unless stunned)
                if enemy.get("Stunned"):
                    print(f"The {enemy['name']} is stunned and can't attack!")
                    enemy["Stunned"] -= 1
                    if enemy["Stunned"] <= 0:
                        del enemy["Stunned"]
                else:
                    enemy_damage = enemy["base_attack"]
                    if equipped_armor:
                        # Balanced flat damage reduction: defense divided by 2 (rounded down)
                        # This makes armor more balanced and less overpowered
                        damage_reduction = equipped_armor["defense"] // 2
                        # Apply armor piercing: enemies can ignore some armor
                        armor_pierce = enemy.get("armor_pierce", 0)
                        effective_reduction = max(0, damage_reduction - armor_pierce)
                        enemy_damage = max(1, enemy_damage - effective_reduction)
                        # Reduce armor durability
                        equipped_armor["durability"] -= 1
                        if equipped_armor["durability"] <= 0:
                            print(f"Your {equipped_armor['name']} breaks!")
                            armor_broken += 1
                            equipped_armor = None
                    
                    player_hp -= enemy_damage
                    total_damage_taken += enemy_damage
                    print(f"The {enemy['name']} attacks you for {enemy_damage} damage!")
                    print(f"You have {player_hp} HP remaining.")
                    
                    if player_hp <= 0:
                        print("You have been defeated!")
                        if handle_player_death():
                            # Player chose to restart, continue with fresh game
                            continue
                        else:
                            # Player chose to exit
                            return
            else:
                print("There's no enemy here to attack.")
        
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
                    print(f"  R. {armor['name']} (Defense: {armor['defense']}, Durability: {armor['durability']}) - 14 gold (1 left)")
                print(f"  P. Health Potion - {shop.get('potion_price', 15)} gold ({shop.get('health_potions', 0)} left)")
                if shop.get("stamina_potions", 0) > 0:
                    print(f"  S. Stamina Potion - {shop.get('stamina_potion_price', 15)} gold ({shop.get('stamina_potions', 0)} left)")
                if shop.get("mana_potions", 0) > 0:
                    print(f"  M. Mana Potion - {shop.get('mana_potion_price', 15)} gold ({shop.get('mana_potions', 0)} left)")
                if shop.get("golden_keys", 0) > 0:
                    print(f"  K. Golden Key - 35 gold ({shop.get('golden_keys', 0)} left)")
                if shop.get("life_crystal"):
                    print("  L. Life Crystal - 21 gold (1 left)")
                if shop.get("stamina_crystal"):
                    print("  T. Stamina Crystal - 21 gold (1 left)")
                if shop.get("mana_crystal"):
                    print("  N. Mana Crystal - 21 gold (1 left)")
                if shop.get("waypoint_scrolls", 0) > 0:
                    print(f"  W. Waypoint Scroll - {shop.get('waypoint_scroll_price', 25)} gold ({shop.get('waypoint_scrolls', 0)} left)")
                
                # Show spell scrolls
                if shop.get("spell_scrolls"):
                    print("Spell Scrolls:")
                    for i, (spell_name, count) in enumerate(shop["spell_scrolls"].items()):
                        price = int(random.randint(40, 80) * 0.7)  # 30% reduction
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
                    if player_money >= 35:  # 30% reduction from 50
                        if golden_keys < 3:
                            player_money -= 35
                            golden_keys += 1
                            shop["golden_keys"] = shop.get("golden_keys", 0) - 1
                            print(f"You bought a golden key! (You now have {golden_keys})")
                        else:
                            print("You can only carry 3 golden keys maximum!")
                    else:
                        print("You don't have enough gold.")
                elif choice.lower() == "l" and shop.get("life_crystal"):
                    if player_money >= 21:  # 30% reduction from 30
                        player_money -= 21
                        player_max_hp += 10
                        player_hp = min(player_hp + 20, player_max_hp)
                        shop["life_crystal"] = False  # Remove the crystal from shop
                        print("You bought and absorbed a life crystal! +10 max HP, +20 current HP")
                    else:
                        print("You don't have enough gold.")
                elif choice.lower() == "t" and shop.get("stamina_crystal"):
                    if player_money >= 21:  # Same price as life crystal
                        player_money -= 21
                        player_max_stamina += 20
                        player_stamina = min(player_stamina + 40, player_max_stamina)
                        shop["stamina_crystal"] = False  # Remove the crystal from shop
                        print("You bought and absorbed a stamina crystal! +20 max stamina, +40 current stamina")
                    else:
                        print("You don't have enough gold.")
                elif choice.lower() == "n" and shop.get("mana_crystal"):
                    if player_money >= 21:  # Same price as life crystal
                        player_money -= 21
                        player_max_mana += 20
                        player_mana = min(player_mana + 40, player_max_mana)
                        shop["mana_crystal"] = False  # Remove the crystal from shop
                        print("You bought and absorbed a mana crystal! +20 max mana, +40 current mana")
                    else:
                        print("You don't have enough gold.")
                elif choice.lower() == "w" and shop.get("waypoint_scrolls", 0) > 0:
                    if player_money >= shop.get("waypoint_scroll_price", 25):
                        player_money -= shop.get("waypoint_scroll_price", 25)
                        waypoint_scrolls += 1
                        shop["waypoint_scrolls"] = shop.get("waypoint_scrolls", 0) - 1
                        print("You bought a waypoint scroll!")
                    else:
                        print("You don't have enough gold.")
                elif choice.lower() == "r" and shop.get("armor"):
                    if player_money >= 14:
                        if len(armor_inventory) < MAX_ARMOR:
                            player_money -= 14
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
                            price = int(random.randint(40, 80) * 0.7)  # 30% reduction
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
        
        # Add more command handlers here as needed
        else:
            print(f"Command not recognized: '{command}'")
            print("Type 'guide' to see available help sections.")

if __name__ == "__main__":
    main() 