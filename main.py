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
        
        # Movement commands
        elif command in ["north", "south", "east", "west"]:
            success, new_x, new_y = handle_movement(command, current_room, player_floor, player_x, player_y, worlds, learned_spells)
            if success:
                player_x = new_x
                player_y = new_y
        
        # Combat commands
        elif command == "attack":
            if not handle_attack(current_room, inventory, player_mana, equipped_armor, player_hp, 
                               discovered_enemies, mysterious_keys, player_floor, player_money, learned_spells, spells, using_fists):
                break  # Player defeated
        
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
        
        # Add more command handlers here as needed
        else:
            print(f"Command not recognized: '{command}'")
            print("Type 'guide' to see available help sections.")

if __name__ == "__main__":
    main() 