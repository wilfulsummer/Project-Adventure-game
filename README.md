# Adventure Game

A text-based adventure game with combat, exploration, and progression systems. Fight enemies, collect items, explore multiple floors, and discover secrets in this immersive RPG experience.

## 🚀 Quick Start

### Prerequisites

**Python 3.7 or higher** is required to run this game.

#### Installing Python

1. **Download Python**: Visit [python.org/downloads](https://www.python.org/downloads/) and download the latest version for your operating system.

2. **Install Python**:
   - **Windows**: Run the installer and make sure to check "Add Python to PATH" during installation
   - **macOS**: Run the installer package
   - **Linux**: Use your package manager (e.g., `sudo apt install python3` on Ubuntu)

3. **Verify Installation**: Open a terminal/command prompt and run:
   ```bash
   python --version
   ```
   or
   ```bash
   python3 --version
   ```

### Running the Game

1. **Download the Game**: Download all the game files to a folder on your computer

2. **Open Terminal/Command Prompt**: Navigate to the game folder:
   ```bash
   cd path/to/Adventure_game.py
   ```

3. **Run the Game**:
   ```bash
   python adventure_game.py
   ```
   or
   ```bash
   python3 adventure_game.py
   ```

## 🎮 First Time Playing

### Getting Started

1. **Start the Game**: Run `python adventure_game.py` in your terminal

2. **You'll Start On Floor 1**: You begin in a room with a training dummy at coordinates (0,0)

3. **Basic Commands to Try**:
   - `north`, `south`, `east`, `west` - Move around
   - `attack` - Fight the training dummy (practice combat)
   - `take` - Pick up the Rusty Sword
   - `inventory` - View your weapons
   - `stats` - See your detailed statistics
   - `guide` - Get help with commands

### First Steps

1. **Practice Combat**: Attack the training dummy to learn how combat works
2. **Explore**: Move around to discover new rooms and enemies
3. **Collect Items**: Use `take` to pick up weapons and armor you find
4. **Fight Enemies**: Defeat enemies to earn gold and materials
5. **Visit Shops**: Buy items and upgrades with your gold

### Essential Commands

| Command | Description |
|---------|-------------|
| `north/south/east/west` | Move in that direction |
| `attack` | Fight enemies in the current room |
| `take` | Pick up weapons and armor |
| `inventory` | View your weapons |
| `armor` | View your armor |
| `stats` | Show detailed statistics |
| `save` | Save your progress |
| `load` | Load a saved game |
| `guide` | Show all available commands |

## 🎯 Game Features

### Combat System
- **Weapon Management**: Carry up to 3 weapons, switch between them
- **Armor System**: Equip armor for damage reduction
- **Durability**: Weapons and armor degrade with use
- **Repair System**: Fix damaged equipment at shops
- **Status Effects**: Use spells with burning, poison, and stun effects

### Exploration
- **Multiple Floors**: Explore different levels with unique enemies
- **Waypoint System**: Set teleport points to return to later
- **Room Types**: Shops, chests, boss rooms, and more
- **Materials Collection**: Gather materials from defeated enemies

### Progression
- **Experience Tracking**: Monitor your combat and exploration stats
- **Key System**: Collect mysterious keys to unlock new floors
- **Boss Battles**: Fight powerful bosses for special rewards
- **Unique Items**: Discover rare equipment and materials

### Economy
- **Gold System**: Earn gold from defeated enemies
- **Shop System**: Buy weapons, armor, potions, and keys
- **Chest Loot**: Use golden keys to open treasure chests
- **Resource Management**: Manage HP, stamina, and mana

## 🛠️ Development

### Running Tests
```bash
python run_tests.py
```

### File Structure
- `adventure_game.py` - Main game file
- `command_handlers.py` - Command processing
- `constants.py` - Game constants and configurations
- `game_state.py` - Game state management
- `save_load.py` - Save/load functionality
- `ui_functions.py` - User interface functions
- `unique_items.py` - Unique item system
- `world_generation.py` - World and room generation

## 🐛 Troubleshooting

### Common Issues

**"python is not recognized"**
- Make sure Python is installed and added to PATH
- Try using `python3` instead of `python`

**"No module named 'random'"**
- This is a built-in module, should work with any Python 3.x installation

**Game crashes or freezes**
- Try running the game in a fresh terminal
- Check that all game files are in the same folder

### Getting Help

- Use the `guide` command in-game for detailed help
- Check the test results to ensure the game is working properly
- All game mechanics are thoroughly tested with 39 unit tests

## 📊 Test Coverage

The game includes comprehensive test coverage with 39 unit tests covering:
- Combat mechanics and weapon systems
- Inventory and item management
- Movement and exploration
- Save/load functionality
- Shop and economy systems
- Status effects and spells
- Waypoint and teleport systems

Run `python run_tests.py` to verify everything is working correctly.

## 🎉 Enjoy Your Adventure!

The game is designed to be both accessible for beginners and deep enough for experienced players. Start with the training dummy, explore the world, and see how far you can progress!

Remember: Use `guide` anytime in-game for help with commands and game mechanics.
