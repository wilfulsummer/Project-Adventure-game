from constants import enemy_stats

def show_map(player_floor, player_x, player_y, waypoints):
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

def show_room(room, player_floor, player_x, player_y, inventory, player_hp, player_max_hp, 
              player_stamina, player_max_stamina, player_mana, player_max_mana, player_money, 
              player_potions, stamina_potions, mana_potions, waypoint_scrolls, mysterious_keys, 
              golden_keys, equipped_armor, spell_scrolls, learned_spells, discovered_enemies, unlocked_floors):
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

def show_bestiary(discovered_enemies):
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
                health_desc = "Very Low Health, Double Attacks"
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
    print("  - Rats: Attack twice per turn but deal reduced damage")
    
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
    print("  - Rats: Attack twice per turn but deal reduced damage")
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