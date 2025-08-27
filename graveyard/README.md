# 🏛️ Graveyard - Character Revival Guide

Welcome to the graveyard, where fallen heroes rest. This folder contains the save files of characters who have died during their adventures.

## 📁 What's in this folder?

- **Character save files** (`.json` files) - These are automatically gitignored
- **README.md** - This file, explaining how to revive characters

## ⚡ How to Revive a Character (Manual Method)

**⚠️ WARNING: This is a manual process that requires editing save files directly. Use at your own risk!**

**🎯 What You're Doing**: You will manually edit the character's save file to change the `living` variable from `false` to `true`. This tells the game that the character is alive again.

### Step 1: Find the Dead Character
Look for `.json` files in this folder. Each file represents a dead character with a name like `character_1234567890.json`.

### Step 2: Open the Save File
Open the `.json` file in any text editor (Notepad, VS Code, etc.).

### Step 3: Edit the Living Status
Find this line in the file:
```json
"living": false
```

Change it to:
```json
"living": true
```

**⚠️ IMPORTANT**: You MUST change this variable to revive a character!

### Understanding Variable Editing
When you open the JSON file, you'll see many lines like this:
```json
"player_hp": 0,
"player_max_hp": 100,
"living": false,
"death_floor": 2
```

**To revive a character, you need to find and change the `"living"` line:**
- **Find**: `"living": false`
- **Change to**: `"living": true`

**⚠️ Be very careful with the syntax:**
- Keep the quotes around `"living"`
- Keep the colon `:`
- Change only `false` to `true`
- Don't add or remove any commas, brackets, or quotes

### Step 4: Clear Death Information (Optional)
You can also clear the death-related fields to reset the character's death status:
```json
"death_floor": null,
"death_x": null,
"death_y": null,
"death_timestamp": null,
"last_death_date": null
```

**Note:** The `times_died` field will be preserved to maintain death history.

### Step 5: Save and Load
1. Save the modified `.json` file
2. Copy it to the `saves/` folder (rename it to something like `revived_character.json`)
3. In the game, use the `load` command and select your revived character

## 🔧 Advanced Revival Options

### Restore HP and Resources
You can also edit other stats to give your revived character a fresh start. **It's recommended to set current HP to a safe level**:

```json
"player_hp": 50,        // Current HP - set this to a safe amount!
"player_max_hp": 50,    // Maximum HP
"player_stamina": 100,  // Current stamina
"player_max_stamina": 100, // Maximum stamina
"player_mana": 50,      // Current mana
"player_max_mana": 50   // Maximum mana
```

**💡 Tip**: Set `player_hp` to a value between 25-50 for safety. Don't set it to 0 or very low values, or your character might die immediately when loaded!

### Reset Position
To start from a specific location:
```json
"player_floor": 1,
"player_x": 0,
"player_y": 0
```

### Restore Inventory
If you want to give the character back their items:
```json
"inventory": [...],
"armor_inventory": [...],
"player_money": 150
```

## 📊 Understanding Character Data

Each character save contains:
- **Basic Stats**: HP, stamina, mana, level, XP
- **Inventory**: Weapons, armor, items, gold
- **Progress**: Enemies defeated, rooms explored, achievements
- **Death Info**: When and where they died, how many times
- **Character ID**: Unique identifier for the character

## 🚨 Important Notes

1. **Backup First**: Always make a backup of the original file before editing
2. **JSON Format**: Be careful not to break the JSON syntax (commas, brackets, quotes)
3. **Game Balance**: Reviving characters with full resources may affect game balance
4. **Save Compatibility**: Modified saves should work with the current game version
5. **No Auto-Revival**: The game will not automatically revive characters

## 🚫 What Happens If You Try to Load a Dead Character?

If you try to load a character that still has `"living": false`, the game will show this message:
> "That character is dead! Go check the graveyard folder and read the README for how to revive it!"

**This is a safety feature** - the game won't let you play a dead character until you manually revive them by editing the save file.

## 🎮 In-Game Death System

When a character dies:
- They are automatically saved to this graveyard
- Death location, floor, and timestamp are recorded
- Death counter increments
- Character status is set to "dead" (`living: false`)

## 🔍 Finding Dead Characters

The game will show special messages in graveyard rooms when dead characters exist on that floor:
> "There are a lot of graves with names that seem familiar for some reason..."

This indicates that characters have died on the current floor and are resting in the graveyard.

---

**Remember: With great power comes great responsibility. Use manual revival wisely!**
