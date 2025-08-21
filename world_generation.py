import random
from constants import weapon_names, enemy_stats, spells

def distance_from_start(x, y):
    return abs(x) + abs(y)

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
    
    # 4% chance for weapon to spawn broken
    is_broken = random.random() < 0.04
    
    # Make staffs stronger but require mana
    if weapon_name == "Magic Staff":
        damage = base_damage + damage_bonus + random.randint(1, 3)  # +1 to +3 extra damage
        if is_broken:
            # Broken weapons get enhanced stats: +50% damage, +25% crit chance, +50% crit damage, -25% mana cost
            damage = int(damage * 1.5)
            crit_chance = 0.25  # 25% crit chance
            crit_damage = 3.0   # 3x crit damage
            mana_cost = max(5, int((damage + random.randint(-2, 2)) * 0.75))  # 25% less mana cost
        else:
            crit_chance = 0.05  # Base 5% crit chance
            crit_damage = 2.0   # Base 2x crit damage
            mana_cost = max(10, damage + random.randint(-2, 2))  # Base 10 + scaling with damage
        
        durability = 0 if is_broken else (base_durability + durability_bonus + random.randint(5, 8))  # +5 to +8 extra durability
        return {
            "name": weapon_name,
            "damage": damage,
            "durability": durability,
            "max_durability": durability,
            "requires_mana": True,
            "mana_cost": mana_cost,
            "is_broken": is_broken,
            "crit_chance": crit_chance,
            "crit_damage": crit_damage
        }
    elif weapon_name == "Spell Book":
        durability = 0 if is_broken else (random.randint(15, 25) + durability_bonus + random.randint(5, 8))  # +5 to +8 extra durability
        return {
            "name": weapon_name,
            "damage": "???",
            "durability": durability,
            "max_durability": durability,
            "is_broken": is_broken
        }
    elif weapon_name == "Sword":
        # Swords are versatile - good damage and durability for all situations
        # +2-4 base damage and +3-5 durability bonus
        damage = base_damage + damage_bonus + random.randint(2, 4)
        if is_broken:
            # Broken weapons get enhanced stats: +50% damage, +25% crit chance, +50% crit damage
            damage = int(damage * 1.5)
            crit_chance = 0.25  # 25% crit chance
            crit_damage = 3.0   # 3x crit damage
        else:
            crit_chance = 0.05  # Base 5% crit chance
            crit_damage = 2.0   # Base 2x crit damage
        
        durability = 0 if is_broken else (base_durability + durability_bonus + random.randint(3, 5))
        return {
            "name": weapon_name,
            "damage": damage,
            "durability": durability,
            "max_durability": durability,
            "is_broken": is_broken,
            "crit_chance": crit_chance,
            "crit_damage": crit_damage
        }
    else:
        damage = base_damage + damage_bonus
        if is_broken:
            # Broken weapons get enhanced stats: +50% damage, +25% crit chance, +50% crit damage
            damage = int(damage * 1.5)
            crit_chance = 0.25  # 25% crit chance
            crit_damage = 3.0   # 3x crit damage
        else:
            crit_chance = 0.05  # Base 5% crit chance
            crit_damage = 2.0   # Base 2x crit damage
        
        durability = 0 if is_broken else (base_durability + durability_bonus)
        return {
            "name": weapon_name,
            "damage": damage,
            "durability": durability,
            "max_durability": durability,
            "is_broken": is_broken,
            "crit_chance": crit_chance,
            "crit_damage": crit_damage
        }

def create_armor(x, y):
    base_defense = random.randint(2, 4)  # Reduced from 5-8 to 2-4
    base_durability = random.randint(8, 15)
    distance = distance_from_start(x, y)
    # Cap scaling at 100 rooms away from (0,0)
    capped_distance = min(distance, 100)
    scaled = capped_distance // 4  # Reduced scaling from //2 to //4
    
    # 4% chance for armor to spawn broken
    is_broken = random.random() < 0.04
    
    durability = 0 if is_broken else (base_durability + scaled * random.choice([0, 1]))
    return {
        "name": random.choice(["Leather Armor", "Iron Mail", "Bone Plate", "Troll Hide"]),
        "defense": base_defense + scaled * random.choice([0, 1]),
        "durability": durability,
        "max_durability": durability
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
    
    # 4% chance for weapon to spawn broken
    is_broken = random.random() < 0.04
    
    # Make staffs stronger but require mana
    if weapon_name == "Magic Staff":
        damage = base_damage + damage_bonus + random.randint(1, 3)  # +1 to +3 extra damage
        if is_broken:
            # Broken weapons get enhanced stats: +50% damage, +25% crit chance, +50% crit damage, -25% mana cost
            damage = int(damage * 1.5)
            crit_chance = 0.25  # 25% crit chance
            crit_damage = 3.0   # 3x crit damage
            mana_cost = max(5, int((damage + random.randint(-2, 2)) * 0.75))  # 25% less mana cost
        else:
            crit_chance = 0.05  # Base 5% crit chance
            crit_damage = 2.0   # Base 2x crit damage
            mana_cost = max(10, damage + random.randint(-2, 2))  # Base 10 + scaling with damage
        
        durability = 0 if is_broken else (base_durability + durability_bonus + random.randint(5, 8))  # +5 to +8 extra durability
        return {
            "name": weapon_name,
            "damage": damage,
            "durability": durability,
            "max_durability": durability,
            "requires_mana": True,
            "mana_cost": mana_cost,
            "is_broken": is_broken,
            "crit_chance": crit_chance,
            "crit_damage": crit_damage
        }
    elif weapon_name == "Spell Book":
        durability = 0 if is_broken else (random.randint(15, 25) + durability_bonus + random.randint(5, 8))  # +5 to +8 extra durability
        return {
            "name": weapon_name,
            "damage": "???",
            "durability": durability,
            "max_durability": durability,
            "is_broken": is_broken
        }
    else:
        damage = base_damage + damage_bonus
        if is_broken:
            # Broken weapons get enhanced stats: +50% damage, +25% crit chance, +50% crit damage
            damage = int(damage * 1.5)
            crit_chance = 0.25  # 25% crit chance
            crit_damage = 3.0   # 3x crit damage
        else:
            crit_chance = 0.05  # Base 5% crit chance
            crit_damage = 2.0   # Base 2x crit damage
        
        durability = 0 if is_broken else (base_durability + durability_bonus)
        return {
            "name": weapon_name,
            "damage": damage,
            "durability": durability,
            "max_durability": durability,
            "is_broken": is_broken,
            "crit_chance": crit_chance,
            "crit_damage": crit_damage
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
    
    # 4% chance for armor to spawn broken
    is_broken = random.random() < 0.04
    
    durability = 0 if is_broken else (base_durability + bonus_dur)
    return {
        "name": random.choice(["Enchanted Mail", "Reinforced Hide", "Darksteel Vest", "Trollbone Harness"]),
        "defense": base_defense + bonus_def,
        "durability": durability,
        "max_durability": durability
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
    elif force_boss == "Baby Dragon":
        base_hp = 75  # Slightly more HP than Troll
        variation = random.randint(-5, 5)
        return {
            "name": "Baby Dragon",
            "hp": base_hp + variation + scaled * random.randint(1, 3),  # Better scaling than Troll
            "base_attack": int((12 + scaled) * 1.4),  # 1.4x damage multiplier
            "armor_pierce": 3 + scaled // 2,  # More armor piercing than Troll
            "is_boss": True
        }

    name = random.choice(list(enemy_stats.keys()))
    base_hp = enemy_stats[name]
    variation = random.randint(-3, 3)
    
    # Create enemy with base stats
    enemy = {
        "name": name,
        "hp": base_hp + variation + scaled * random.randint(1, 2),
        "base_attack": 5 + scaled,
        "armor_pierce": 1 + scaled // 6,  # Regular enemies have some armor piercing, scales with distance from (0,0)
        "is_boss": False
    }
    
    # Special handling for rats: reduce damage by 30% and give extra turns
    if name == "Rat":
        enemy["base_attack"] = int(enemy["base_attack"] * 0.7)  # 30% damage reduction
        enemy["extra_turns"] = 2  # Rats get 2 turns (double turns)
    
    # Special handling for spiders: very low damage
    if name == "Spider":
        enemy["base_attack"] = 2 + scaled  # Very low base damage that scales
    
    return enemy

def create_spider_swarm(x, y):
    """Create a swarm of spiders with 2-4 spiders based on probability"""
    dist = distance_from_start(x, y)
    capped_dist = min(dist, 100)
    scaled = capped_dist // 4
    
    # Determine swarm size based on probability
    rand = random.random()
    if rand < 0.5:
        swarm_size = 2  # 50% chance
    elif rand < 0.8:
        swarm_size = 3  # 30% chance
    else:
        swarm_size = 4  # 20% chance
    
    # Create individual spiders
    spiders = []
    for i in range(swarm_size):
        base_hp = 6
        variation = random.randint(-2, 2)
        spider = {
            "name": "Spider",
            "hp": base_hp + variation + scaled * random.randint(0, 1),
            "base_attack": 2 + scaled,  # Very low damage
            "armor_pierce": 0,  # No armor piercing
            "is_boss": False,
            "swarm_id": i + 1  # Track individual spiders in swarm
        }
        spiders.append(spider)
    
    return spiders

def create_room(floor, x, y, learned_spells):
    from constants import room_descriptions
    
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
        # Choose boss based on floor
        if floor == 2:
            boss_type = "Baby Dragon"
            description = "You find a glowing golden door… and a Baby Dragon guarding it!"
        else:
            boss_type = "Troll"
            description = "You find a glowing golden door… and the Troll guarding it!"
        
        return {
            "description": description,
            "type": "key_door",
            "key_required": True,
            "enemy": create_enemy(x, y, force_boss=boss_type),
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
            
            # Handle Spell Book damage (which is "???")
            if base["name"] == "Spell Book":
                damage = "???"
            else:
                damage = base["damage"] + bonus
            
            items.append({
                "name": f"{base['name']}+{bonus}",
                "damage": damage,
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
        
        # 35% chance for discount shop
        is_discount_shop = random.random() < 0.35
        discount_multiplier = 0.875 if is_discount_shop else 1.0  # 7.5-12.5% discount (average 10%)
        
        shop = {
            "items": items,
            "potion_price": int(random.randint(8, 15) * discount_multiplier),
            "stamina_potion_price": int(random.randint(6, 12) * discount_multiplier),
            "mana_potion_price": int(random.randint(15, 20) * discount_multiplier),
            "has_key": random.random() < 0.4,
            "armor": create_armor(x, y) if random.random() < 0.35 else None,
            "life_crystal": random.random() < 0.1,
            "health_potions": random.randint(2, 4),  # Always have health potions
            "stamina_potions": random.randint(1, 2) if random.random() < 0.6 else 0,
            "mana_potions": random.randint(1, 2) if random.random() < 0.6 else 0,
            "waypoint_scrolls": random.randint(1, 2) if random.random() < 0.3 else 0,
            "waypoint_scroll_price": int(random.randint(25, 35) * discount_multiplier),
            "spell_scrolls": spell_scrolls_shop,
            "is_discount_shop": is_discount_shop
        }
        
        # Apply discount to weapon costs
        for item in shop["items"]:
            item["cost"] = int(item["cost"] * discount_multiplier)
        
        # Apply discount to spell scroll prices and store calculated prices
        if shop["spell_scrolls"]:
            shop["spell_scroll_discount"] = discount_multiplier
            # Calculate and store spell scroll prices to avoid random price changes
            shop["spell_scroll_prices"] = {}
            for spell_name in shop["spell_scrolls"].keys():
                base_price = random.randint(40, 80)
                if is_discount_shop:
                    price = int(base_price * 0.7 * discount_multiplier)
                else:
                    price = int(base_price * 0.7)
                shop["spell_scroll_prices"][spell_name] = price
        
        shop_description = "A cozy discount shop with items for sale at reduced prices!" if is_discount_shop else "A cozy shop with items for sale."
        
        return {
            "description": shop_description,
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
        if crystal_roll < 0.175:  # 17.5% chance for dual crystals
            if random.random() < 0.5:
                crystal_type = "life_stamina"  # Life + Stamina
            else:
                crystal_type = "life_mana"  # Life + Mana
        elif crystal_roll < 0.22:  # 4.5% chance for triple crystals
            crystal_type = "all"  # All three crystals
        else:
            # Single crystal (78% chance within crystal rooms)
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
    
    # Enemy generation with spider swarm support
    enemy = None
    if random.random() < 0.5:
        # 15% chance for spider swarm, 85% chance for regular enemy
        if random.random() < 0.15:
            enemy = create_spider_swarm(x, y)
        else:
            enemy = create_enemy(x, y)
    
    return {
        "description": random.choice(room_descriptions),
        "type": "normal",
        "enemy": enemy,
        "weapons": weapons,
        "armors": armors,
        "shop": None,
        "chest": None,
        "crystal_type": None,  # Crystals only spawn in special crystal rooms
        "mysterious_key": mysterious_key_item
    }

def get_room(floor, x, y, worlds, learned_spells):
    if floor not in worlds:
        worlds[floor] = {}
    
    if (x, y) not in worlds[floor]:
        if floor == 1 and x == 0 and y == 0:
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
            worlds[floor][(x, y)] = create_room(floor, x, y, learned_spells)
    return worlds[floor][(x, y)] 