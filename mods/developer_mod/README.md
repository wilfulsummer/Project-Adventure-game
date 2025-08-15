# Developer Mod

A powerful developer mod for the Adventure Game that provides testing and development tools.

## Features

- **Teleportation** - Move to any location on any floor
- **Stat Manipulation** - Modify player stats for testing
- **Custom Weapons** - Create weapons with custom damage and durability
- **Spawn System** - Spawn enemies, items, and equipment
- **Debug Information** - View mod status and available commands
- **Permission System** - Asks for permission to enable at startup

## Installation

1. The mod is already included in the `mods/developer_mod/` folder
2. It's automatically enabled in `mods/mods.json`
3. The mod will ask for permission to enable when you start the game

## Usage

### Startup
When you start the game, the developer mod will ask:
```
=== DEVELOPER MOD DETECTED ===
This mod provides developer tools for testing and development.
It includes commands for teleportation, stat manipulation, and more.
Enable developer mode? (yes/no):
```

### Commands

All developer commands start with `dev_`:

#### `dev_teleport <floor> <x> <y>`
Teleport to any location in the game world.
```
Example: dev_teleport 3 15 20
```

#### `dev_stats <stat> <value>`
Modify player stats for testing.
```
Available stats: hp, max_hp, stamina, max_stamina, mana, max_mana, money
Example: dev_stats hp 100
```

#### `dev_weapon <name> <damage> <durability>`
Create a custom weapon with specific stats.
```
Example: dev_weapon "Super Sword" 50 200
```

#### `dev_spawn <type> <name>`
Spawn enemies, weapons, armor, or items.
```
Types: enemy, weapon, armor, item
Example: dev_spawn enemy "Dragon"
```

#### `dev_info`
Show developer mod information and available commands.

#### `dev_disable`
Disable developer mode (can be re-enabled by restarting the game).

## Security

- Developer mode must be explicitly enabled at startup
- All commands check if developer mode is enabled
- Commands are isolated from normal gameplay
- Can be disabled at any time with `dev_disable`

## Integration

This mod demonstrates how to:
- Create startup hooks that ask for user input
- Register custom commands with the mod system
- Handle command arguments and validation
- Maintain mod state across game sessions

## Development

The mod is designed to be easily extensible. You can add new commands by:
1. Creating new handler functions
2. Adding them to the `commands` dictionary
3. Adding them to the `admin_commands` dictionary
4. Updating the help text in `dev_info`

## Notes

- This is a development tool - use responsibly
- Commands currently show what they would do but don't actually modify game state
- Full integration requires connecting to the main game systems
- Perfect for testing and debugging during development
