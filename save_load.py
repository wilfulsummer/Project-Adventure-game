import json
import os
import glob

# Default values for save compatibility
SAVE_DEFAULTS = {
    # Core player stats
    "player_hp": 50,
    "player_max_hp": 50,
    "player_stamina": 20,
    "player_max_stamina": 20,
    "player_mana": 20,
    "player_max_mana": 20,
    "player_money": 0,
    "player_potions": 0,
    "stamina_potions": 0,
    "mana_potions": 0,
    "waypoint_scrolls": 1,
    "golden_keys": 0,
    
    # Leveling system
    "player_level": 1,
    "player_xp": 0,
    "player_xp_to_next": 100,
    "player_skill_points": 0,
    
    # Statistics tracking
    "enemies_defeated": 0,
    "bosses_defeated": 0,
    "total_damage_dealt": 0,
    "total_damage_taken": 0,
    "critical_hits": 0,
    "attack_count": 0,
    "rooms_explored": 0,
    "move_count": 0,
    "items_collected": 0,
    "weapons_broken": 0,
    "armor_broken": 0,
    "gold_earned": 0,
    
    # Collections and flags
    "inventory": [],
    "armor_inventory": [],
    "equipped_armor": None,
    "mysterious_keys": {},
    "unlocked_floors": [],
    "waypoints": {},
    "discovered_enemies": [],
    "learned_spells": [],
    "spell_scrolls": {},
    "using_fists": False,
    "discovered_uniques": {},
    "materials_inventory": {},
    "floors_visited": [],
    "has_viewed_mechanics": False
}

def get_save_field_with_default(data, field_name, default_value=None):
    """Get a field from save data with fallback to defaults"""
    if field_name in data:
        return data[field_name]
    
    # Check if we have a default for this field
    if default_value is None and field_name in SAVE_DEFAULTS:
        return SAVE_DEFAULTS[field_name]
    
    return default_value

# Directory for save files
SAVE_DIR = "saves"
DEFAULT_SAVE = "savegame.json"

def ensure_save_directory():
    """Ensure the saves directory exists"""
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

def get_save_file_path(save_name):
    """Get the full path for a save file"""
    ensure_save_directory()
    if save_name == "default":
        return os.path.join(SAVE_DIR, DEFAULT_SAVE)
    else:
        # Clean the filename to be safe
        safe_name = "".join(c for c in save_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_name = safe_name.replace(' ', '_')
        return os.path.join(SAVE_DIR, f"{safe_name}.json")

def list_save_files():
    """List all available save files"""
    ensure_save_directory()
    save_files = []
    
    # Check for auto-save (slot 0)
    auto_save_path = os.path.join(SAVE_DIR, "auto_save.json")
    if os.path.exists(auto_save_path):
        save_files.append(("auto_save", "Auto Save (Most Recent)"))
    
    # Check for default save
    default_path = os.path.join(SAVE_DIR, DEFAULT_SAVE)
    if os.path.exists(default_path):
        save_files.append(("default", "Default Save"))
    
    # Check for named saves
    pattern = os.path.join(SAVE_DIR, "*.json")
    for file_path in glob.glob(pattern):
        filename = os.path.basename(file_path)
        if filename not in ["auto_save.json", DEFAULT_SAVE]:
            save_name = os.path.splitext(filename)[0]
            save_name = save_name.replace('_', ' ')
            save_files.append((save_name, save_name.title()))
    
    return save_files

def save_game(save_name, worlds, inventory, armor_inventory, equipped_armor, player_floor, player_x, player_y,
              player_hp, player_max_hp, player_stamina, player_max_stamina, player_mana, player_max_mana,
              player_money, player_potions, stamina_potions, mana_potions, mysterious_keys, golden_keys,
              unlocked_floors, waypoints, waypoint_scrolls, discovered_enemies, learned_spells, spell_scrolls, using_fists,
              player_level=1, player_xp=0, player_xp_to_next=100, player_skill_points=0, enemies_defeated=0, bosses_defeated=0,
              total_damage_dealt=0, total_damage_taken=0, critical_hits=0, attack_count=0, rooms_explored=0,
              floors_visited=None, move_count=0, items_collected=0, weapons_broken=0, gold_earned=0):
    
    # Import unique items system to get discovered uniques
    from unique_items import discovered_uniques
    
    # Handle floors_visited set conversion - ensure it's always a set before converting to list
    if floors_visited is None:
        floors_visited = set()
    elif isinstance(floors_visited, int):
        # Convert old integer format to set
        floors_visited = set([floors_visited]) if floors_visited > 0 else set()
    elif not isinstance(floors_visited, (set, list)):
        # Fallback for any other unexpected types
        floors_visited = set()
    
    data = {
        "save_name": save_name,
        "timestamp": "now",  # Could add actual timestamp later
        "worlds": {
            str(floor): {
                f"{x},{y}": {
                    "description": r["description"],
                    "type": r.get("type"),
                    "enemy": r["enemy"],
                    "weapons": r.get("weapons", []),
                    "armors": r.get("armors", []),
                    "shop": r.get("shop"),
                    "chest": r.get("chest"),
                    "crystal_type": r.get("crystal_type"),
                    "key_required": r.get("key_required"),
                    "requires_mysterious_key": r.get("requires_mysterious_key"),
                    "treasure_looted": r.get("treasure_looted"),
                    "mysterious_key": r.get("mysterious_key")
                } for (x, y), r in world.items()
            } for floor, world in worlds.items()
        },
        "inventory": inventory,
        "armor_inventory": armor_inventory,
        "equipped_armor": equipped_armor,
        "player_floor": player_floor,
        "player_x": player_x,
        "player_y": player_y,
        "player_hp": player_hp,
        "player_max_hp": player_max_hp,
        "player_stamina": player_stamina,
        "player_max_stamina": player_max_stamina,
        "player_mana": player_mana,
        "player_max_mana": player_max_mana,
        "player_money": player_money,
        "player_potions": player_potions,
        "stamina_potions": stamina_potions,
        "mana_potions": mana_potions,
        "mysterious_keys": mysterious_keys,
        "golden_keys": golden_keys,
        "unlocked_floors": list(unlocked_floors) if isinstance(unlocked_floors, set) else [],
        "waypoints": waypoints,
        "waypoint_scrolls": waypoint_scrolls,
        "discovered_enemies": list(discovered_enemies) if isinstance(discovered_enemies, set) else [],
        "learned_spells": learned_spells,
        "spell_scrolls": spell_scrolls,
        "using_fists": using_fists,
        "discovered_uniques": discovered_uniques,
        "player_level": player_level,
        "player_xp": player_xp,
        "player_xp_to_next": player_xp_to_next,
        "player_skill_points": player_skill_points,
        "enemies_defeated": enemies_defeated,
        "bosses_defeated": bosses_defeated,
        "total_damage_dealt": total_damage_dealt,
        "total_damage_taken": total_damage_taken,
        "critical_hits": critical_hits,
        "attack_count": attack_count,
        "rooms_explored": rooms_explored,
        "floors_visited": list(floors_visited),
        "move_count": move_count,
        "items_collected": items_collected,
        "weapons_broken": weapons_broken,
        "gold_earned": gold_earned
    }
    
    save_path = get_save_file_path(save_name)
    with open(save_path, "w") as f:
        json.dump(data, f)
    
    if save_name == "default":
        print("Game saved to default save!")
    else:
        print(f"Game saved as '{save_name}'!")
    
    return save_path

def auto_save_game(worlds, inventory, armor_inventory, equipped_armor, player_floor, player_x, player_y,
                   player_hp, player_max_hp, player_stamina, player_max_stamina, player_mana, player_max_mana,
                   player_money, player_potions, stamina_potions, mana_potions, mysterious_keys, golden_keys,
                   unlocked_floors, waypoints, waypoint_scrolls, discovered_enemies, learned_spells, spell_scrolls, using_fists,
                   player_level=1, player_xp=0, player_xp_to_next=100, player_skill_points=0, enemies_defeated=0, bosses_defeated=0,
                   total_damage_dealt=0, total_damage_taken=0, critical_hits=0, attack_count=0, rooms_explored=0,
                   floors_visited=None, move_count=0, items_collected=0, weapons_broken=0, gold_earned=0):
    """Auto-save the game (overwrites previous auto-save)"""
    
    # Ensure set parameters are properly converted to lists for JSON serialization
    unlocked_floors_list = list(unlocked_floors) if isinstance(unlocked_floors, set) else unlocked_floors
    discovered_enemies_list = list(discovered_enemies) if isinstance(discovered_enemies, set) else discovered_enemies
    floors_visited_list = list(floors_visited) if isinstance(floors_visited, set) else floors_visited
    
    return save_game("auto_save", worlds, inventory, armor_inventory, equipped_armor, player_floor, player_x, player_y,
                     player_hp, player_max_hp, player_stamina, player_max_stamina, player_mana, player_max_mana,
                     player_money, player_potions, stamina_potions, mana_potions, mysterious_keys, golden_keys,
                     unlocked_floors_list, waypoints, waypoint_scrolls, discovered_enemies_list, learned_spells, spell_scrolls, using_fists,
                     player_level, player_xp, player_xp_to_next, enemies_defeated, bosses_defeated, total_damage_dealt,
                     total_damage_taken, critical_hits, attack_count, rooms_explored, floors_visited_list, move_count,
                     items_collected, weapons_broken, gold_earned)

def load_game(save_name=None):
    """Load a game from a specific save file"""
    if save_name is None:
        # Show available saves and let user choose
        save_files = list_save_files()
        
        if not save_files:
            print("No saved games found.")
            return None
        
        print("\nAvailable save files:")
        for i, (file_name, display_name) in enumerate(save_files, 1):
            print(f"  {i}. {display_name}")
        
        while True:
            try:
                choice = input(f"\nSelect save file (1-{len(save_files)}) or type name: ").strip()
                
                # Check if it's a number choice
                if choice.isdigit():
                    choice_num = int(choice)
                    if 1 <= choice_num <= len(save_files):
                        save_name = save_files[choice_num - 1][0]
                        break
                    else:
                        print(f"Please enter a number between 1 and {len(save_files)}")
                else:
                    # Check if it's a valid save name
                    valid_names = [name for name, _ in save_files]
                    if choice in valid_names:
                        save_name = choice
                        break
                    elif choice == "default" and any(name == "default" for name, _ in save_files):
                        save_name = "default"
                        break
                    else:
                        print(f"Save file '{choice}' not found. Available saves:")
                        for name, display_name in save_files:
                            print(f"  - {display_name}")
            except ValueError:
                print("Please enter a valid number or save name.")
    
    save_path = get_save_file_path(save_name)
    
    if not os.path.exists(save_path):
        print(f"Save file '{save_name}' not found.")
        return None

    try:
        with open(save_path, "r") as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        print(f"Error reading save file '{save_name}'. File may be corrupted.")
        return None

    # Handle old save format
    if "world" in data:
        # Convert old single-floor format to new multi-floor format
        worlds = {}
        worlds[0] = {}
        for key, value in data["world"].items():
            x, y = map(int, key.split(","))
            worlds[0][(x, y)] = value
        player_floor = data.get("player_floor", 1)
    else:
        # New multi-floor format
        worlds = {}
        for floor_str, world_data in data["worlds"].items():
            floor = int(floor_str)
            worlds[floor] = {}
            for key, value in world_data.items():
                x, y = map(int, key.split(","))
                worlds[floor][(x, y)] = value
        player_floor = data["player_floor"]
    
    player_x = data["player_x"]
    player_y = data["player_y"]
    inventory = get_save_field_with_default(data, "inventory")
    armor_inventory = get_save_field_with_default(data, "armor_inventory")
    equipped_armor = get_save_field_with_default(data, "equipped_armor")
    player_hp = get_save_field_with_default(data, "player_hp")
    player_max_hp = get_save_field_with_default(data, "player_max_hp")
    player_stamina = get_save_field_with_default(data, "player_stamina")
    player_max_stamina = get_save_field_with_default(data, "player_max_stamina")
    player_mana = get_save_field_with_default(data, "player_mana")
    player_max_mana = get_save_field_with_default(data, "player_max_mana")
    player_money = get_save_field_with_default(data, "player_money")
    player_potions = get_save_field_with_default(data, "player_potions")
    stamina_potions = get_save_field_with_default(data, "stamina_potions")
    mana_potions = get_save_field_with_default(data, "mana_potions")
    waypoint_scrolls = get_save_field_with_default(data, "waypoint_scrolls")
    
    # Handle old mysterious_key format
    if "mysterious_key" in data and data["mysterious_key"]:
        mysterious_keys = {1: True}  # Old saves get Floor 1 key
    else:
        mysterious_keys = get_save_field_with_default(data, "mysterious_keys")
    
    golden_keys = get_save_field_with_default(data, "golden_keys")
    unlocked_floors = set(get_save_field_with_default(data, "unlocked_floors"))
    
    # Handle old waypoint format
    old_waypoints = get_save_field_with_default(data, "waypoints")
    if old_waypoints and isinstance(next(iter(old_waypoints.values())), tuple) and len(next(iter(old_waypoints.values()))) == 2:
        # Convert old (x, y) format to new (floor, x, y) format
        waypoints = {}
        for name, (x, y) in old_waypoints.items():
            waypoints[name] = (0, x, y)
    else:
        waypoints = old_waypoints
    
    discovered_enemies = set(get_save_field_with_default(data, "discovered_enemies"))
    
    # Handle floors_visited conversion - ensure it's always a set
    floors_visited_data = get_save_field_with_default(data, "floors_visited")
    if isinstance(floors_visited_data, int):
        floors_visited = set([floors_visited_data]) if floors_visited_data > 0 else set()
    elif isinstance(floors_visited_data, list):
        floors_visited = set(floors_visited_data)
    else:
        floors_visited = set()
    learned_spells = get_save_field_with_default(data, "learned_spells")
    spell_scrolls = get_save_field_with_default(data, "spell_scrolls")
    using_fists = get_save_field_with_default(data, "using_fists")
    
    # Load unique items discovered
    discovered_uniques = get_save_field_with_default(data, "discovered_uniques")
    
    # Handle newly added stats with sensible defaults
    attack_count = get_save_field_with_default(data, "attack_count")
    move_count = get_save_field_with_default(data, "move_count")
    has_viewed_mechanics = get_save_field_with_default(data, "has_viewed_mechanics")
    materials_inventory = get_save_field_with_default(data, "materials_inventory")
    armor_broken = get_save_field_with_default(data, "armor_broken")
    
    save_display_name = data.get("save_name", save_name)
    print(f"Game loaded from '{save_display_name}'!")
    
    return {
        "worlds": worlds,
        "player_floor": player_floor,
        "player_x": player_x,
        "player_y": player_y,
        "inventory": inventory,
        "armor_inventory": armor_inventory,
        "equipped_armor": equipped_armor,
        "player_hp": player_hp,
        "player_max_hp": player_max_hp,
        "player_stamina": player_stamina,
        "player_max_stamina": player_max_stamina,
        "player_mana": player_mana,
        "player_max_mana": player_max_mana,
        "player_money": player_money,
        "player_potions": player_potions,
        "stamina_potions": stamina_potions,
        "mana_potions": mana_potions,
        "mysterious_keys": mysterious_keys,
        "golden_keys": golden_keys,
        "unlocked_floors": unlocked_floors,
        "waypoints": waypoints,
        "waypoint_scrolls": waypoint_scrolls,
        "discovered_enemies": discovered_enemies,
        "learned_spells": learned_spells,
        "spell_scrolls": spell_scrolls,
        "using_fists": using_fists,
        "discovered_uniques": discovered_uniques,
        "player_level": get_save_field_with_default(data, "player_level"),
        "player_xp": get_save_field_with_default(data, "player_xp"),
        "player_xp_to_next": get_save_field_with_default(data, "player_xp_to_next"),
        "player_skill_points": get_save_field_with_default(data, "player_skill_points"),
        "enemies_defeated": get_save_field_with_default(data, "enemies_defeated"),
        "bosses_defeated": get_save_field_with_default(data, "bosses_defeated"),
        "total_damage_dealt": get_save_field_with_default(data, "total_damage_dealt"),
        "total_damage_taken": get_save_field_with_default(data, "total_damage_taken"),
        "critical_hits": get_save_field_with_default(data, "critical_hits"),
        "attack_count": get_save_field_with_default(data, "attack_count"),
        "rooms_explored": get_save_field_with_default(data, "rooms_explored"),
        "floors_visited": get_save_field_with_default(data, "floors_visited"),
        "move_count": get_save_field_with_default(data, "move_count"),
        "items_collected": get_save_field_with_default(data, "items_collected"),
        "weapons_broken": get_save_field_with_default(data, "weapons_broken"),
        "gold_earned": get_save_field_with_default(data, "gold_earned")
    }

def delete_save(save_name):
    """Delete a specific save file"""
    save_path = get_save_file_path(save_name)
    
    if not os.path.exists(save_path):
        print(f"Save file '{save_name}' not found.")
        return False
    
    try:
        os.remove(save_path)
        print(f"Save file '{save_name}' deleted!")
        return True
    except OSError as e:
        print(f"Error deleting save file: {e}")
        return False

def show_save_info(save_name):
    """Show information about a specific save file"""
    save_path = get_save_file_path(save_name)
    
    if not os.path.exists(save_path):
        print(f"Save file '{save_name}' not found.")
        return
    
    try:
        with open(save_path, "r") as f:
            data = json.load(f)
        
        print(f"\n=== SAVE INFO: {data.get('save_name', save_name)} ===")
        print(f"Player Level: {data.get('player_level', 'Unknown')}")
        print(f"Skill Points: {data.get('player_skill_points', 'Unknown')}")
        print(f"Floor: {data.get('player_floor', 'Unknown')}")
        print(f"Position: ({data.get('player_x', 'Unknown')}, {data.get('player_y', 'Unknown')})")
        print(f"HP: {data.get('player_hp', 'Unknown')}/{data.get('player_max_hp', 'Unknown')}")
        print(f"Stamina: {data.get('player_stamina', 'Unknown')}/{data.get('player_max_stamina', 'Unknown')}")
        print(f"Mana: {data.get('player_mana', 'Unknown')}/{data.get('player_max_mana', 'Unknown')}")
        print(f"Money: {data.get('player_money', 'Unknown')}")
        print(f"Unlocked Floors: {len(data.get('unlocked_floors', []))}")
        print(f"Discovered Enemies: {len(data.get('discovered_enemies', []))}")
        print(f"Learned Spells: {len(data.get('learned_spells', []))}")
        print(f"Weapons: {len(data.get('inventory', []))}")
        print(f"Armor: {len(data.get('armor_inventory', []))}")
        
    except (json.JSONDecodeError, FileNotFoundError):
        print(f"Error reading save file '{save_name}'. File may be corrupted.")

# Backward compatibility functions
def save_game_old(worlds, inventory, armor_inventory, equipped_armor, player_floor, player_x, player_y,
                  player_hp, player_max_hp, player_stamina, player_max_stamina, player_mana, player_max_mana,
                  player_money, player_potions, stamina_potions, mana_potions, mysterious_keys, golden_keys,
                  unlocked_floors, waypoints, waypoint_scrolls, discovered_enemies, learned_spells, spell_scrolls, using_fists):
    """Old save function for backward compatibility"""
    return save_game("default", worlds, inventory, armor_inventory, equipped_armor, player_floor, player_x, player_y,
                     player_hp, player_max_hp, player_stamina, player_max_stamina, player_mana, player_max_mana,
                     player_money, player_potions, stamina_potions, mana_potions, mysterious_keys, golden_keys,
                     unlocked_floors, waypoints, waypoint_scrolls, discovered_enemies, learned_spells, spell_scrolls, using_fists,
                     1, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

def load_game_old():
    """Old load function for backward compatibility"""
    return load_game("default") 