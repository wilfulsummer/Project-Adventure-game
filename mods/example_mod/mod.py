"""
Example Mod for Adventure Game
This demonstrates how to create mods for the game.

To use this mod:
1. Copy this folder to the mods directory
2. Add "example_mod" to the enabled_mods list in mods/mods.json
3. Restart the game
"""

# Mod metadata
version = "1.0.0"
author = "Example Modder"
description = "An example mod that adds new content to the game"

# Import the modding system
from mods.mod_loader import *

# Example unique item
unique_items = {
    "example_sword": {
        "name": "Sword of Examples",
        "type": "weapon",
        "damage": 25,
        "durability": 100,
        "description": "A powerful sword created by modding",
        "rarity": "unique",
        "spawn_conditions": {
            "floor": 1,
            "min_distance": 50,
            "room_type": "normal"
        }
    }
}

# Example enemy
enemies = {
    "example_boss": {
        "name": "Example Boss",
        "hp": 200,
        "base_attack": 25,
        "is_boss": True,
        "description": "A boss created by modding",
        "drops": ["example_sword"]
    }
}

# Example weapon
weapons = {
    "example_weapon": {
        "name": "Modded Weapon",
        "damage": 15,
        "durability": 50,
        "description": "A weapon added by a mod"
    }
}

# Example armor
armors = {
    "example_armor": {
        "name": "Modded Armor",
        "defense": 10,
        "durability": 75,
        "description": "Armor added by a mod"
    }
}

# Example spell
spells = {
    "example_spell": {
        "name": "Modded Spell",
        "damage": 30,
        "mana_cost": 25,
        "description": "A powerful spell added by modding"
    }
}

# Example command
commands = {
    "example": {
        "name": "example",
        "description": "Example mod command",
        "function": "handle_example_command"
    }
}

# Example room type
room_types = {
    "example_room": {
        "description": "A mysterious room created by modding",
        "enemy_chance": 0.8,
        "loot_chance": 0.9,
        "special": "example_room_logic"
    }
}

# Example hooks
def example_combat_hook(player_hp, enemy_hp, damage_dealt):
    """Hook called during combat"""
    print(f"Mod hook: Player dealt {damage_dealt} damage!")
    return None

def example_room_hook(room_data, player_x, player_y, player_floor):
    """Hook called when entering a room"""
    if room_data.get("type") == "example_room":
        print("You enter a modded room!")
    return room_data

hooks = {
    "combat": example_combat_hook,
    "room_enter": example_room_hook
}

# Example command handler
def handle_example_command(args):
    """Handle the example command"""
    print("This is an example command from a mod!")
    print("You can add custom commands to the game!")
    return True

# Register everything with the mod system
def register_mod():
    """Register all mod content"""
    # Register unique items
    for item_id, item_data in unique_items.items():
        register_unique_item(f"example_mod.{item_id}", item_data)
    
    # Register enemies
    for enemy_id, enemy_data in enemies.items():
        register_enemy(f"example_mod.{enemy_id}", enemy_data)
    
    # Register weapons
    for weapon_id, weapon_data in weapons.items():
        register_weapon(f"example_mod.{weapon_id}", weapon_data)
    
    # Register armors
    for armor_id, armor_data in armors.items():
        register_armor(f"example_mod.{armor_id}", armor_data)
    
    # Register spells
    for spell_id, spell_data in spells.items():
        register_spell(f"example_mod.{spell_id}", spell_data)
    
    # Register commands
    for cmd_name, cmd_data in commands.items():
        register_command(f"example_mod.{cmd_name}", cmd_data)
    
    # Register room types
    for room_type, room_data in room_types.items():
        register_room_type(f"example_mod.{room_type}", room_data)
    
    # Register hooks
    for hook_name, hook_func in hooks.items():
        register_hook(f"example_mod.{hook_name}", hook_func)

# Auto-register when mod is loaded
register_mod()
