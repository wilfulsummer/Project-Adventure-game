# Adventure Game Modding Guide

Welcome to the Adventure Game modding system! This guide will teach you how to create mods that add new content to the game without modifying the core files.

## Quick Start

1. **Create a mod folder** in the `mods` directory
2. **Create a `mod.py` file** with your mod content
3. **Add your mod name** to `mods/mods.json` in the `enabled_mods` list
4. **Restart the game** to load your mod

## Mod Structure

```
mods/
├── your_mod_name/
│   ├── mod.py          # Main mod file
│   ├── assets/         # Optional: images, sounds, etc.
│   └── README.md       # Optional: mod documentation
├── mods.json           # Mod configuration
└── README.md           # This file
```

## Basic Mod Template

```python
# Mod metadata
version = "1.0.0"
author = "Your Name"
description = "Description of your mod"

# Import the modding system
from mods.mod_loader import *

# Define your content here
unique_items = {}
enemies = {}
weapons = {}
armors = {}
spells = {}
commands = {}
room_types = {}
hooks = {}

# Register everything
def register_mod():
    # Register your content here
    pass

register_mod()
```

## What You Can Add

### 1. Unique Items
```python
unique_items = {
    "my_sword": {
        "name": "My Awesome Sword",
        "type": "weapon",
        "damage": 20,
        "durability": 80,
        "description": "A powerful weapon",
        "rarity": "unique",
        "spawn_conditions": {
            "floor": 1,
            "min_distance": 75,
            "room_type": "normal"
        }
    }
}
```

### 2. Enemies
```python
enemies = {
    "my_boss": {
        "name": "My Boss",
        "hp": 150,
        "base_attack": 20,
        "is_boss": True,
        "description": "A challenging boss",
        "drops": ["my_sword"]
    }
}
```

### 3. Weapons
```python
weapons = {
    "my_weapon": {
        "name": "My Weapon",
        "damage": 15,
        "durability": 60,
        "description": "A custom weapon"
    }
}
```

### 4. Armor
```python
armors = {
    "my_armor": {
        "name": "My Armor",
        "defense": 8,
        "durability": 70,
        "description": "Custom armor"
    }
}
```

### 5. Spells
```python
spells = {
    "my_spell": {
        "name": "My Spell",
        "damage": 25,
        "mana_cost": 20,
        "description": "A powerful spell"
    }
}
```

### 6. Commands
```python
commands = {
    "mycommand": {
        "name": "mycommand",
        "description": "My custom command",
        "function": "handle_my_command"
    }
}

def handle_my_command(args):
    print("My command was executed!")
    return True
```

### 7. Room Types
```python
room_types = {
    "my_room": {
        "description": "A custom room type",
        "enemy_chance": 0.7,
        "loot_chance": 0.8,
        "special": "my_room_logic"
    }
}
```

### 8. Hooks
```python
def my_combat_hook(player_hp, enemy_hp, damage_dealt):
    """Called during combat"""
    print(f"Player dealt {damage_dealt} damage!")
    return None

def my_room_hook(room_data, player_x, player_y, player_floor):
    """Called when entering a room"""
    if room_data.get("type") == "my_room":
        print("Entering my custom room!")
    return room_data

hooks = {
    "combat": my_combat_hook,
    "room_enter": my_room_hook
}
```

## Registration

All your content must be registered with the mod system:

```python
def register_mod():
    # Register unique items
    for item_id, item_data in unique_items.items():
        register_unique_item(f"your_mod.{item_id}", item_data)
    
    # Register enemies
    for enemy_id, enemy_data in enemies.items():
        register_enemy(f"your_mod.{enemy_id}", enemy_data)
    
    # Register weapons
    for weapon_id, weapon_data in weapons.items():
        register_weapon(f"your_mod.{weapon_id}", weapon_data)
    
    # Register armors
    for armor_id, armor_data in armors.items():
        register_armor(f"your_mod.{armor_id}", armor_data)
    
    # Register spells
    for spell_id, spell_data in spells.items():
        register_spell(f"your_mod.{spell_id}", spell_data)
    
    # Register commands
    for cmd_name, cmd_data in commands.items():
        register_command(f"your_mod.{cmd_name}", cmd_data)
    
    # Register room types
    for room_type, room_data in room_types.items():
        register_room_type(f"your_mod.{room_type}", room_data)
    
    # Register hooks
    for hook_name, hook_func in hooks.items():
        register_hook(f"your_mod.{hook_name}", hook_func)

# Auto-register when mod is loaded
register_mod()
```

## Mod Configuration

Edit `mods/mods.json` to enable/disable mods:

```json
{
    "enabled_mods": [
        "your_mod_name",
        "another_mod"
    ],
    "mod_settings": {
        "auto_reload": false,
        "debug_mode": false
    }
}
```

## Best Practices

1. **Use unique names** - Prefix your content with your mod name to avoid conflicts
2. **Test thoroughly** - Make sure your mod doesn't break the game
3. **Document your mod** - Include a README explaining what your mod does
4. **Version your mods** - Use semantic versioning (1.0.0, 1.1.0, etc.)
5. **Handle errors gracefully** - Don't let mod errors crash the game

## Available Hooks

- `combat` - Called during combat with (player_hp, enemy_hp, damage_dealt)
- `room_enter` - Called when entering a room with (room_data, player_x, player_y, player_floor)
- `item_pickup` - Called when picking up items
- `enemy_defeat` - Called when defeating enemies
- `level_up` - Called when player levels up

## Troubleshooting

- **Mod not loading?** Check that the mod name is in `enabled_mods` in `mods.json`
- **Content not appearing?** Make sure you're calling `register_mod()` at the end of your mod.py
- **Game crashing?** Check the console for error messages from your mod
- **Conflicts?** Make sure your content IDs are unique across all mods

## Example Mods

Check out the `example_mod` folder for a complete working example of a mod.

## Need Help?

If you have questions or need help with modding, check the main game documentation or create an issue in the game's repository.

Happy modding! 🎮
