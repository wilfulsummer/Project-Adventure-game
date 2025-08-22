# Adventure Game Mod Installation Guide

## Quick Start
1. **Extract the game folder** anywhere on your computer
2. **Run `Adventure Game.exe`** to play
3. **Mods are already included** and ready to use!

## What's Included
- **Adventure Game.exe** - The main game executable
- **mods/** folder - Contains all available mods
- **saves/** folder - Your save games (auto-created)
- **README.md** - Game information
- **LICENSE** - Game license

## Mod System Features
- **File-based mods** - No Python coding required!
- **Automatic loading** - Mods load when you start the game
- **Easy management** - Enable/disable mods by editing `mods.json`
- **Hot-reloading** - Some mods update without restarting

## Available Mods

### Developer Mod (ENABLED by default)
- **Purpose**: Testing and development tools
- **Commands**: `dev_teleport`, `dev_stats`, `dev_weapon`, `dev_spawn`
- **Access**: Type `dev_info` in game for full command list
- **Security**: Asks for permission at startup

### Example Mod (DISABLED by default)
- **Purpose**: Shows how to create mods
- **Content**: Sample weapons, enemies, and items
- **Enable**: Add "example_mod" to `mods.json`

## Installing New Mods

### Method 1: Simple Copy & Paste
1. **Download a mod folder** (e.g., `my_awesome_mod`)
2. **Copy it to the `mods/` folder**
3. **Edit `mods.json`** to add the mod name
4. **Restart the game**

### Method 2: Using the Mod Manager
1. **Type `mods` in game** to see current status
2. **Check the mods folder** for available mods
3. **Edit `mods.json`** to enable desired mods

## Mod Configuration

### Editing mods.json
```json
{
    "enabled_mods": [
        "developer_mod",
        "example_mod",
        "my_new_mod"
    ],
    "mod_settings": {
        "auto_reload": false,
        "debug_mode": false
    }
}
```

### Mod Settings Explained
- **enabled_mods**: List of mod names to load
- **auto_reload**: Automatically reload mods when files change
- **debug_mode**: Show detailed mod loading information

## Creating Your Own Mods

### Basic Mod Structure
```
mods/my_mod/
├── mod.py              # Main mod file (required)
├── guide.txt           # Help text (optional)
├── guides/             # Multiple help sections (optional)
│   ├── weapons.txt
│   └── enemies.txt
├── weapons/            # Custom weapons (optional)
│   └── my_sword.txt
└── README.md           # Mod documentation (optional)
```

### Simple Weapon Mod
Create `mods/my_mod/weapons/awesome_sword.txt`:
```
Awesome Sword
damage: 50
durability: 200
crit_chance: 0.25
crit_damage: 3.0
mana_cost: 0
description: The most awesome sword ever!
```

### Simple Guide Mod
Create `mods/my_mod/guide.txt`:
```
my_mod
Welcome to my awesome mod!

This mod adds:
• Cool new weapons
• Amazing enemies
• Fun gameplay mechanics

Type 'guide my_mod' to see this help again!
```

## Troubleshooting

### Mods Not Loading?
1. **Check `mods.json`** - Ensure mod names are correct
2. **Verify folder structure** - Mods must be in `mods/mod_name/`
3. **Check for errors** - Look for error messages when starting
4. **Restart the game** - Mods only load at startup

### Game Crashes with Mods?
1. **Disable all mods** - Set `enabled_mods: []` in `mods.json`
2. **Test one mod at a time** - Enable mods individually
3. **Check mod compatibility** - Some mods may conflict
4. **Report the issue** - Include error messages and mod list

### Mod Commands Not Working?
1. **Check if mod is enabled** - Use `mods` command
2. **Verify command syntax** - Check mod documentation
3. **Check permissions** - Some mods require special access
4. **Restart the game** - Commands register at startup

## Advanced Features

### Mod Dependencies
Some mods require other mods to work:
```json
{
    "enabled_mods": [
        "base_mod",      # Required first
        "expansion_mod"  # Depends on base_mod
    ]
}
```

### Custom Commands
Mods can add new game commands:
- **Movement commands** - Custom travel methods
- **Combat commands** - Special attack types
- **Utility commands** - Helper functions
- **Admin commands** - Developer tools

### Hooks and Events
Mods can respond to game events:
- **Combat hooks** - Custom damage calculations
- **Room hooks** - Special room behaviors
- **Item hooks** - Custom item effects
- **Startup hooks** - Initialization code

## Support and Community

### Getting Help
1. **Check this guide** - Most issues are covered here
2. **Use in-game help** - Type `guide` for game help
3. **Check mod documentation** - Each mod has its own guide
4. **Report bugs** - Include mod list and error messages

### Contributing
1. **Create mods** - Share your creations with others
2. **Improve existing mods** - Submit enhancements
3. **Document mods** - Write clear installation guides
4. **Test mods** - Help find and fix bugs

## File Locations

### Game Files
- **Executable**: `Adventure Game.exe`
- **Mods**: `mods/` folder
- **Saves**: `saves/` folder
- **Configuration**: `mods/mods.json`

### Mod Files
- **Python code**: `mods/mod_name/mod.py`
- **Text guides**: `mods/mod_name/guide.txt`
- **Weapon data**: `mods/mod_name/weapons/`
- **Documentation**: `mods/mod_name/README.md`

## Security Notes

### Safe Modding
- **Only download mods** from trusted sources
- **Check mod code** before installing
- **Backup saves** before testing new mods
- **Report suspicious mods** to the community

### Developer Mode
- **Developer mod** provides testing tools
- **Use responsibly** - Can affect game balance
- **Disable in production** - Use `dev_disable` command
- **Requires permission** - Asks at startup

---

**Happy Modding!** 🎮✨

The mod system is designed to be simple yet powerful. Start with the included mods, then create your own!
