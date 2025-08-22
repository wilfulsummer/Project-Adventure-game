"""
Developer Mod for Adventure Game
This mod provides developer tools for testing and development.

Features:
- Teleport to any location on any floor
- Modify player stats
- Create custom stat weapons
- Spawn enemies and items
- Debug information
- Admin commands

The mod asks for permission to enable at startup.
"""

# Mod metadata
version = "1.0.0"
author = "Game Developer"
description = "Developer tools for testing and development"
requires_permission = True

# Import the modding system
from mods.mod_loader import *

# Developer mod state
developer_mode_enabled = False
admin_commands = {}

# Store state in the mod loader instead of files
def save_developer_state(enabled):
    """Save developer mode state to mod loader"""
    try:
        # Store the state in the mod loader's data
        from mods.mod_loader import mod_loader
        if "developer_state" not in mod_loader.mod_data:
            mod_loader.mod_data["developer_state"] = {}
        mod_loader.mod_data["developer_state"]["developer_mode_enabled"] = enabled
        return True
    except Exception as e:
        print(f"Warning: Could not save developer state: {e}")
        return False

def load_developer_state():
    """Load developer mode state from mod loader"""
    try:
        from mods.mod_loader import mod_loader
        if "developer_state" in mod_loader.mod_data:
            return mod_loader.mod_data["developer_state"].get("developer_mode_enabled", False)
        return False
    except Exception as e:
        print(f"Warning: Could not load developer state: {e}")
        return False

# Initialize state from mod loader
developer_mode_enabled = load_developer_state()

def ask_permission():
    """Ask user if they want to enable developer mode"""
    print("\n=== DEVELOPER MOD DETECTED ===")
    print("This mod provides developer tools for testing and development.")
    print("It includes commands for teleportation, stat manipulation, and more.")
    
    while True:
        response = input("Enable developer mode? (yes/no): ").lower().strip()
        if response in ['yes', 'y']:
            print("Developer mode ENABLED!")
            return True
        elif response in ['no', 'n']:
            print("Developer mode DISABLED.")
            return False
        else:
            print("Please answer 'yes' or 'no'.")

# Developer commands
def handle_dev_teleport(args):
    """Teleport to any location"""
    if not is_developer_mode_enabled():
        print("Developer mode is not enabled.")
        return False
    
    if len(args) < 3:
        print("Usage: dev_teleport <floor> <x> <y>")
        print("Example: dev_teleport 3 15 20")
        return False
    
    try:
        floor = int(args[0])
        x = int(args[1])
        y = int(args[2])
        
        # Import and modify game state
        import game_state
        game_state.player_floor = floor
        game_state.player_x = x
        game_state.player_y = y
        
        print(f"[DEV] Teleported to Floor {floor} at ({x}, {y})")
        print("Developer teleportation successful!")
        return True
        
    except ValueError:
        print("Invalid coordinates. Use numbers only.")
        return False

def handle_dev_stats(args):
    """Modify player stats"""
    if not is_developer_mode_enabled():
        print("Developer mode is not enabled.")
        return False
    
    if len(args) < 2:
        print("Usage: dev_stats <stat> <value>")
        print("Available stats: hp, max_hp, stamina, max_stamina, mana, max_mana, money")
        print("Example: dev_stats hp 100")
        return False
    
    stat = args[0].lower()
    try:
        value = int(args[1])
        
        # Import game state
        import game_state
        
        # Map stat names to game state variables
        stat_mapping = {
            'hp': 'player_hp',
            'max_hp': 'player_max_hp', 
            'stamina': 'player_stamina',
            'max_stamina': 'player_max_stamina',
            'mana': 'player_mana',
            'max_mana': 'player_max_mana',
            'money': 'player_money'
        }
        
        if stat not in stat_mapping:
            print(f"Invalid stat. Available: {', '.join(stat_mapping.keys())}")
            return False
        
        # Get old value
        old_value = getattr(game_state, stat_mapping[stat])
        
        # Set new value
        setattr(game_state, stat_mapping[stat], value)
        
        print(f"[DEV] Changed {stat} from {old_value} to {value}")
        print("Developer stat modification successful!")
        return True
        
    except ValueError:
        print("Invalid value. Use numbers only.")
        return False

def handle_dev_weapon(args):
    """Create custom weapon with custom stats"""
    if not is_developer_mode_enabled():
        print("Developer mode is not enabled.")
        return False
    
    if len(args) < 3:
        print("Usage: dev_weapon <name> <damage> <durability>")
        print("Example: dev_weapon 'Super Sword' 50 200")
        return False
    
    try:
        name = args[0]
        damage = int(args[1])
        durability = int(args[2])
        
        if damage < 0 or durability < 0:
            print("Damage and durability must be positive numbers.")
            return False
        
        # Import game state
        import game_state
        from constants import MAX_WEAPONS
        
        # Check if inventory is full
        if len(game_state.inventory) >= MAX_WEAPONS:
            print(f"Cannot create weapon: inventory is full ({len(game_state.inventory)}/{MAX_WEAPONS})")
            print("Drop a weapon first using 'drop' command")
            return False
        
        # Create custom weapon
        custom_weapon = {
            "name": name,
            "damage": damage,
            "durability": durability
        }
        
        # Add to inventory
        game_state.inventory.append(custom_weapon)
        game_state.using_fists = False  # Switch to using weapons
        
        print(f"[DEV] Created weapon: {name}")
        print(f"  Damage: {damage}")
        print(f"  Durability: {durability}")
        print("Developer weapon creation successful!")
        return True
        
    except ValueError:
        print("Invalid damage or durability. Use numbers only.")
        return False

def handle_dev_spawn(args):
    """Spawn enemies or items"""
    if not is_developer_mode_enabled():
        print("Developer mode is not enabled.")
        return False
    
    if len(args) < 2:
        print("Usage: dev_spawn <type> <name>")
        print("Types: enemy, weapon, armor")
        print("Example: dev_spawn enemy 'Baby Dragon'")
        return False
    
    spawn_type = args[0].lower()
    name = ' '.join(args[1:])
    
    valid_types = ['enemy', 'weapon', 'armor']
    if spawn_type not in valid_types:
        print(f"Invalid type. Available: {', '.join(valid_types)}")
        return False
    
    # Import game state
    import game_state
    from world_generation import get_room
    
    # Get current room
    current_room = get_room(game_state.player_floor, game_state.player_x, game_state.player_y, game_state.worlds, game_state.learned_spells)
    
    if spawn_type == "enemy":
        # Create a custom enemy
        custom_enemy = {
            "name": name,
            "hp": 50,
            "base_attack": 10,
            "armor_pierce": 0
        }
        
        # Add enemy to current room
        current_room["enemy"] = custom_enemy
        print(f"[DEV] Spawned enemy: {name}")
        print(f"  HP: {custom_enemy['hp']}")
        print(f"  Attack: {custom_enemy['base_attack']}")
        
    elif spawn_type == "weapon":
        # Create a basic weapon and add it to the room
        custom_weapon = {
            "name": name,
            "damage": 15,
            "durability": 50
        }
        
        if "weapons" not in current_room:
            current_room["weapons"] = []
        current_room["weapons"].append(custom_weapon)
        print(f"[DEV] Spawned weapon: {name}")
        print(f"  Damage: {custom_weapon['damage']}")
        print(f"  Durability: {custom_weapon['durability']}")
        
    elif spawn_type == "armor":
        # Create basic armor and add it to the room
        custom_armor = {
            "name": name,
            "defense": 5,
            "durability": 30
        }
        
        if "armors" not in current_room:
            current_room["armors"] = []
        current_room["armors"].append(custom_armor)
        print(f"[DEV] Spawned armor: {name}")
        print(f"  Defense: {custom_armor['defense']}")
        print(f"  Durability: {custom_armor['durability']}")
    
    print("Developer spawn successful!")
    return True

def handle_dev_info(args):
    """Show debug information"""
    if not is_developer_mode_enabled():
        print("Developer mode is not enabled.")
        return False
    
    # Import game state to show current info
    import game_state
    
    print("\n=== DEVELOPER INFO ===")
    print(f"Developer Mode: {'ENABLED' if is_developer_mode_enabled() else 'DISABLED'}")
    print(f"Mod Version: {version}")
    print(f"Author: {author}")
    
    print("\n=== CURRENT GAME STATE ===")
    print(f"Player Position: Floor {game_state.player_floor} at ({game_state.player_x}, {game_state.player_y})")
    print(f"Player Stats: HP {game_state.player_hp}/{game_state.player_max_hp}, Stamina {game_state.player_stamina}/{game_state.player_max_stamina}, Mana {game_state.player_mana}/{game_state.player_max_mana}")
    print(f"Money: {game_state.player_money}")
    print(f"Weapons: {len(game_state.inventory)} items")
    print(f"Armor: {len(game_state.armor_inventory)} pieces")
    
    print("\nAvailable Commands:")
    print("  dev_teleport <floor> <x> <y> - Teleport to location")
    print("  dev_stats <stat> <value> - Modify player stats")
    print("  dev_weapon <name> <damage> <durability> - Create custom weapon")
    print("  dev_spawn <type> <name> - Spawn enemies/items")
    print("  dev_info - Show this information")
    print("  dev_disable - Disable developer mode")
    print("=============================")
    return True

def handle_dev_disable(args):
    """Disable developer mode"""
    save_developer_state(False)
    print("Developer mode DISABLED.")
    print("Developer commands are no longer available.")
    return True

def handle_dev_reload(args):
    """Reload a specific mod"""
    if not is_developer_mode_enabled():
        print("Developer mode is not enabled.")
        return False
    
    if len(args) < 1:
        print("Usage: dev_reload <mod_name>")
        print("Example: dev_reload example_mod")
        return False
    
    mod_name = args[0]
    
    # Import mod loader and reload the mod
    from mods.mod_loader import mod_loader
    mod_loader.reload_specific_mod(mod_name)
    return True

def handle_dev_auto_reload(args):
    """Auto-reload all changed mods"""
    if not is_developer_mode_enabled():
        print("Developer mode is not enabled.")
        return False
    
    # Import mod loader and auto-reload changed mods
    from mods.mod_loader import mod_loader
    mod_loader.auto_reload_changed_mods()
    return True

# Register commands
commands = {
    "dev_teleport": {
        "name": "dev_teleport",
        "description": "Teleport to any location (Developer only)",
        "function": "handle_dev_teleport"
    },
    "dev_stats": {
        "name": "dev_stats", 
        "description": "Modify player stats (Developer only)",
        "function": "handle_dev_stats"
    },
    "dev_weapon": {
        "name": "dev_weapon",
        "description": "Create custom weapon (Developer only)", 
        "function": "handle_dev_weapon"
    },
    "dev_spawn": {
        "name": "dev_spawn",
        "description": "Spawn enemies/items (Developer only)",
        "function": "handle_dev_spawn"
    },
    "dev_info": {
        "name": "dev_info",
        "description": "Show developer information (Developer only)",
        "function": "handle_dev_info"
    },
    "dev_disable": {
        "name": "dev_disable",
        "description": "Disable developer mode (Developer only)",
        "function": "handle_dev_disable"
    },
    "dev_reload": {
        "name": "dev_reload",
        "description": "Reload a specific mod (Developer only)",
        "function": "handle_dev_reload"
    },
    "dev_auto_reload": {
        "name": "dev_auto_reload",
        "description": "Auto-reload all changed mods (Developer only)",
        "function": "handle_dev_auto_reload"
    }
}

# Guide section for the mod
def show_developer_guide():
    """Display developer tools guide section"""
    print("\n=== DEVELOPER TOOLS GUIDE ===")
    print("WARNING: These are developer tools for testing and debugging!")
    print("WARNING: Use responsibly and only in development environments!")
    print("\nCommands:")
    print("  dev_info - Show developer mod information and status")
    print("  dev_teleport <floor> <x> <y> - Teleport to any location")
    print("  dev_stats <stat> <value> - Modify player stats")
    print("  dev_weapon <name> <damage> <durability> - Create custom weapon")
    print("  dev_spawn <type> <name> - Spawn enemies, items, or equipment")
    print("  dev_disable - Disable developer mode")
    print("\nUsage Examples:")
    print("  dev_teleport 3 15 20     - Move to Floor 3, coordinates (15,20)")
    print("  dev_stats hp 100          - Set current HP to 100")
    print("  dev_stats max_hp 200      - Set maximum HP to 200")
    print("  dev_weapon 'Super Sword' 50 200 - Create weapon with 50 damage, 200 durability")
    print("  dev_spawn enemy 'Baby Dragon'  - Spawn a baby dragon enemy")
    print("  dev_spawn weapon 'Laser'  - Spawn a laser weapon")
    print("\nAvailable Stats:")
    print("  hp, max_hp, stamina, max_stamina, mana, max_mana, money")
    print("\nSpawn Types:")
    print("  enemy, weapon, armor, item")
    print("\nSecurity:")
    print("  - Developer mode must be enabled at startup")
    print("  - All commands check if developer mode is active")
    print("  - Can be disabled anytime with 'dev_disable'")
    print("  - Commands are isolated from normal gameplay")
    print("==================")

# Hooks for startup permission
def startup_hook():
    """Hook called at game startup to ask for permission"""
    global developer_mode_enabled
    result = ask_permission()
    developer_mode_enabled = result
    # Save the state to file so it persists across imports
    save_developer_state(result)
    print(f"Startup hook: Developer mode set to {developer_mode_enabled}")
    return developer_mode_enabled

hooks = {
    "startup": startup_hook
}

# Register guide section at module level so it can be found by mod loader
guides = {
    "guide": {
        "name": "developer",
        "title": "Developer Tools",
        "description": "Developer tools for testing and debugging",
        "function": show_developer_guide,
        "requires_permission": True
    }
}

# Register everything with the mod system
def register_mod():
    """Register all mod content"""
    # Register commands
    for cmd_name, cmd_data in commands.items():
        register_command(f"developer_mod.{cmd_name}", cmd_data)
    
    # Register hooks
    for hook_name, hook_func in hooks.items():
        register_hook(f"developer_mod.{hook_name}", hook_func)
    
    # Guide is registered at module level above

# Auto-register when mod is loaded
register_mod()

# Function to check if developer mode is enabled (for external use)
def is_developer_mode_enabled():
    """Check if developer mode is currently enabled"""
    # Always check the current file state to ensure consistency
    return load_developer_state()

# Store command handlers for easy access
admin_commands = {
    "dev_teleport": handle_dev_teleport,
    "dev_stats": handle_dev_stats,
    "dev_weapon": handle_dev_weapon,
    "dev_spawn": handle_dev_spawn,
    "dev_info": handle_dev_info,
    "dev_disable": handle_dev_disable,
    "dev_reload": handle_dev_reload,
    "dev_auto_reload": handle_dev_auto_reload
}
