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
    if not developer_mode_enabled:
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
        
        # This would need to be integrated with the main game state
        print(f"Would teleport to Floor {floor} at ({x}, {y})")
        print("Note: This command needs to be integrated with the main game state")
        return True
        
    except ValueError:
        print("Invalid coordinates. Use numbers only.")
        return False

def handle_dev_stats(args):
    """Modify player stats"""
    if not developer_mode_enabled:
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
        
        valid_stats = ['hp', 'max_hp', 'stamina', 'max_stamina', 'mana', 'max_mana', 'money']
        if stat not in valid_stats:
            print(f"Invalid stat. Available: {', '.join(valid_stats)}")
            return False
        
        print(f"Would set {stat} to {value}")
        print("Note: This command needs to be integrated with the main game state")
        return True
        
    except ValueError:
        print("Invalid value. Use numbers only.")
        return False

def handle_dev_weapon(args):
    """Create custom weapon with custom stats"""
    if not developer_mode_enabled:
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
        
        print(f"Would create weapon: {name}")
        print(f"  Damage: {damage}")
        print(f"  Durability: {durability}")
        print("Note: This command needs to be integrated with the main game state")
        return True
        
    except ValueError:
        print("Invalid damage or durability. Use numbers only.")
        return False

def handle_dev_spawn(args):
    """Spawn enemies or items"""
    if not developer_mode_enabled:
        print("Developer mode is not enabled.")
        return False
    
    if len(args) < 2:
        print("Usage: dev_spawn <type> <name>")
        print("Types: enemy, weapon, armor, item")
        print("Example: dev_spawn enemy 'Dragon'")
        return False
    
    spawn_type = args[0].lower()
    name = ' '.join(args[1:])
    
    valid_types = ['enemy', 'weapon', 'armor', 'item']
    if spawn_type not in valid_types:
        print(f"Invalid type. Available: {', '.join(valid_types)}")
        return False
    
    print(f"Would spawn {spawn_type}: {name}")
    print("Note: This command needs to be integrated with the main game state")
    return True

def handle_dev_info(args):
    """Show debug information"""
    if not developer_mode_enabled:
        print("Developer mode is not enabled.")
        return False
    
    print("\n=== DEVELOPER INFO ===")
    print(f"Developer Mode: {'ENABLED' if developer_mode_enabled else 'DISABLED'}")
    print(f"Mod Version: {version}")
    print(f"Author: {author}")
    print("\nAvailable Commands:")
    print("  dev_teleport <floor> <x> <y> - Teleport to location")
    print("  dev_stats <stat> <value> - Modify player stats")
    print("  dev_weapon <name> <damage> <durability> - Create custom weapon")
    print("  dev_spawn <type> <name> - Spawn enemies/items")
    print("  dev_info - Show this information")
    print("  dev_disable - Disable developer mode")
    return True

def handle_dev_disable(args):
    """Disable developer mode"""
    global developer_mode_enabled
    developer_mode_enabled = False
    print("Developer mode DISABLED.")
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
    print("  dev_spawn enemy 'Dragon'  - Spawn a dragon enemy")
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
    developer_mode_enabled = ask_permission()
    return developer_mode_enabled

hooks = {
    "startup": startup_hook
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
    
    # Register guide section using the new system
    guides = {
        "guide": {
            "name": "developer",
            "title": "Developer Tools",
            "description": "Developer tools for testing and debugging",
            "function": show_developer_guide,
            "requires_permission": True
        }
    }
    
    # The mod system will automatically load guides from the guides attribute

# Auto-register when mod is loaded
register_mod()

# Function to check if developer mode is enabled (for external use)
def is_developer_mode_enabled():
    """Check if developer mode is currently enabled"""
    return developer_mode_enabled

# Store command handlers for easy access
admin_commands = {
    "dev_teleport": handle_dev_teleport,
    "dev_stats": handle_dev_stats,
    "dev_weapon": handle_dev_weapon,
    "dev_spawn": handle_dev_spawn,
    "dev_info": handle_dev_info,
    "dev_disable": handle_dev_disable
}
