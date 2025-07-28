import random
import json
import os

# --- Constants ---
SAVE_FILE = "savegame.json"
MAX_WEAPONS = 3
MAX_ARMOR = 2
MAX_PLAYER_HP = 250

room_descriptions = [
    "A dark cave with dripping water.",
    "A bright room filled with gold!",
    "A library with ancient dusty books.",
    "A small hut with a warm fireplace.",
    "An underground tunnel that echoes your steps."
    "A mineshaft with bones and dust litted around the walls."
    "A circular chamber where dust dances in the beam of a cracked ceiling stone.",
    "A low corridor with walls scraped as if something massive squeezed through.",
    "A wide room with a floor pattern that hums faintly when you step on it.",
    "A collapsed hall where light filters through twisted roots from above.",
    "A chamber flooded ankle-deep with murky water and floating broken wood.",
    "A dry room with ash scattered in swirling patterns across the stone floor.",
    "A crooked hallway that shifts slightly when you're not looking directly at it.",
    "A narrow nook filled with stacked crates and unmarked jars sealed tight.",
    "A hollow den with strange claw marks circling the walls in spirals.",
    "A cool, echoing space where every sound feels a second too late to arrive."
]

weapon_names = ["Sword", "Bow", "Magic Staff", "Dagger", "Axe", "Spell Book"]

# Spell definitions
spells = {
  "Fire": {
    "name": "Fire",
    "damage": 8,
    "mana_cost": 12,
    "effect": "Burning",
    "effect_damage": 3,
    "effect_duration": 3,
    "cooldown": 3,
    "description": "Deals fire damage and inflicts Burning (3 damage per turn for 3 turns)"
  },
  "Poison": {
    "name": "Poison", 
    "damage": 6,
    "mana_cost": 12,
    "effect": "Poisoned",
    "effect_damage": 2,
    "effect_duration": 4,
    "cooldown": 2,
    "description": "Deals poison damage and inflicts Poisoned (2 damage per turn for 4 turns)"
  },
  "Stun": {
    "name": "Stun",
    "damage": 15,
    "mana_cost": 20,
    "effect": "Stunned",
    "effect_duration": 1,
    "cooldown": 3,
    "description": "Deals high damage and stuns enemy for 1 turn (3 turn cooldown)"
  }
}

enemy_stats = {
    "Goblin": 12,
    "Skeleton": 14,
    "Zombie": 18,
    "Orc": 20,
    "Rat": 8,
    "Hungry Wolf": 10
}

# --- Game State ---
worlds = {}  # Dictionary of floors: {floor: world}
player_floor = 0
player_x = 0
player_y = 0
inventory = []
armor_inventory = []
equipped_armor = None
player_hp = 50
player_max_hp = 50
player_stamina = 20
player_max_stamina = 20
player_mana = 20
player_max_mana = 20
player_money = 0
player_potions = 0
stamina_potions = 0
mana_potions = 0
waypoint_scrolls = 0  # Can hold up to 3 waypoint scrolls
mysterious_keys = {}  # Dictionary of floor-specific mysterious keys: {floor: True}
golden_keys = 0  # Can hold up to 3 golden keys
unlocked_floors = set()  # Set of floors that can be accessed with mysterious keys
waypoints = {}  # Dictionary to store waypoints: {name: (floor, x, y)}
discovered_enemies = set()  # Track which enemies have been defeated
learned_spells = []  # List of learned spells in order
spell_scrolls = {}  # Dictionary of spell scrolls: {spell_name: count}
def distance_from_start(x, y):
  return abs(x) + abs(y)

def show_map():
  """Display the current map with player location and waypoints"""
  print(f"\n=== MAP ===")
  print(f"You are on Floor {player_floor} at: ({player_x}, {player_y})")
  
  if waypoints:
    print("\nWaypoints:")
    for i, (name, (floor, x, y)) in enumerate(waypoints.items(), 1):
      if floor == player_floor:
        distance = abs(x - player_x) + abs(y - player_y)
        direction = ""
        if x > player_x: direction += "E"
        elif x < player_x: direction += "W"
        if y > player_y: direction += "N"
        elif y < player_y: direction += "S"
        if not direction: direction = "HERE"
        print(f"  {i}. {name}: ({x}, {y}) - {distance} steps {direction}")
      else:
        print(f"  {i}. {name}: Floor {floor} ({x}, {y})")
  else:
    print("No waypoints set.")
  print("===========")

def add_waypoint():
  """Add a waypoint at current location"""
  global waypoints
  
  if len(waypoints) >= 10:
    print("You can only have 10 waypoints maximum!")
    return
  
  name = input("Enter waypoint name: ").strip()
  if not name:
    print("Waypoint name cannot be empty!")
    return
  
  if name in waypoints:
    print(f"A waypoint named '{name}' already exists!")
    return
  
  waypoints[name] = (player_floor, player_x, player_y)
  print(f"Waypoint '{name}' added at Floor {player_floor} ({player_x}, {player_y})!")

def view_waypoint():
  """View details of a specific waypoint"""
  if not waypoints:
    print("No waypoints to view.")
    return
  
  print("\nSelect waypoint to view:")
  waypoint_list = list(waypoints.items())
  for i, (name, (floor, x, y)) in enumerate(waypoint_list, 1):
    print(f"  {i}. {name}")
  
  try:
    choice = int(input("Enter number: ")) - 1
    if 0 <= choice < len(waypoint_list):
      name, (floor, x, y) = waypoint_list[choice]
      if floor == player_floor:
        distance = abs(x - player_x) + abs(y - player_y)
        direction = ""
        if x > player_x: direction += "E"
        elif x < player_x: direction += "W"
        if y > player_y: direction += "N"
        elif y < player_y: direction += "S"
        if not direction: direction = "HERE"
        
        print(f"\nWaypoint: {name}")
        print(f"Location: Floor {floor} ({x}, {y})")
        print(f"Distance: {distance} steps")
        print(f"Direction: {direction}")
      else:
        print(f"\nWaypoint: {name}")
        print(f"Location: Floor {floor} ({x}, {y})")
        print("(On different floor)")
      
      # Get room info if it exists
      if floor in worlds and (x, y) in worlds[floor]:
        room = worlds[floor][(x, y)]
        print(f"Room type: {room.get('type', 'normal')}")
        if room.get('enemy'):
          enemy = room['enemy']
          boss_tag = " [BOSS]" if enemy.get('is_boss') else ""
          print(f"Enemy: {enemy['name']}{boss_tag}")
        if room.get('weapons'):
          print(f"Weapons: {len(room['weapons'])} items")
        if room.get('armors'):
          print(f"Armor: {len(room['armors'])} items")
        if room.get('shop'):
          print("Contains: Shop")
        if room.get('chest'):
          print("Contains: Chest")
        if room.get('life_crystal'):
          print("Contains: Life Crystal")
        if room.get('type') == 'key_door' and not room.get('enemy') and not room.get('treasure_looted'):
          print("Contains: Treasure Chamber (requires golden key)")
        elif room.get('type') == 'key_door' and not room.get('enemy') and room.get('treasure_looted'):
          print("Contains: Treasure Chamber (looted)")
        if room.get('type') == 'stairwell':
          print("Contains: Stairwell")
    else:
      print("Invalid choice.")
  except ValueError:
    print("Please enter a valid number.")

def delete_waypoint():
  """Delete a waypoint"""
  if not waypoints:
    print("No waypoints to delete.")
    return
  
  print("\nSelect waypoint to delete:")
  waypoint_list = list(waypoints.items())
  for i, (name, (floor, x, y)) in enumerate(waypoint_list, 1):
    print(f"  {i}. {name} at Floor {floor} ({x}, {y})")
  
  try:
    choice = int(input("Enter number: ")) - 1
    if 0 <= choice < len(waypoint_list):
      name, _ = waypoint_list[choice]
      del waypoints[name]
      print(f"Waypoint '{name}' deleted!")
    else:
      print("Invalid choice.")
  except ValueError:
    print("Please enter a valid number.")

def create_weapon(x, y):
  base_damage = random.randint(5, 10)
  base_durability = random.randint(5, 15)
  distance = distance_from_start(x, y)
  # Cap scaling at 100 rooms away from (0,0)
  capped_distance = min(distance, 100)
  # Adjust scaling to cap at ~25 damage and ~40 durability
  scaled = capped_distance // 4  # Reduced from // 2
  damage_bonus = scaled * random.randint(1, 2)
  durability_bonus = scaled * random.randint(1, 2)
  weapon_name = random.choice(weapon_names)
  
  # Make staffs stronger but require mana
  if weapon_name == "Magic Staff":
    damage = base_damage + damage_bonus + random.randint(1, 2)  # +1 to +2 extra damage
    return {
      "name": weapon_name,
      "damage": damage,
      "durability": base_durability + durability_bonus,
      "requires_mana": True,
      "mana_cost": max(10, damage + random.randint(-2, 2))  # Base 10 + scaling with damage
    }
  elif weapon_name == "Spell Book":
    durability = random.randint(15, 25) + durability_bonus
    return {
      "name": weapon_name,
      "damage": "???",
      "durability": durability
    }
  else:
    return {
      "name": weapon_name,
      "damage": base_damage + damage_bonus,
      "durability": base_durability + durability_bonus
    }

def create_armor(x, y):
  base_defense = random.randint(2, 4)  # Reduced from 5-8 to 2-4
  base_durability = random.randint(8, 15)
  distance = distance_from_start(x, y)
  # Cap scaling at 100 rooms away from (0,0)
  capped_distance = min(distance, 100)
  scaled = capped_distance // 4  # Reduced scaling from //2 to //4
  return {
    "name": random.choice(["Leather Armor", "Iron Mail", "Bone Plate", "Troll Hide"]),
    "defense": base_defense + scaled * random.choice([0, 1]),
    "durability": base_durability + scaled * random.choice([0, 1])
  }

def create_chest_weapon(dist):
  base_damage = random.randint(5, 10)
  base_durability = random.randint(5, 15)
  # Cap scaling at 100 rooms away from (0,0)
  capped_dist = min(dist, 100)
  # Adjust scaling to cap at ~25 damage and ~40 durability
  scaled = capped_dist // 4  # Reduced from // 2
  damage_bonus = scaled * random.randint(1, 2)
  durability_bonus = scaled * random.randint(1, 2)
  weapon_name = random.choice(weapon_names)
  
  # Make staffs stronger but require mana
  if weapon_name == "Magic Staff":
    damage = base_damage + damage_bonus + random.randint(1, 2)  # +1 to +2 extra damage
    return {
      "name": weapon_name,
      "damage": damage,
      "durability": base_durability + durability_bonus,
      "requires_mana": True,
      "mana_cost": max(10, damage + random.randint(-2, 2))  # Base 10 + scaling with damage
    }
  elif weapon_name == "Spell Book":
    durability = random.randint(15, 25) + durability_bonus
    return {
      "name": weapon_name,
      "damage": "???",
      "durability": durability
    }
  else:
    return {
      "name": weapon_name,
      "damage": base_damage + damage_bonus,
      "durability": base_durability + durability_bonus
    }

def create_chest_armor(x, y):
  dist = distance_from_start(x, y) + random.randint(3, 5)
  # Cap scaling at 100 rooms away from (0,0)
  capped_dist = min(dist, 100)
  scaled = capped_dist // 4  # Reduced scaling from //2 to //4
  base_defense = random.randint(3, 6)  # Reduced from 5-8 to 3-6
  base_durability = random.randint(8, 15)
  bonus_def = scaled * random.choice([1, 2])
  bonus_dur = scaled * random.choice([1, 2])
  return {
    "name": random.choice(["Enchanted Mail", "Reinforced Hide", "Darksteel Vest", "Trollbone Harness"]),
    "defense": base_defense + bonus_def,
    "durability": base_durability + bonus_dur
  }

def create_enemy(x, y, force_boss=None):
  dist = distance_from_start(x, y)
  # Cap scaling at 100 rooms away from (0,0)
  capped_dist = min(dist, 100)
  # Adjust scaling to be more balanced (reduced from // 2)
  scaled = capped_dist // 4

  if force_boss == "Troll":
    base_hp = 60
    variation = random.randint(-3, 3)
    return {
      "name": "Troll",
      "hp": base_hp + variation + scaled * random.randint(1, 2),
      "base_attack": 10 + scaled,
      "armor_pierce": 2 + scaled // 3,  # Bosses have more armor piercing, scales with distance from (0,0)
      "is_boss": True
    }

  name = random.choice(list(enemy_stats.keys()))
  base_hp = enemy_stats[name]
  variation = random.randint(-3, 3)
  return {
    "name": name,
    "hp": base_hp + variation + scaled * random.randint(1, 2),
    "base_attack": 5 + scaled,
    "armor_pierce": 1 + scaled // 6,  # Regular enemies have some armor piercing, scales with distance from (0,0)
    "is_boss": False
  }
def create_room(floor, x, y):
  # Stairwell room (1 in 25) - requires mysterious key
  if random.randint(1, 25) == 1:
    return {
      "description": "You find a mysterious stairwell leading deeper into the dungeon...",
      "type": "stairwell",
      "enemy": None,
      "weapons": [],
      "armors": [],
      "shop": None,
      "chest": None,
      "life_crystal": False,
      "requires_mysterious_key": True
    }

  # Golden key door room (1 in 25)
  if random.randint(1, 25) == 1:
    return {
      "description": "You find a glowing golden door… and the Troll guarding it!",
      "type": "key_door",
      "key_required": True,
      "enemy": create_enemy(x, y, force_boss="Troll"),
      "weapons": [],
      "armors": [],
      "shop": None,
      "chest": None,
      "life_crystal": False,
      "treasure_room": True  # Indicates there's a treasure room behind this boss
    }

  # Chest room (1 in 15)
  if random.randint(1, 15) == 1:
    loot = {
      "weapons": [create_chest_weapon(distance_from_start(x, y) + random.randint(3, 5))],
      "potions": 2,
      "locked": True,
      "life_crystal": random.random() < 0.2,
      "armor": create_chest_armor(x, y) if random.random() < 0.5 else None
    }
    if random.random() < 0.3:
      loot["weapons"].append(create_chest_weapon(distance_from_start(x, y) + random.randint(3, 5)))
    return {
      "description": "You find an old stone chamber with a heavy locked chest.",
      "type": "chest",
      "chest": loot,
      "enemy": None,
      "weapons": [],
      "armors": [],
      "shop": None,
      "life_crystal": False
    }

  # Shop (10% chance)
  if random.random() < 0.1:
    items = []
    for _ in range(random.randint(0, 2)):
      base = create_weapon(x, y)
      bonus = random.randint(1, 3)
      items.append({
        "name": f"{base['name']}+{bonus}",
        "damage": base["damage"] + bonus,
        "durability": base["durability"] + bonus,
        "cost": random.randint(10, 25)
      })
    
    # Generate spell scrolls (40% chance, then 30% chance for 2 different spells)
    spell_scrolls_shop = {}
    if random.random() < 0.4:
      available_spells = [spell for spell in spells.keys() if spell not in learned_spells]
      if available_spells:
        spell1 = random.choice(available_spells)
        spell_scrolls_shop[spell1] = 1
        if random.random() < 0.3 and len(available_spells) > 1:
          spell2 = random.choice([s for s in available_spells if s != spell1])
          spell_scrolls_shop[spell2] = 1
    
    shop = {
      "items": items,
      "potion_price": random.randint(8, 15),
      "stamina_potion_price": random.randint(6, 12),
      "mana_potion_price": random.randint(15, 20),
      "has_key": random.random() < 0.4,
      "armor": create_armor(x, y) if random.random() < 0.35 else None,
      "life_crystal": random.random() < 0.1,
      "stamina_potions": random.randint(1, 2) if random.random() < 0.6 else 0,
      "mana_potions": random.randint(1, 2) if random.random() < 0.6 else 0,
      "waypoint_scrolls": random.randint(1, 2) if random.random() < 0.3 else 0,
      "spell_scrolls": spell_scrolls_shop
    }
    return {
      "description": "A cozy shop with items for sale.",
      "type": "shop",
      "shop": shop,
      "enemy": None,
      "weapons": [],
      "armors": [],
      "chest": None,
      "life_crystal": False
    }

  # Crystal room (5% chance) - can have life, stamina, or mana crystal, or combinations
  crystal_type = None
  if random.random() < 0.05:
    crystal_roll = random.random()
    if crystal_roll < 0.04:  # 2% chance for dual crystals
      if random.random() < 0.5:
        crystal_type = "life_stamina"  # Life + Stamina
      else:
        crystal_type = "life_mana"  # Life + Mana
    elif crystal_roll < 0.06:  # 1% chance for triple crystals
      crystal_type = "all"  # All three crystals
    else:
      # Single crystal (2% chance)
      crystal_choice = random.random()
      if crystal_choice < 0.33:
        crystal_type = "life"
      elif crystal_choice < 0.67:
        crystal_type = "stamina"
      else:
        crystal_type = "mana"
  
  weapons = []
  if random.random() < 0.3:
    weapons.append(create_weapon(x, y))
  armors = []
  if random.random() < 0.2:
    armors.append(create_armor(x, y))
  
  # Mysterious key (1 in 50 chance)
  mysterious_key_item = None
  if random.randint(1, 50) == 1:
    mysterious_key_item = {
      "floor": floor,
      "name": f"Mysterious Key (Floor {floor})"
    }
  
  enemy = create_enemy(x, y) if random.random() < 0.5 else None
  return {
    "description": random.choice(room_descriptions),
    "type": "normal",
    "enemy": enemy,
    "weapons": weapons,
    "armors": armors,
    "shop": None,
    "chest": None,
    "crystal_type": crystal_type,
    "mysterious_key": mysterious_key_item
  }

def get_room(floor, x, y):
  if floor not in worlds:
    worlds[floor] = {}
  
  if (x, y) not in worlds[floor]:
    if floor == 0 and x == 0 and y == 0:
      worlds[floor][(x, y)] = {
        "description": "You are in a clearing with a training dummy.",
        "type": "normal",
        "enemy": {
          "name": "Training Dummy",
          "hp": 999,  # Very high HP so it doesn't die
          "base_attack": 0,  # No damage
          "is_boss": False,
          "is_training_dummy": True  # Special flag for training dummy
        },
        "weapons": [{
          "name": "Rusty Sword",
          "damage": 5,
          "durability": 10
        }],
        "armors": [],
        "shop": None,
        "chest": None,
        "crystal_type": None
      }
    else:
      worlds[floor][(x, y)] = create_room(floor, x, y)
  return worlds[floor][(x, y)]
def show_room(room):
  print(f"\nYou enter Floor {player_floor} ({player_x}, {player_y}):", room["description"])

  if room.get("crystal_type") == "life":
    print("A glowing red crystal pulses on a stone pedestal. Use 'absorb' to consume it.")
  elif room.get("crystal_type") == "stamina":
    print("A glowing blue crystal pulses on a stone pedestal. Use 'absorb' to consume it.")
  elif room.get("crystal_type") == "mana":
    print("A glowing purple crystal pulses on a stone pedestal. Use 'absorb' to consume it.")
  elif room.get("crystal_type") == "life_stamina":
    print("Two crystals pulse on stone pedestals - a red life crystal and a blue stamina crystal. Use 'absorb' to consume them.")
  elif room.get("crystal_type") == "life_mana":
    print("Two crystals pulse on stone pedestals - a red life crystal and a purple mana crystal. Use 'absorb' to consume them.")
  elif room.get("crystal_type") == "all":
    print("Three crystals pulse on stone pedestals - a red life crystal, a blue stamina crystal, and a purple mana crystal. Use 'absorb' to consume them.")

  if room.get("type") == "chest" and room.get("chest"):
    if room["chest"]["locked"]:
      print("There is a heavy chest here. It looks like it requires a golden key.")
    else:
      print("The opened chest lies empty.")

    if room.get("type") == "key_door":
      if room.get("enemy"):
        print("A glowing golden door blocks your path. A monstrous Troll stands guard!")
      else:
        # Boss defeated, door is now open
        if not room.get("treasure_looted"):
          print("The golden door is now open! A magnificent treasure chamber lies beyond!")
          if golden_keys > 0:
            print(f"Use 'loot' to collect the treasure with your golden key. (You have {golden_keys})")
          else:
            print("You need a golden key to access the treasure chamber.")
        else:
          print("The golden door stands open, but the treasure chamber has been emptied.")

  if room.get("type") == "stairwell":
    if room.get("requires_mysterious_key"):
      if player_floor in mysterious_keys or player_floor in unlocked_floors:
        print("The stairwell is unlocked! Use 'descend' to go deeper.")
      else:
        print("The stairwell is locked. You need a mysterious key for this floor to proceed.")

  if room.get("enemy"):
    e = room["enemy"]
    tag = " [BOSS]" if e.get("is_boss") else ""
    if e.get("is_training_dummy"):
      tag = " [TRAINING]"
      # Show ??? for training dummy HP until defeated
      if "Training Dummy" not in discovered_enemies:
        print(f"Enemy here: {e['name']}{tag} (HP: ???)")
      else:
        print(f"Enemy here: {e['name']}{tag} (HP: {e['hp']})")
    else:
      print(f"Enemy here: {e['name']}{tag} (HP: {e['hp']})")

  if room.get("weapons"):
    print("Weapons here:")
    for i, w in enumerate(room["weapons"], 1):
      if w.get("name") == "Spell Book":
        print(f"  {i}. {w['name']} (Damage: ???, Durability: {w['durability']})")
      elif w.get("requires_mana"):
        print(f"  {i}. {w['name']} (Damage: {w['damage']}, Durability: {w['durability']}, Mana Cost: {w.get('mana_cost', 10)})")
      else:
        print(f"  {i}. {w['name']} (Damage: {w['damage']}, Durability: {w['durability']})")

  if room.get("armors"):
    print("Armor here:")
    for i, a in enumerate(room["armors"], 1):
      print(f"  {i}. {a['name']} (Defense: {a['defense']}, Durability: {a['durability']})")

  if room.get("mysterious_key"):
    key = room["mysterious_key"]
    if player_floor in mysterious_keys or player_floor in unlocked_floors:
      print(f"A {key['name']} lies here, but it's not useful to you.")
    else:
      print(f"A {key['name']} lies here. Use 'take_key' to pick it up.")

  if room.get("shop"):
    print("This is a shop. Type 'buy' to see what's for sale.")

  inv_names = [f"{w['name']}({w.get('durability', '-')})" for w in inventory if "damage" in w]
  if not inventory:
    print("Your inventory: Empty (using fists)")
  else:
    print("Your inventory:", inv_names)
  print(f"Your HP: {player_hp}/{player_max_hp} | Stamina: {player_stamina}/{player_max_stamina} | Mana: {player_mana}/{player_max_mana} | Gold: {player_money} | Health Potions: {player_potions} | Stamina Potions: {stamina_potions} | Mana Potions: {mana_potions} | Waypoint Scrolls: {waypoint_scrolls}")
  if mysterious_keys:
    floor_list = ", ".join([f"Floor {floor}" for floor in mysterious_keys.keys()])
    print(f"You have mysterious keys for: {floor_list}")
  if golden_keys > 0:
    print(f"You have {golden_keys} golden key(s)!")
  if equipped_armor:
    print(f"Equipped Armor: {equipped_armor['name']} (Defense: {equipped_armor['defense']}, Durability: {equipped_armor['durability']})")
  if spell_scrolls:
    scroll_list = ", ".join([f"{name} ({count})" for name, count in spell_scrolls.items()])
    print(f"Spell Scrolls: {scroll_list}")
  if learned_spells:
    spell_list = ", ".join([f"{i+1}.{name}" for i, name in enumerate(learned_spells)])
    print(f"Learned Spells: {spell_list}")
  print("Type 'help' to see a list of commands.")

def save_game():
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
    "spell_scrolls": spell_scrolls
  }
  with open(SAVE_FILE, "w") as f:
    json.dump(data, f)
  print("Game saved!")

def load_game():
  global player_floor, player_x, player_y, player_hp, player_max_hp, player_money, player_potions, waypoints, unlocked_floors, waypoint_scrolls, player_stamina, player_max_stamina, player_mana, player_max_mana, stamina_potions, mana_potions, discovered_enemies, learned_spells, spell_scrolls

  if not os.path.exists(SAVE_FILE):
    print("No saved game found.")
    return False

  with open(SAVE_FILE, "r") as f:
    data = json.load(f)

  # Handle old save format
  if "world" in data:
    # Convert old single-floor format to new multi-floor format
    worlds.clear()
    worlds[0] = {}
    for key, value in data["world"].items():
      x, y = map(int, key.split(","))
      worlds[0][(x, y)] = value
    player_floor = data.get("player_floor", 0)
  else:
    # New multi-floor format
    worlds.clear()
    for floor_str, world_data in data["worlds"].items():
      floor = int(floor_str)
      worlds[floor] = {}
      for key, value in world_data.items():
        x, y = map(int, key.split(","))
        worlds[floor][(x, y)] = value
    player_floor = data["player_floor"]
  
  player_x = data["player_x"]
  player_y = data["player_y"]
  inventory.clear()
  inventory.extend(data["inventory"])
  armor_inventory.clear()
  armor_inventory.extend(data["armor_inventory"])
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
    mysterious_keys.clear()
    mysterious_keys[0] = True  # Old saves get Floor 0 key
  else:
    mysterious_keys.clear()
    mysterious_keys.update(data.get("mysterious_keys", {}))
  
  golden_keys = data.get("golden_keys", 0)
  unlocked_floors.clear()
  unlocked_floors.update(data.get("unlocked_floors", []))
  
  # Handle old waypoint format
  old_waypoints = data.get("waypoints", {})
  if old_waypoints and isinstance(next(iter(old_waypoints.values())), tuple) and len(next(iter(old_waypoints.values()))) == 2:
    # Convert old (x, y) format to new (floor, x, y) format
    waypoints.clear()
    for name, (x, y) in old_waypoints.items():
      waypoints[name] = (0, x, y)
  else:
    waypoints.clear()
    waypoints.update(old_waypoints)
  
  discovered_enemies.clear()
  discovered_enemies.update(data.get("discovered_enemies", []))
  
  learned_spells = data.get("learned_spells", [])
  spell_scrolls = data.get("spell_scrolls", {})
  
  print("Game loaded!")
  return True

def show_bestiary():
  """Display information about discovered enemies in the game"""
  print("\n=== BESTIARY ===")
  
  if not discovered_enemies:
    print("You have no enemy info!")
    print("Defeat enemies to unlock their files in the bestiary.")
    print("==================")
    return
  
  # Regular enemies
  print("\n📖 Discovered Enemies:")
  for enemy_name in discovered_enemies:
    if enemy_name in enemy_stats:
      base_hp = enemy_stats[enemy_name]
      # Determine health category
      if base_hp <= 8:
        health_desc = "Very Low Health"
      elif base_hp <= 12:
        health_desc = "Low Health"
      elif base_hp <= 16:
        health_desc = "Average Health"
      elif base_hp <= 20:
        health_desc = "High Health"
      else:
        health_desc = "Very High Health"
      
      # Special descriptions for specific enemies
      if enemy_name == "Hungry Wolf":
        health_desc = "Low Health, High Attack"
      elif enemy_name == "Rat":
        health_desc = "Very Low Health, Easy Target"
      elif enemy_name == "Orc":
        health_desc = "High Health, Tough Opponent"
      
      print(f"  🐺 {enemy_name}: {base_hp} HP - {health_desc}")
    elif enemy_name == "Training Dummy":
      print("  🎯 Training Dummy: ??? HP - Practice Target (No Rewards)")
    elif enemy_name == "Troll":
      print("  👹 Troll: ??? HP - Boss Enemy (Drops Mysterious Key)")
  
  # Combat tips
  print("\n💡 Combat Tips:")
  print("  - Enemies scale with distance from (0,0) but cap at 100 rooms")
  print("  - Boss enemies can be escaped from by moving away")
  print("  - Regular enemies block your path until defeated")
  print("  - Hungry Wolves: Kill quickly due to high attack potential")
  print("  - Orcs: Tough opponents, use your best weapons")
  print("  - Rats: Easy targets, good for farming gold")
  
  print("==================")

def show_help():
  """Display help information organized by sections"""
  print("\n=== HELP SYSTEM ===")
  print("Type 'guide' followed by a section name to view specific help:")
  print("  guide combat     - Combat commands and tips")
  print("  guide movement   - Movement and exploration")
  print("  guide items      - Weapons, armor, and inventory")
  print("  guide resources  - Potions, crystals, and resources")
  print("  guide progression - Keys, floors, and progression")
  print("  guide utility    - Map, waypoints, save/load")
  print("  guide all        - Show all commands")
  print("==================")

def show_combat_help():
  """Display combat-related help"""
  print("\n=== COMBAT HELP ===")
  print("Commands:")
  print("  attack - Attack an enemy")
  print("  run - Run away from an enemy (costs 10 stamina)")
  print("\nCombat Tips:")
  print("  - All weapons have a 5% chance to land critical hits (2x damage)")
  print("  - Daggers have 20% crit chance and deal 2.6x damage on crits")
  print("  - Magic staffs require mana to use but deal extra damage")
  print("  - Boss enemies can be escaped from by moving away")
  print("  - Regular enemies block your path until defeated")
  print("  - Hungry Wolves: Kill quickly due to high attack potential")
  print("  - Orcs: Tough opponents, use your best weapons")
  print("  - Rats: Easy targets, good for farming gold")
  print("==================")

def show_movement_help():
  """Display movement-related help"""
  print("\n=== MOVEMENT HELP ===")
  print("Commands:")
  print("  north/south/east/west - Move in that direction")
  print("  descend - Use stairwell to go deeper")
  print("\nMovement Tips:")
  print("  - You can escape from boss enemies by moving away")
  print("  - Regular enemies will block your path until defeated")
  print("  - Training dummy at (0,0) on Floor 0 can be moved past freely")
  print("  - Each floor has its own world to explore")
  print("==================")

def show_items_help():
  """Display item-related help"""
  print("\n=== ITEMS HELP ===")
  print("Commands:")
  print("  take - Pick up weapons or armor")
  print("  drop - Drop a weapon")
  print("  drop_armor - Drop armor")
  print("  switch - Switch between weapons (includes fists option)")
  print("  equip - Equip armor")
  print("  inventory - Show your weapons")
  print("  armor - Show your armor")
  print("  use_scroll - Learn spells from scrolls")
  print("\nItem Tips:")
  print("  - Weapons and armor have durability that decreases with use")
  print("  - Items and enemies scale with distance from (0,0) but cap at 100 rooms away")
  print("  - Floor 0 gear caps at ~25 damage and ~40 durability")
  print("  - To find better gear, you must descend to higher floors")
  print("  - Use 'inventory' to see your weapons and 'armor' to see armor")
  print("  - Spell Books can cast learned spells (buy scrolls from shops)")
  print("  - Use 'switch' to select fists (option 0) if you have no spells for Spell Book")
  print("==================")

def show_resources_help():
  """Display resource-related help"""
  print("\n=== RESOURCES HELP ===")
  print("Commands:")
  print("  absorb - Use a life/stamina/mana crystal")
  print("  use - Use health, stamina, or mana potions")
  print("\nResource Tips:")
  print("  - Health potions restore 30 HP")
  print("  - Stamina potions restore 10 stamina")
  print("  - Mana potions restore 15 mana")
  print("  - Life crystals: +10 max HP, +20 current HP")
  print("  - Stamina crystals: +10 max stamina, +10 current stamina")
  print("  - Mana crystals: +10 max mana, +10 current mana")
  print("  - Crystal rooms can have single, dual, or triple crystals")
  print("==================")

def show_progression_help():
  """Display progression-related help"""
  print("\n=== PROGRESSION HELP ===")
  print("Commands:")
  print("  take_key - Pick up a mysterious key")
  print("  drop_mysterious_key - Drop your mysterious key")
  print("  open - Open a chest")
  print("  loot - Loot treasure chambers")
  print("  buy - Buy from a shop")
  print("\nProgression Tips:")
  print("  - Mysterious keys are floor-specific and unlock stairwells permanently")
  print("  - Bosses drop mysterious keys for their specific floor")
  print("  - Golden keys (max 3) are needed to loot treasure chambers")
  print("  - Golden keys can be bought from shops for 50 gold")
  print("  - Treasure chambers contain gold, potions, and mysterious keys")
  print("  - Stairwell rooms (1 in 25) require mysterious keys to descend")
  print("==================")

def show_utility_help():
  """Display utility command help"""
  print("\n=== UTILITY HELP ===")
  print("Commands:")
  print("  map - Show map and waypoints")
  print("  waypoint - Add a waypoint")
  print("  view - View waypoint details")
  print("  delete - Delete a waypoint")
  print("  teleport - Use waypoint scroll to teleport to a waypoint")
  print("  bestiary - Show information about enemies")
  print("  save - Save the game")
  print("  load - Load your saved game")
  print("  guide - Show this help system")
  print("  quit - Exit the game")
  print("\nUtility Tips:")
  print("  - Use waypoints to mark important locations (max 10)")
  print("  - Waypoint scrolls can teleport you to any waypoint, even during combat")
  print("  - Waypoint scrolls can be bought from shops for 40 gold (max 3)")
  print("  - The training dummy at (0,0) on Floor 0 can be attacked without losing durability")
  print("==================")

def show_all_help():
  """Display all commands"""
  print("\n=== ALL COMMANDS ===")
  print("Combat:")
  print("  attack, run")
  print("Movement:")
  print("  north/south/east/west, descend")
  print("Items:")
  print("  take, drop, drop_armor, switch, equip, inventory, armor, use_scroll")
  print("Resources:")
  print("  absorb, use")
  print("Progression:")
  print("  take_key, drop_mysterious_key, open, loot, buy")
  print("Utility:")
  print("  map, waypoint, view, delete, teleport, bestiary, save, load, guide, quit")
  print("==================")
# --- Start game ---
print("Welcome to the Adventure Game!")
print("Type 'guide' to see available info on how to play!")

if os.path.exists(SAVE_FILE):
  answer = input("Load previous save? (yes/no/delete): ").lower()
  if answer == "yes":
    load_game()
  elif answer == "delete":
    confirm = input("Are you sure you want to delete the save file? (yes/no): ").lower()
    if confirm == "yes":
      os.remove(SAVE_FILE)
      print("Save file deleted!")
    else:
      print("Save file deletion cancelled.")

# Don't show help automatically - let players discover it

while True:
  current_room = get_room(player_floor, player_x, player_y)
  show_room(current_room)

  command = input("\nWhat do you do? ").lower().strip()

  if command == "quit":
    print("Game over!")
    break

  elif command in ["north", "south", "east", "west"]:
    if current_room.get("enemy"):
      enemy = current_room["enemy"]
      if enemy.get("is_boss"):
        print(f"The {enemy['name']} is too powerful! You manage to escape!")
        if command == "north": player_y += 1
        elif command == "south": player_y -= 1
        elif command == "east": player_x += 1
        elif command == "west": player_x -= 1
      elif enemy.get("is_training_dummy"):
        print(f"You can move freely past the {enemy['name']}.")
        if command == "north": player_y += 1
        elif command == "south": player_y -= 1
        elif command == "east": player_x += 1
        elif command == "west": player_x -= 1
      else:
        print(f"You can't leave! The {enemy['name']} blocks your way!")
    else:
      if command == "north": player_y += 1
      elif command == "south": player_y -= 1
      elif command == "east": player_x += 1
      elif command == "west": player_x -= 1

  elif command == "guide":
    show_help()
  elif command.startswith("guide "):
    section = command[6:].lower().strip()
    if section == "combat":
      show_combat_help()
    elif section == "movement":
      show_movement_help()
    elif section == "items":
      show_items_help()
    elif section == "resources":
      show_resources_help()
    elif section == "progression":
      show_progression_help()
    elif section == "utility":
      show_utility_help()
    elif section == "all":
      show_all_help()
    else:
      print(f"Unknown guide section: '{section}'")
      print("Available sections: combat, movement, items, resources, progression, utility, all")
    show_help()

  elif command == "save":
    save_game()

  elif command == "load":
    load_game()

  # All your core command handlers:
  elif command == "attack":
    if current_room.get("enemy"):
      enemy = current_room["enemy"]
      
      # Use fists if no weapons available, otherwise use first weapon
      if not inventory:
        # Use fists (3 damage, infinite durability)
        damage = 3
        weapon_name = "fists"
        
        # Check for critical hits (fists can crit too!)
        crit_chance = 0.05  # Base 5% crit chance
        crit_multiplier = 2.0  # Base 2x damage
        
        # Roll for critical hit
        if random.random() < crit_chance:
          original_damage = damage
          damage = int(damage * crit_multiplier)
          print(f"*** CRITICAL HIT! *** Your fists strike true! {original_damage} → {damage} damage!")
        else:
          print(f"You attack the {enemy['name']} with your {weapon_name} for {damage} damage!")
      else:
        # Use the first weapon in inventory
        weapon = inventory[0]
        weapon_name = weapon["name"]
        
        # Special handling for Spell Book
        if weapon_name == "Spell Book":
          if not learned_spells:
            print("You have a Spell Book but don't know any spells!")
            print("Buy spell scrolls from shops and use 'use_scroll' to learn them.")
            continue
          
          print("Which spell do you want to cast?")
          for i, spell_name in enumerate(learned_spells, 1):
            spell = spells[spell_name]
            print(f"  {i}. {spell_name} - {spell['mana_cost']} mana: {spell['description']}")
          
          try:
            choice = int(input("Enter number: ")) - 1
            if 0 <= choice < len(learned_spells):
              spell_name = learned_spells[choice]
              spell = spells[spell_name]
              
              # Check mana
              if player_mana < spell["mana_cost"]:
                print(f"You need {spell['mana_cost']} mana to cast {spell_name}, but you only have {player_mana} mana!")
                continue
              
              # Cast spell
              player_mana -= spell["mana_cost"]
              damage = spell["damage"]
              
              print(f"You cast {spell_name} for {damage} damage! (Mana used: {spell['mana_cost']})")
              
              # Apply spell effects
              if spell.get("effect"):
                if spell["effect"] in ["Burning", "Poisoned"]:
                  enemy[spell["effect"]] = {
                    "damage": spell["effect_damage"],
                    "duration": spell["effect_duration"]
                  }
                  print(f"The {enemy['name']} is {spell['effect']}!")
                elif spell["effect"] == "Stunned":
                  enemy["Stunned"] = spell["effect_duration"]
                  print(f"The {enemy['name']} is Stunned!")
            else:
              print("Invalid choice.")
              continue
          except ValueError:
            print("Please enter a valid number.")
            continue
        else:
          # Regular weapon attack
          damage = weapon["damage"]
          
          # Check if weapon requires mana (staff)
          if weapon.get("requires_mana"):
            mana_cost = weapon.get("mana_cost", 10)
            if player_mana < mana_cost:
              print(f"You need {mana_cost} mana to use the {weapon_name}, but you only have {player_mana} mana!")
              print("You can't attack with this weapon.")
              continue
            else:
              player_mana -= mana_cost
          
          # Check for critical hits
          crit_chance = 0.05  # Base 5% crit chance
          crit_multiplier = 2.0  # Base 2x damage
          
          # Daggers get bonus crit chance and damage
          if weapon_name == "Dagger":
            crit_chance += 0.15  # +15% chance (total 20%)
            crit_multiplier = 2.6  # 2.6x damage
          
          # Roll for critical hit
          if random.random() < crit_chance:
            original_damage = damage
            damage = int(damage * crit_multiplier)
            if weapon_name == "Dagger":
              print(f"*** CRITICAL HIT! *** Your dagger strikes true! {original_damage} → {damage} damage!")
            else:
              print(f"*** CRITICAL HIT! *** {original_damage} → {damage} damage!")
          else:
            # Normal attack message
            if weapon.get("requires_mana"):
              print(f"You attack the {enemy['name']} with your {weapon_name} for {damage} damage! (Mana used: {mana_cost})")
            else:
              print(f"You attack the {enemy['name']} with your {weapon_name} for {damage} damage!")
          
          # Reduce weapon durability (except for training dummy)
          if not enemy.get("is_training_dummy"):
            weapon["durability"] -= 1
            if weapon["durability"] <= 0:
              print(f"Your {weapon['name']} breaks!")
              inventory.pop(0)
          else:
            print("Your weapon doesn't lose durability against the training dummy.")
      
      # Deal damage to enemy
      enemy["hp"] -= damage
      
      # Check if enemy is defeated
      if enemy["hp"] <= 0:
        if enemy.get("is_training_dummy"):
          print("Congrats! You wasted your time...")
        else:
          print(f"You defeated the {enemy['name']}!")
        
        # Add enemy to discovered enemies and show unlock message
        if enemy["name"] not in discovered_enemies:
          discovered_enemies.add(enemy["name"])
          print(f"{enemy['name']}'s File Unlocked!")
        
        # Boss drops mysterious key for current floor
        if enemy.get("is_boss"):
          if player_floor not in mysterious_keys:
            mysterious_keys[player_floor] = True
            print(f"The boss drops a mysterious key for Floor {player_floor}!")
          else:
            print(f"The boss drops a mysterious key for Floor {player_floor}, but you already have one!")
        else:
          # Regular enemy drops money (but not training dummy)
          if not enemy.get("is_training_dummy"):
            money_drop = random.randint(5, 15)
            player_money += money_drop
            print(f"You found {money_drop} gold!")
        
        current_room["enemy"] = None
      else:
        # Don't show HP remaining for training dummy
        if not enemy.get("is_training_dummy"):
          print(f"The {enemy['name']} has {enemy['hp']} HP remaining.")
        # Enemy counter-attack (but not training dummy)
        if not enemy.get("is_training_dummy"):
          # Apply status effects first
          if enemy.get("Burning"):
            burn_damage = enemy["Burning"]["damage"]
            enemy["hp"] -= burn_damage
            enemy["Burning"]["duration"] -= 1
            print(f"The {enemy['name']} takes {burn_damage} burning damage!")
            if enemy["Burning"]["duration"] <= 0:
              del enemy["Burning"]
              print(f"The {enemy['name']} is no longer burning.")
          
          if enemy.get("Poisoned"):
            poison_damage = enemy["Poisoned"]["damage"]
            enemy["hp"] -= poison_damage
            enemy["Poisoned"]["duration"] -= 1
            print(f"The {enemy['name']} takes {poison_damage} poison damage!")
            if enemy["Poisoned"]["duration"] <= 0:
              del enemy["Poisoned"]
              print(f"The {enemy['name']} is no longer poisoned.")
          
          # Check if enemy died from status effects
          if enemy["hp"] <= 0:
            print(f"The {enemy['name']} dies from the effects!")
            if enemy["name"] not in discovered_enemies:
              discovered_enemies.add(enemy["name"])
              print(f"{enemy['name']}'s File Unlocked!")
            if not enemy.get("is_training_dummy"):
              money_drop = random.randint(5, 15)
              player_money += money_drop
              print(f"You found {money_drop} gold!")
            current_room["enemy"] = None
            continue
          
          # Enemy attack (unless stunned)
          if enemy.get("Stunned"):
            print(f"The {enemy['name']} is stunned and can't attack!")
            enemy["Stunned"] -= 1
            if enemy["Stunned"] <= 0:
              del enemy["Stunned"]
          else:
            enemy_damage = enemy["base_attack"]
            if equipped_armor:
              # Balanced flat damage reduction: defense divided by 2 (rounded down)
              # This makes armor more balanced and less overpowered
              damage_reduction = equipped_armor["defense"] // 2
              # Apply armor piercing: enemies can ignore some armor
              armor_pierce = enemy.get("armor_pierce", 0)
              effective_reduction = max(0, damage_reduction - armor_pierce)
              enemy_damage = max(1, enemy_damage - effective_reduction)
              # Reduce armor durability
              equipped_armor["durability"] -= 1
              if equipped_armor["durability"] <= 0:
                print(f"Your {equipped_armor['name']} breaks!")
                equipped_armor = None
            
            player_hp -= enemy_damage
            print(f"The {enemy['name']} attacks you for {enemy_damage} damage!")
            print(f"You have {player_hp} HP remaining.")
            
            if player_hp <= 0:
              print("You have been defeated!")
              break
        else:
          print("The training dummy doesn't fight back.")
    else:
      print("There's no enemy here to attack.")
      
  elif command == "take":
    # Check if there are weapons or armor to take
    has_weapons = current_room.get("weapons")
    has_armors = current_room.get("armors")
    
    if not has_weapons and not has_armors:
      print("There's nothing here to take.")
      continue
    
    # Show available items
    available_items = []
    if has_weapons:
      for weapon in current_room["weapons"]:
        available_items.append(("weapon", weapon))
    if has_armors:
      for armor in current_room["armors"]:
        available_items.append(("armor", armor))
    
    if len(available_items) == 1:
      # Only one item, take it automatically
      item_type, item = available_items[0]
      if item_type == "weapon":
        if len(inventory) >= MAX_WEAPONS:
          print("Your weapon inventory is full! Drop a weapon first.")
          continue
        inventory.append(item)
        current_room["weapons"].remove(item)
        print(f"You picked up the {item['name']}!")
      else:  # armor
        if len(armor_inventory) >= MAX_ARMOR:
          print("Your armor inventory is full! Drop some armor first.")
          continue
        armor_inventory.append(item)
        current_room["armors"].remove(item)
        print(f"You picked up the {item['name']}!")
    else:
      # Multiple items, let player choose
      print("What do you want to take?")
      for i, (item_type, item) in enumerate(available_items, 1):
        if item_type == "weapon":
          if item.get("requires_mana"):
            print(f"  {i}. {item['name']} (Weapon - Damage: {item['damage']}, Durability: {item['durability']}, Mana Cost: {item.get('mana_cost', 10)})")
          else:
            print(f"  {i}. {item['name']} (Weapon - Damage: {item['damage']}, Durability: {item['durability']})")
        else:  # armor
          print(f"  {i}. {item['name']} (Armor - Defense: {item['defense']}, Durability: {item['durability']})")
      
      try:
        choice = int(input("Enter number: ")) - 1
        if 0 <= choice < len(available_items):
          item_type, item = available_items[choice]
          if item_type == "weapon":
            if len(inventory) >= MAX_WEAPONS:
              print("Your weapon inventory is full! Drop a weapon first.")
              continue
            inventory.append(item)
            current_room["weapons"].remove(item)
            print(f"You picked up the {item['name']}!")
          else:  # armor
            if len(armor_inventory) >= MAX_ARMOR:
              print("Your armor inventory is full! Drop some armor first.")
              continue
            armor_inventory.append(item)
            current_room["armors"].remove(item)
            print(f"You picked up the {item['name']}!")
        else:
          print("Invalid choice.")
      except ValueError:
        print("Please enter a valid number.")
      

      
  elif command == "inventory":
    if inventory:
      print("\nYour weapons:")
      for i, weapon in enumerate(inventory):
        if weapon.get("name") == "Spell Book":
          print(f"  {i+1}. {weapon['name']} (Damage: ???, Durability: {weapon['durability']})")
        elif weapon.get("requires_mana"):
          print(f"  {i+1}. {weapon['name']} (Damage: {weapon['damage']}, Durability: {weapon['durability']}, Mana Cost: {weapon.get('mana_cost', 10)})")
        else:
          print(f"  {i+1}. {weapon['name']} (Damage: {weapon['damage']}, Durability: {weapon['durability']})")
    else:
      print("You have no weapons.")
      print("Currently using: Fists (Damage: 3, Durability: Infinite)")
      
  elif command == "armor":
    if armor_inventory:
      print("\nYour armor:")
      for i, armor in enumerate(armor_inventory):
        print(f"  {i+1}. {armor['name']} (Defense: {armor['defense']}, Durability: {armor['durability']})")
    else:
      print("You have no armor.")
    if equipped_armor:
      print(f"Equipped: {equipped_armor['name']} (Defense: {equipped_armor['defense']}, Durability: {equipped_armor['durability']})")
      
  elif command == "drop":
    if not inventory:
      print("You have no weapons to drop.")
    else:
      print("Which weapon do you want to drop?")
      for i, weapon in enumerate(inventory):
        if weapon.get("name") == "Spell Book":
          print(f"  {i+1}. {weapon['name']} (Damage: ???, Durability: {weapon['durability']})")
        elif weapon.get("requires_mana"):
          print(f"  {i+1}. {weapon['name']} (Damage: {weapon['damage']}, Durability: {weapon['durability']}, Mana Cost: {weapon.get('mana_cost', 10)})")
        else:
          print(f"  {i+1}. {weapon['name']} (Damage: {weapon['damage']}, Durability: {weapon['durability']})")
      try:
        choice = int(input("Enter number: ")) - 1
        if 0 <= choice < len(inventory):
          dropped_weapon = inventory.pop(choice)
          # Check if this was the currently held weapon (first in inventory)
          if choice == 0:
            print(f"You dropped your currently held weapon: {dropped_weapon['name']}")
            if inventory:
              print(f"You are now holding: {inventory[0]['name']}")
            else:
              print("You are now holding no weapon (using fists).")
          else:
            print(f"You dropped the {dropped_weapon['name']}.")
          # Initialize weapons list if it doesn't exist
          if "weapons" not in current_room:
            current_room["weapons"] = []
          current_room["weapons"].append(dropped_weapon)
        else:
          print("Invalid choice.")
      except ValueError:
        print("Please enter a valid number.")
        
  elif command == "drop_armor":
    if not armor_inventory:
      print("You have no armor to drop.")
    else:
      print("Which armor do you want to drop?")
      for i, armor in enumerate(armor_inventory):
        print(f"  {i+1}. {armor['name']} (Defense: {armor['defense']}, Durability: {armor['durability']})")
      try:
        choice = int(input("Enter number: ")) - 1
        if 0 <= choice < len(armor_inventory):
          dropped_armor = armor_inventory.pop(choice)
          # Unequip if this was the equipped armor
          if equipped_armor and equipped_armor == dropped_armor:
            equipped_armor = None
            print(f"You unequipped and dropped your equipped armor: {dropped_armor['name']}")
            print("You are now wearing no armor.")
          else:
            print(f"You dropped the {dropped_armor['name']}.")
          # Initialize armors list if it doesn't exist
          if "armors" not in current_room:
            current_room["armors"] = []
          current_room["armors"].append(dropped_armor)
        else:
          print("Invalid choice.")
      except ValueError:
        print("Please enter a valid number.")
        
  elif command == "equip":
    if not armor_inventory:
      print("You have no armor to equip.")
    else:
      print("Which armor do you want to equip?")
      for i, armor in enumerate(armor_inventory):
        print(f"  {i+1}. {armor['name']} (Defense: {armor['defense']}, Durability: {armor['durability']})")
      try:
        choice = int(input("Enter number: ")) - 1
        if 0 <= choice < len(armor_inventory):
          equipped_armor = armor_inventory[choice]
          print(f"You equipped the {equipped_armor['name']}!")
        else:
          print("Invalid choice.")
      except ValueError:
        print("Please enter a valid number.")
        
  elif command == "switch":
    print("Which weapon do you want to use?")
    print("  0. Fists (Damage: 3, Durability: Infinite)")
    for i, weapon in enumerate(inventory):
      if weapon.get("name") == "Spell Book":
        print(f"  {i+1}. {weapon['name']} (Damage: ???, Durability: {weapon['durability']})")
      elif weapon.get("requires_mana"):
        print(f"  {i+1}. {weapon['name']} (Damage: {weapon['damage']}, Durability: {weapon['durability']}, Mana Cost: {weapon.get('mana_cost', 10)})")
      else:
        print(f"  {i+1}. {weapon['name']} (Damage: {weapon['damage']}, Durability: {weapon['durability']})")
    try:
      choice = int(input("Enter number: ")) - 1
      if choice == -1:
        # Switch to fists - move all weapons to inventory
        if inventory:
          print("You switch to using your fists.")
          # Move current weapon to back of inventory
          if inventory:
            weapon = inventory.pop(0)
            inventory.append(weapon)
        else:
          print("You're already using your fists.")
      elif 0 <= choice < len(inventory):
        # Move selected weapon to front of inventory
        weapon = inventory.pop(choice)
        inventory.insert(0, weapon)
        print(f"You switched to {weapon['name']}.")
      else:
        print("Invalid choice.")
    except ValueError:
      print("Please enter a valid number.")
      
  elif command == "absorb":
    if current_room.get("crystal_type") == "life":
      player_max_hp += 10
      player_hp = min(player_hp + 20, player_max_hp)
      print("You absorb the life crystal! +10 max HP, +20 current HP")
      current_room["crystal_type"] = None
    elif current_room.get("crystal_type") == "stamina":
      player_stamina = min(player_stamina + 10, player_max_stamina)  # Cap at max stamina
      print("You absorb the stamina crystal! +10 stamina")
      current_room["crystal_type"] = None
    elif current_room.get("crystal_type") == "mana":
      player_max_mana = min(player_max_mana + 10, 200)  # Cap at 200 max mana
      player_mana = min(player_mana + 10, player_max_mana)  # Cap at max mana
      print("You absorb the mana crystal! +10 max mana, +10 current mana")
      current_room["crystal_type"] = None
    elif current_room.get("crystal_type") == "life_stamina":
      player_max_hp += 10
      player_hp = min(player_hp + 20, player_max_hp)
      player_stamina = min(player_stamina + 10, player_max_stamina)  # Cap at max stamina
      print("You absorb both crystals! +10 max HP, +20 current HP, +10 stamina")
      current_room["crystal_type"] = None
    elif current_room.get("crystal_type") == "life_mana":
      player_max_hp += 10
      player_hp = min(player_hp + 20, player_max_hp)
      player_max_mana = min(player_max_mana + 10, 200)  # Cap at 200 max mana
      player_mana = min(player_mana + 10, player_max_mana)  # Cap at max mana
      print("You absorb both crystals! +10 max HP, +20 current HP, +10 max mana, +10 current mana")
      current_room["crystal_type"] = None
    elif current_room.get("crystal_type") == "all":
      player_max_hp += 10
      player_hp = min(player_hp + 20, player_max_hp)
      player_stamina = min(player_stamina + 10, player_max_stamina)  # Cap at max stamina
      player_max_mana = min(player_max_mana + 10, 200)  # Cap at 200 max mana
      player_mana = min(player_mana + 10, player_max_mana)  # Cap at max mana
      print("You absorb all crystals! +10 max HP, +20 current HP, +10 stamina, +10 max mana, +10 current mana")
      current_room["crystal_type"] = None
    else:
      print("There's no crystal here to absorb.")
      
  elif command == "open":
    if current_room.get("type") == "chest" and current_room.get("chest"):
      chest = current_room["chest"]
      if chest["locked"]:
        print("The chest is locked. You need a golden key to open it.")
      else:
        print("The chest is already open.")
    else:
      print("There's no chest here to open.")
      
  elif command == "buy":
    if current_room.get("type") == "shop" and current_room.get("shop"):
      shop = current_room["shop"]
      
      # Check if shop has any items
      has_items = (len(shop["items"]) > 0 or 
                   shop.get("armor") or 
                   shop.get("has_key") or 
                   shop.get("life_crystal") or 
                   shop.get("stamina_potions", 0) > 0 or 
                   shop.get("mana_potions", 0) > 0 or 
                   shop.get("waypoint_scrolls", 0) > 0)
      
      if not has_items:
        print("The shop is empty and closed.")
        continue
      
      print("\nShop inventory:")
      for i, item in enumerate(shop["items"]):
        print(f"  {i+1}. {item['name']} (Damage: {item['damage']}, Durability: {item['durability']}) - {item['cost']} gold")
      if shop.get("armor"):
        armor = shop["armor"]
        print(f"  R. {armor['name']} (Defense: {armor['defense']}, Durability: {armor['durability']}) - 20 gold")
      print(f"  P. Health Potion - {shop['potion_price']} gold")
      if shop.get("stamina_potions", 0) > 0:
        print(f"  S. Stamina Potion - {shop['stamina_potion_price']} gold ({shop['stamina_potions']} available)")
      if shop.get("mana_potions", 0) > 0:
        print(f"  M. Mana Potion - {shop['mana_potion_price']} gold ({shop['mana_potions']} available)")
      if shop.get("has_key"):
        print("  K. Golden Key - 50 gold")
      if shop.get("life_crystal"):
        print("  L. Life Crystal - 30 gold")
      if shop.get("waypoint_scrolls") > 0:
        print(f"  W. Waypoint Scroll - 40 gold ({shop['waypoint_scrolls']} available)")
      
      # Show spell scrolls
      if shop.get("spell_scrolls"):
        print("Spell Scrolls:")
        for i, (spell_name, count) in enumerate(shop["spell_scrolls"].items()):
          price = random.randint(40, 80)
          print(f"  {chr(65 + i)}. {spell_name} Scroll - {price} gold ({count} available)")
      
      choice = input("What would you like to buy? (or 'cancel'): ").strip()
      
      if choice == "cancel":
        print("You leave the shop.")
      elif choice.lower() == "p":
        if player_money >= shop["potion_price"]:
          player_money -= shop["potion_price"]
          player_potions += 1
          print("You bought a health potion!")
        else:
          print("You don't have enough gold.")
      elif choice.lower() == "s" and shop.get("stamina_potions", 0) > 0:
        if player_money >= shop["stamina_potion_price"]:
          player_money -= shop["stamina_potion_price"]
          stamina_potions += 1
          shop["stamina_potions"] -= 1
          print("You bought a stamina potion!")
        else:
          print("You don't have enough gold.")
      elif choice.lower() == "m" and shop.get("mana_potions", 0) > 0:
        if player_money >= shop["mana_potion_price"]:
          player_money -= shop["mana_potion_price"]
          mana_potions += 1
          shop["mana_potions"] -= 1
          print("You bought a mana potion!")
        else:
          print("You don't have enough gold.")
      elif choice.lower() == "k" and shop.get("has_key"):
        if player_money >= 50:
          if golden_keys < 3:
            player_money -= 50
            golden_keys += 1
            shop["has_key"] = False  # Remove the key from shop
            print(f"You bought a golden key! (You now have {golden_keys})")
          else:
            print("You can only carry 3 golden keys maximum!")
        else:
          print("You don't have enough gold.")
      elif choice.lower() == "l" and shop.get("life_crystal"):
        if player_money >= 30:
          player_money -= 30
          player_max_hp += 10
          player_hp = min(player_hp + 20, player_max_hp)
          shop["life_crystal"] = False  # Remove the crystal from shop
          print("You bought and absorbed a life crystal! +10 max HP, +20 current HP")
        else:
          print("You don't have enough gold.")
      elif choice.lower() == "w" and shop.get("waypoint_scrolls") > 0:
        if player_money >= 40:
          if waypoint_scrolls < 3:
            player_money -= 40
            waypoint_scrolls += 1
            shop["waypoint_scrolls"] -= 1
            print("You bought a waypoint scroll!")
          else:
            print("You can only carry 3 waypoint scrolls maximum!")
        else:
          print("You don't have enough gold.")
      elif choice.isdigit():
        # Regular weapon purchase
        item_index = int(choice) - 1
        if 0 <= item_index < len(shop["items"]):
          item = shop["items"][item_index]
          if player_money >= item["cost"]:
            if len(inventory) < MAX_WEAPONS:
              player_money -= item["cost"]
              inventory.append(item)
              shop["items"].pop(item_index)
              print(f"You bought the {item['name']}!")
            else:
              print("Your weapon inventory is full!")
          else:
            print("You don't have enough gold.")
        else:
          print("Invalid choice.")
      elif len(choice) == 1 and choice.isalpha():
        # Check if it's a spell scroll (A, B, C, etc.)
        spell_list = list(shop.get("spell_scrolls", {}).items())
        spell_index = ord(choice.upper()) - ord('A')
        if 0 <= spell_index < len(spell_list):
          spell_name, count = spell_list[spell_index]
          price = random.randint(40, 80)
          if player_money >= price:
            player_money -= price
            spell_scrolls[spell_name] = spell_scrolls.get(spell_name, 0) + 1
            shop["spell_scrolls"][spell_name] -= 1
            if shop["spell_scrolls"][spell_name] <= 0:
              del shop["spell_scrolls"][spell_name]
            print(f"You bought a {spell_name} scroll!")
          else:
            print("You don't have enough gold.")
        else:
          print("Invalid choice.")
      elif choice.lower() == "r" and shop.get("armor"):
        if player_money >= 20:
          if len(armor_inventory) < MAX_ARMOR:
            player_money -= 20
            armor_inventory.append(shop["armor"])
            print(f"You bought the {shop['armor']['name']}!")
            shop["armor"] = None
          else:
            print("Your armor inventory is full!")
        else:
          print("You don't have enough gold.")
      else:
        print("Invalid choice.")
    else:
      print("There's no shop here.")
      
  elif command == "use":
    # Check what potions are available
    available_potions = []
    if player_potions > 0:
      available_potions.append(("health", player_potions))
    if stamina_potions > 0:
      available_potions.append(("stamina", stamina_potions))
    if mana_potions > 0:
      available_potions.append(("mana", mana_potions))
    
    if not available_potions:
      print("You don't have any potions to use.")
      continue
    
    if len(available_potions) == 1:
      # Only one type of potion, use it automatically
      potion_type, count = available_potions[0]
      if potion_type == "health":
        heal_amount = 30
        old_hp = player_hp
        player_hp = min(player_hp + heal_amount, player_max_hp)
        player_potions -= 1
        actual_heal = player_hp - old_hp
        print(f"You use a health potion and recover {actual_heal} HP!")
        print(f"You now have {player_hp}/{player_max_hp} HP and {player_potions} health potions remaining.")
      elif potion_type == "stamina":
        old_stamina = player_stamina
        player_stamina = min(player_stamina + 10, player_max_stamina)  # Cap at max stamina
        stamina_potions -= 1
        actual_regen = player_stamina - old_stamina
        print(f"You use a stamina potion and recover {actual_regen} stamina!")
        print(f"You now have {player_stamina}/{player_max_stamina} stamina and {stamina_potions} stamina potions remaining.")
      else:  # mana
        old_mana = player_mana
        player_mana = min(player_mana + 15, player_max_mana)  # Cap at max mana
        mana_potions -= 1
        actual_regen = player_mana - old_mana
        print(f"You use a mana potion and recover {actual_regen} mana!")
        print(f"You now have {player_mana}/{player_max_mana} mana and {mana_potions} mana potions remaining.")
    else:
      # Multiple potion types, let player choose
      print("Which potion do you want to use?")
      for i, (potion_type, count) in enumerate(available_potions, 1):
        if potion_type == "health":
          print(f"  {i}. Health Potion ({count} available)")
        elif potion_type == "stamina":
          print(f"  {i}. Stamina Potion ({count} available)")
        else:  # mana
          print(f"  {i}. Mana Potion ({count} available)")
      
      try:
        choice = int(input("Enter number: ")) - 1
        if 0 <= choice < len(available_potions):
          potion_type, count = available_potions[choice]
          if potion_type == "health":
            heal_amount = 30
            old_hp = player_hp
            player_hp = min(player_hp + heal_amount, player_max_hp)
            player_potions -= 1
            actual_heal = player_hp - old_hp
            print(f"You use a health potion and recover {actual_heal} HP!")
            print(f"You now have {player_hp}/{player_max_hp} HP and {player_potions} health potions remaining.")
          elif potion_type == "stamina":
            old_stamina = player_stamina
            player_stamina = min(player_stamina + 10, player_max_stamina)  # Cap at max stamina
            stamina_potions -= 1
            actual_regen = player_stamina - old_stamina
            print(f"You use a stamina potion and recover {actual_regen} stamina!")
            print(f"You now have {player_stamina}/{player_max_stamina} stamina and {stamina_potions} stamina potions remaining.")
          else:  # mana
            old_mana = player_mana
            player_mana = min(player_mana + 15, player_max_mana)  # Cap at max mana
            mana_potions -= 1
            actual_regen = player_mana - old_mana
            print(f"You use a mana potion and recover {actual_regen} mana!")
            print(f"You now have {player_mana}/{player_max_mana} mana and {mana_potions} mana potions remaining.")
        else:
          print("Invalid choice.")
      except ValueError:
        print("Please enter a valid number.")
      
  elif command == "map":
    show_map()
    
  elif command == "waypoint":
    add_waypoint()
    
  elif command == "view":
    view_waypoint()
    
  elif command == "delete":
    delete_waypoint()
    
  elif command == "descend":
    if current_room.get("type") == "stairwell" and current_room.get("requires_mysterious_key"):
      if player_floor in mysterious_keys or player_floor in unlocked_floors:
        # Use mysterious key if player has one for this floor
        if player_floor in mysterious_keys:
          del mysterious_keys[player_floor]
          unlocked_floors.add(player_floor)
          print(f"You use your mysterious key for Floor {player_floor} to unlock the stairwell!")
          print("The key dissolves into the lock, permanently unlocking this floor's stairwells.")
          
          # Remove any mysterious keys from this floor's rooms since they're no longer useful
          if player_floor in worlds:
            for room in worlds[player_floor].values():
              if room.get("mysterious_key"):
                room["mysterious_key"] = None
        
        # Descend to next floor
        player_floor += 1
        player_x = 0
        player_y = 0
        print(f"You descend to Floor {player_floor}!")
      else:
        print(f"You need a mysterious key for Floor {player_floor} to unlock this stairwell!")
    else:
      print("There's no stairwell here to descend.")

  elif command == "loot":
    if current_room.get("type") == "key_door" and not current_room.get("enemy") and not current_room.get("treasure_looted"):
      if golden_keys <= 0:
        print("You need a golden key to access the treasure chamber!")
        print("You can buy one from shops for 50 gold.")
      else:
        # Boss room treasure rewards
        gold_reward = 60
        potion_reward = random.randint(2, 4)
        
        player_money += gold_reward
        player_potions += potion_reward
        
        print(f"You use your golden key to unlock the treasure chamber!")
        print(f"Found {gold_reward} gold!")
        print(f"Found {potion_reward} health potions!")
        
        if player_floor not in mysterious_keys:
          mysterious_keys[player_floor] = True
          print(f"Found a mysterious key for Floor {player_floor}!")
        else:
          print(f"Found a mysterious key for Floor {player_floor}, but you already have one!")
        
        golden_keys -= 1  # Golden key is consumed
        current_room["treasure_looted"] = True
        print("The treasure chamber has been emptied.")
    else:
      print("There's nothing to loot here.")

  elif command == "take_key":
    if current_room.get("mysterious_key"):
      key = current_room["mysterious_key"]
      if player_floor in mysterious_keys or player_floor in unlocked_floors:
        print(f"You already have a mysterious key for Floor {player_floor} or this floor is already unlocked!")
        print("Maybe you should use it instead of picking up another one.")
      else:
        mysterious_keys[player_floor] = True
        current_room["mysterious_key"] = None
        print(f"You picked up the {key['name']}!")
    else:
      print("There's no mysterious key here to take.")

  elif command == "drop_mysterious_key":
    if player_floor in mysterious_keys:
      confirm = input("Are you sure you want to drop your mysterious key? (yes/no): ").lower().strip()
      if confirm == "yes":
        print("Maybe you should use it instead of dropping it...")
        confirm2 = input("Really drop it? (yes/no): ").lower().strip()
        if confirm2 == "yes":
          del mysterious_keys[player_floor]
          current_room["mysterious_key"] = {
            "floor": player_floor,
            "name": f"Mysterious Key (Floor {player_floor})"
          }
          print(f"You dropped your mysterious key for Floor {player_floor}.")
        else:
          print("You decide to keep your mysterious key.")
      else:
        print("You decide to keep your mysterious key.")
    else:
      print("You don't have a mysterious key to drop.")

  elif command == "run":
    if current_room.get("enemy"):
      if player_stamina >= 10:
        player_stamina -= 10
        print(f"You run away from the {current_room['enemy']['name']}!")
        print(f"Stamina used: 10 (Remaining: {player_stamina})")
        # Move to a random adjacent room
        directions = ["north", "south", "east", "west"]
        direction = random.choice(directions)
        if direction == "north": player_y += 1
        elif direction == "south": player_y -= 1
        elif direction == "east": player_x += 1
        elif direction == "west": player_x -= 1
      else:
        print("You don't have enough stamina to run away!")
        print(f"You need 10 stamina, but you only have {player_stamina}.")
    else:
      print("There's no enemy here to run away from.")

  elif command == "teleport":
    if waypoint_scrolls <= 0:
      print("You don't have any waypoint scrolls to use.")
    elif not waypoints:
      print("You don't have any waypoints to teleport to.")
    else:
      print("\nSelect waypoint to teleport to:")
      waypoint_list = list(waypoints.items())
      for i, (name, (floor, x, y)) in enumerate(waypoint_list, 1):
        print(f"  {i}. {name} at Floor {floor} ({x}, {y})")
      
      try:
        choice = int(input("Enter number: ")) - 1
        if 0 <= choice < len(waypoint_list):
          name, (floor, x, y) = waypoint_list[choice]
          waypoint_scrolls -= 1
          player_floor = floor
          player_x = x
          player_y = y
          print(f"You use a waypoint scroll and teleport to {name}!")
          print(f"You are now at Floor {player_floor} ({player_x}, {player_y})")
          print(f"Waypoint scrolls remaining: {waypoint_scrolls}")
        else:
          print("Invalid choice.")
      except ValueError:
        print("Please enter a valid number.")

  elif command == "bestiary":
    show_bestiary()

  elif command == "use_scroll":
    if not spell_scrolls:
      print("You don't have any spell scrolls to use.")
    else:
      print("Which spell scroll do you want to use?")
      for i, (spell_name, count) in enumerate(spell_scrolls.items(), 1):
        print(f"  {i}. {spell_name} Scroll ({count} available)")
      
      try:
        choice = int(input("Enter number: ")) - 1
        spell_list = list(spell_scrolls.items())
        if 0 <= choice < len(spell_list):
          spell_name, count = spell_list[choice]
          if spell_name in learned_spells:
            print(f"You already know the {spell_name} spell!")
          else:
            learned_spells.append(spell_name)
            spell_scrolls[spell_name] -= 1
            if spell_scrolls[spell_name] <= 0:
              del spell_scrolls[spell_name]
            print(f"You learned the {spell_name} spell!")
            print(f"Description: {spells[spell_name]['description']}")
        else:
          print("Invalid choice.")
      except ValueError:
        print("Please enter a valid number.")

  else:
    print(f"Command not recognized: '{command}'")
    print("Type 'guide' to see available help sections.")
