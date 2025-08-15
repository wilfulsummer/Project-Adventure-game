import random
import os
from constants import *
from game_state import *
from world_generation import get_room
from ui_functions import *
from save_load import save_game, load_game
from command_handlers import *

def main():
    global worlds, player_floor, player_x, player_y, inventory, armor_inventory, equipped_armor
    global player_hp, player_max_hp, player_stamina, player_max_stamina, player_mana, player_max_mana
    global player_money, player_potions, stamina_potions, mana_potions, waypoint_scrolls
    global mysterious_keys, golden_keys, unlocked_floors, waypoints, discovered_enemies
    global learned_spells, spell_scrolls, using_fists
    global attack_count, critical_hits, total_damage_dealt, total_damage_taken, armor_broken
    global discovered_uniques
    
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

    if os.path.exists(SAVE_FILE):
        answer = input("Load previous save? (yes/no/delete): ").lower()
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
            confirm = input("Are you sure you want to delete the save file? (yes/no): ").lower()
            if confirm == "yes":
                os.remove(SAVE_FILE)
                print("Save file deleted!")
            else:
                print("Save file deletion cancelled.")

    while True:
        current_room = get_room(player_floor, player_x, player_y, worlds, learned_spells)
        show_room(current_room, player_floor, player_x, player_y, inventory, player_hp, player_max_hp,
                  player_stamina, player_max_stamina, player_mana, player_max_mana, player_money,
                  player_potions, stamina_potions, mana_potions, waypoint_scrolls, mysterious_keys,
                  golden_keys, equipped_armor, spell_scrolls, learned_spells, discovered_enemies, unlocked_floors)

        command = input("\nWhat do you do? ").lower().strip()

        if command == "quit":
            print("Game over!")
            break

        # Add your command handlers here
        # This is where you'll implement all the game logic
        # For now, just a basic structure
        elif command == "save":
            save_game(worlds, inventory, armor_inventory, equipped_armor, player_floor, player_x, player_y,
                     player_hp, player_max_hp, player_stamina, player_max_stamina, player_mana, player_max_mana,
                     player_money, player_potions, stamina_potions, mana_potions, mysterious_keys, golden_keys,
                     unlocked_floors, waypoints, waypoint_scrolls, discovered_enemies, learned_spells, spell_scrolls, using_fists)
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
            elif section == "all":
                show_all_help()
            else:
                print(f"Unknown guide section: '{section}'")
                print("Available sections: combat, movement, items, resources, progression, utility, all")
        elif command == "map":
            show_map(player_floor, player_x, player_y, waypoints)
        elif command == "bestiary":
            show_bestiary(discovered_enemies)
        
        elif command == "uniques":
            from unique_items import show_unique_collection
            show_unique_collection()
        
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
                            crit_chance += 0.15  # +15% chance (total 20%)
                            crit_multiplier = 2.6  # 2.6x damage
                        
                        # Roll for critical hit
                        if random.random() < crit_chance:
                            original_damage = damage
                            damage = int(damage * crit_multiplier)
                            critical_hits += 1
                            if weapon_name == "Dagger":
                                print(f"*** CRITICAL HIT! *** Your dagger strikes true! {original_damage} → {damage} damage!")
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
                        discovered_enemies[enemy["name"]] = True
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
                        break
            else:
                print("There's no enemy here to attack.")
        
        elif command == "run":
            player_stamina, player_x, player_y = handle_run(current_room, player_stamina, player_x, player_y)
        
        # Inventory commands
        elif command == "take":
            handle_take(current_room, inventory, armor_inventory, MAX_WEAPONS, MAX_ARMOR)
        
        elif command == "inventory":
            handle_inventory(inventory, using_fists)
        
        elif command == "armor":
            handle_armor(armor_inventory, equipped_armor)
        
        elif command == "drop":
            handle_drop(inventory, current_room)
        
        elif command == "drop_armor":
            handle_drop_armor(armor_inventory, equipped_armor, current_room)
        
        elif command == "equip":
            success, new_equipped_armor = handle_equip(armor_inventory)
            if success and new_equipped_armor:
                equipped_armor = new_equipped_armor
        
        elif command == "switch":
            success, new_using_fists = handle_switch(inventory)
            if success:
                using_fists = new_using_fists
        
        # Resource commands
        elif command == "absorb":
            player_max_hp, player_hp, player_stamina, player_max_mana, player_mana = handle_absorb(
                current_room, player_max_hp, player_hp, player_stamina, player_max_stamina, 
                player_mana, player_max_mana)
        
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