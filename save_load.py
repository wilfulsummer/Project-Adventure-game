import json
import os
from constants import SAVE_FILE

def save_game(worlds, inventory, armor_inventory, equipped_armor, player_floor, player_x, player_y,
              player_hp, player_max_hp, player_stamina, player_max_stamina, player_mana, player_max_mana,
              player_money, player_potions, stamina_potions, mana_potions, mysterious_keys, golden_keys,
              unlocked_floors, waypoints, waypoint_scrolls, discovered_enemies, learned_spells, spell_scrolls, using_fists):
    data = {
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
        "unlocked_floors": list(unlocked_floors),
        "waypoints": waypoints,
        "waypoint_scrolls": waypoint_scrolls,
        "discovered_enemies": list(discovered_enemies),
        "learned_spells": learned_spells,
        "spell_scrolls": spell_scrolls,
        "using_fists": using_fists
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)
    print("Game saved!")

def load_game():
    if not os.path.exists(SAVE_FILE):
        print("No saved game found.")
        return None

    with open(SAVE_FILE, "r") as f:
        data = json.load(f)

    # Handle old save format
    if "world" in data:
        # Convert old single-floor format to new multi-floor format
        worlds = {}
        worlds[0] = {}
        for key, value in data["world"].items():
            x, y = map(int, key.split(","))
            worlds[0][(x, y)] = value
        player_floor = data.get("player_floor", 0)
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
    inventory = data["inventory"]
    armor_inventory = data["armor_inventory"]
    equipped_armor = data["equipped_armor"]
    player_hp = data["player_hp"]
    player_max_hp = data["player_max_hp"]
    player_stamina = data.get("player_stamina", 20)
    player_max_stamina = data.get("player_max_stamina", 20)
    player_mana = data.get("player_mana", 20)
    player_max_mana = data.get("player_max_mana", 20)
    player_money = data["player_money"]
    player_potions = data["player_potions"]
    stamina_potions = data.get("stamina_potions", 0)
    mana_potions = data.get("mana_potions", 0)
    waypoint_scrolls = data.get("waypoint_scrolls", 0)
    
    # Handle old mysterious_key format
    if "mysterious_key" in data and data["mysterious_key"]:
        mysterious_keys = {0: True}  # Old saves get Floor 0 key
    else:
        mysterious_keys = data.get("mysterious_keys", {})
    
    golden_keys = data.get("golden_keys", 0)
    unlocked_floors = set(data.get("unlocked_floors", []))
    
    # Handle old waypoint format
    old_waypoints = data.get("waypoints", {})
    if old_waypoints and isinstance(next(iter(old_waypoints.values())), tuple) and len(next(iter(old_waypoints.values()))) == 2:
        # Convert old (x, y) format to new (floor, x, y) format
        waypoints = {}
        for name, (x, y) in old_waypoints.items():
            waypoints[name] = (0, x, y)
    else:
        waypoints = old_waypoints
    
    discovered_enemies = set(data.get("discovered_enemies", []))
    learned_spells = data.get("learned_spells", [])
    spell_scrolls = data.get("spell_scrolls", {})
    using_fists = data.get("using_fists", False)
    
    print("Game loaded!")
    
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
        "using_fists": using_fists
    } 