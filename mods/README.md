# Adventure Game Modding System

This system allows modders to extend the game without modifying core files.

## What Modders Can Add

- **Unique Items** - Special items with custom properties
- **Enemies** - New creatures to fight
- **Weapons & Armor** - New equipment with custom stats
- **Spells** - New magical abilities
- **Commands** - New game commands
- **Room Types** - New room layouts and behaviors
- **Hooks** - Custom game event handlers
- **Guide Sections** - Helpful information for players

## Weapon System - CUSTOM STATS! ⚔️

Easily add weapons with custom critical hit chances, damage multipliers, and mana costs!

### Weapon File Format

Create weapon files in your mod's `weapons/` directory:

```
Weapon Name
damage: 25
durability: 100
crit_chance: 0.15
crit_damage: 2.5
mana_cost: 0
description: Your weapon description here
```

### Weapon Stats Explained

- **damage** - Base damage dealt (required)
- **durability** - How many hits before breaking (required)
- **crit_chance** - Critical hit probability (0.0 to 1.0, default 0.05 = 5%)
- **crit_damage** - Critical hit multiplier (default 2.0 = 2x damage)
- **mana_cost** - Mana consumed per attack (0 = no mana, default 0)
- **description** - Weapon description (optional)

### Example Weapons

**High Crit Weapon:**
```
Lucky Dagger
damage: 18
durability: 80
crit_chance: 0.25
crit_damage: 3.0
mana_cost: 0
description: A dagger with extremely high critical hit chance and damage
```

**Mana Weapon:**
```
Magic Staff
damage: 35
durability: 200
crit_chance: 0.08
crit_damage: 2.2
mana_cost: 20
description: A powerful staff that consumes mana but deals massive damage
```

**Balanced Weapon:**
```
Custom Sword
damage: 22
durability: 120
crit_chance: 0.12
crit_damage: 2.3
mana_cost: 0
description: A custom sword with enhanced critical hit capabilities
```

### How It Works

1. **Create weapons/ directory** in your mod folder
2. **Add .txt files** with weapon stats
3. **Game automatically loads** all weapons
4. **Weapons appear** in the world naturally
5. **Custom stats work** automatically in combat

**That's it!** No Python coding required - just create text files and the game handles the rest!

## Guide System - SUPER EASY MOD GUIDES! 📚

The easiest way to add guide sections is using **text files** - no Python coding required!

### Simple Guide Format

Create a `guide.txt` file in your mod directory with this format:

```
GUIDE_ENTRY_NAME
Your guide content goes here
Lots of text
Whatever you want to write
```

**Example:**
```
example_mod
Welcome to my awesome mod!

NEW FEATURES:
• Cool new weapons
• Amazing enemies
• Fun gameplay mechanics

HOW TO USE:
• Just play normally
• New content appears automatically
• Use 'guide example_mod' to see this help
```

### Multiple Guide Sections

Create a `guides/` subdirectory with multiple `.txt` files:

```
mods/my_mod/
├── mod.py
├── guide.txt              # Main guide (accessible via 'guide example_mod')
└── guides/
    ├── weapons.txt        # Weapons guide (accessible via 'guide weapons')
    ├── enemies.txt        # Enemies guide (accessible via 'guide enemies')
    └── tips.txt          # Tips guide (accessible via 'guide tips')
```

### How It Works

1. **First line** = Guide entry name (what players type after 'guide')
2. **Everything below** = Content that gets printed when the guide is accessed
3. **Game automatically** loads and registers your guides
4. **Players access** them with `guide GUIDE_ENTRY_NAME`

### Accessing Mod Guides

Players can access your guides using:
- `guide example_mod` - Shows your main guide
- `guide weapons` - Shows weapons guide (if you have guides/weapons.txt)
- `guide enemies` - Shows enemies guide (if you have guides/enemies.txt)

**That's it!** No Python coding, no complex setup - just create text files and the game does the rest!

## Traditional Guide System (Python)

You can also create guides using Python code in your `mod.py`:

```python
def show_my_guide():
    print("=== MY MOD GUIDE ===")
    print("This is a custom guide function!")
    print("==================")

guides = {
    "guide": {
        "name": "mymod",
        "title": "My Mod Guide",
        "description": "Guide for my awesome mod",
        "function": show_my_guide,
        "requires_permission": False
    }
}
```

## Mod Structure

```
mods/your_mod/
├── mod.py              # Main mod file (required)
├── guide.txt           # Main guide (optional, auto-loaded)
├── guides/             # Multiple guides directory (optional)
│   ├── weapons.txt
│   ├── enemies.txt
│   └── tips.txt
└── README.md           # Mod documentation (optional)
```

## Getting Started

1. **Copy the example mod** as a starting point
2. **Modify the content** to match your ideas
3. **Add your guide.txt file** for easy player help
4. **Test your mod** by adding it to `mods/mods.json`
5. **Share your mod** with other players!

## Example Mod

Check out `example_mod/` to see a complete working mod with:
- New weapons, enemies, and items
- File-based guides (guide.txt + guides/ subdirectory)
- Python-based guides
- All modding features demonstrated

## Need Help?

- Check the example mod for working code
- Look at existing mods for patterns
- The system automatically loads most content
- Guides are the easiest way to help players understand your mod!

## File-Based Guides Are Awesome! 🎉

**No Python coding required!** Just create text files and the game automatically:
- Loads your guides
- Makes them accessible to players
- Integrates them into the help system
- Updates when you modify the files

This makes modding accessible to everyone, even those who don't know Python!
