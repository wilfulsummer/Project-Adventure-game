# Adventure Game

A text-based adventure game written in Python with roguelike elements, featuring exploration, combat, inventory management, and progression systems.

## Features

### Core Gameplay
- **Exploration**: Navigate through procedurally generated rooms across multiple floors
- **Combat System**: Turn-based combat with weapons, armor, and special abilities
- **Inventory Management**: Collect and manage weapons, armor, and items
- **Progression**: Unlock new floors, discover enemies, and find better equipment

### Combat Features
- **Weapon System**: Multiple weapon types with durability and damage scaling
- **Critical Hits**: 5% base crit chance, daggers have 20% crit chance with 2.6x damage
- **Magic System**: Cast spells using Spell Books and learned scrolls
- **Status Effects**: Burning, Poison, and Stun effects
- **Armor System**: Defense mechanics with armor piercing enemies

### Items & Resources
- **Weapons**: Swords, Bows, Magic Staffs, Daggers, Axes, Spell Books
- **Armor**: Leather, Iron, Bone, and Troll armor with defense ratings
- **Potions**: Health, Stamina, and Mana potions
- **Crystals**: Life, Stamina, and Mana crystals for permanent stat increases
- **Keys**: Mysterious keys for floor access, Golden keys for treasure chambers

### Progression Systems
- **Multi-floor Exploration**: Descend deeper for better loot and stronger enemies
- **Waypoint System**: Mark and teleport to important locations
- **Bestiary**: Track discovered enemies and their information
- **Save/Load**: Persistent game state with JSON save files

### Special Features
- **Training Dummy**: Practice combat without losing weapon durability
- **Shops**: Buy items, potions, and special equipment
- **Treasure Chambers**: High-value loot behind boss encounters
- **Spell Learning**: Collect and learn magical abilities

## How to Play

### Installation
1. Ensure you have Python 3.6+ installed
2. Download the `adventure_game.py` file
3. Run the game: `python adventure_game.py`

### Basic Commands
- **Movement**: `north`, `south`, `east`, `west`
- **Combat**: `attack`, `run`
- **Inventory**: `take`, `drop`, `inventory`, `switch`
- **Resources**: `absorb`, `use`
- **Progression**: `descend`, `take_key`, `open`, `loot`
- **Utility**: `map`, `waypoint`, `save`, `load`, `guide`

### Getting Started
1. Start at Floor 0, Room (0,0) with a training dummy
2. Explore nearby rooms to find weapons and armor
3. Defeat enemies to earn gold and discover new areas
4. Use `guide` command for detailed help on any topic
5. Save your progress regularly with the `save` command

## Game Mechanics

### Scaling System
- Items and enemies scale with distance from (0,0)
- Scaling caps at 100 rooms away for balance
- Higher floors offer better equipment and stronger enemies

### Inventory Limits
- Maximum 3 weapons in inventory
- Maximum 2 armor pieces in inventory
- Maximum 3 golden keys and waypoint scrolls

### Combat Tips
- Use daggers for high critical hit potential
- Magic staffs require mana but deal extra damage
- Boss enemies can be escaped from by moving away
- Regular enemies block your path until defeated

## File Structure
```
Adventure_game.py/
├── adventure_game.py    # Main game file
├── savegame.json        # Save file (auto-generated)
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Development

This game is designed to be easily extensible. Key areas for modification:
- Add new weapon types in the `weapon_names` list
- Create new spells in the `spells` dictionary
- Add new enemies to `enemy_stats`
- Modify room generation in `create_room()`

## License

This project is open source. Feel free to modify and distribute as you wish.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the game!

---

*Enjoy your adventure! Remember to save often and explore thoroughly.* 