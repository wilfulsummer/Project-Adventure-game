import random
from constants import spells, MAX_WEAPONS, MAX_ARMOR, MAX_PLAYER_HP
from world_generation import get_room
from ui_functions import show_map, show_bestiary

def handle_movement(command, current_room, player_floor, player_x, player_y, worlds, learned_spells):
    """Handle movement commands"""
    if command in ["north", "south", "east", "west"]:
        if current_room.get("enemy"):
            enemy = current_room["enemy"]
            if enemy.get("is_boss"):
                print(f"The {enemy['name']} is too powerful! You manage to escape!")
                if command == "north": 
                    player_y += 1
                    return True, player_x, player_y
                elif command == "south": 
                    player_y -= 1
                    return True, player_x, player_y
                elif command == "east": 
                    player_x += 1
                    return True, player_x, player_y
                elif command == "west": 
                    player_x -= 1
                    return True, player_x, player_y
            elif enemy.get("is_training_dummy"):
                print(f"You can move freely past the {enemy['name']}.")
                if command == "north": 
                    player_y += 1
                    return True, player_x, player_y
                elif command == "south": 
                    player_y -= 1
                    return True, player_x, player_y
                elif command == "east": 
                    player_x += 1
                    return True, player_x, player_y
                elif command == "west": 
                    player_x -= 1
                    return True, player_x, player_y
            else:
                print(f"You can't leave! The {enemy['name']} blocks your way!")
                return False, player_x, player_y
        else:
            if command == "north": 
                player_y += 1
                return True, player_x, player_y
            elif command == "south": 
                player_y -= 1
                return True, player_x, player_y
            elif command == "east": 
                player_x += 1
                return True, player_x, player_y
            elif command == "west": 
                player_x -= 1
                return True, player_x, player_y
    return False, player_x, player_y

def handle_attack(current_room, inventory, player_mana, equipped_armor, player_hp, 
                 discovered_enemies, mysterious_keys, player_floor, player_money, learned_spells, spells):
    """Handle attack command"""
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
                    return True
                
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
                            return True
                        
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
                        return True
                except ValueError:
                    print("Please enter a valid number.")
                    return True
            else:
                # Regular weapon attack
                damage = weapon["damage"]
                
                # Check if weapon requires mana (staff)
                if weapon.get("requires_mana"):
                    mana_cost = weapon.get("mana_cost", 10)
                    if player_mana < mana_cost:
                        print(f"You need {mana_cost} mana to use the {weapon_name}, but you only have {player_mana} mana!")
                        print("You can't attack with this weapon.")
                        return True
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
                    return True
                
                # Enemy attack (unless stunned)
                if enemy.get("Stunned"):
                    print(f"The {enemy['name']} is stunned and can't attack!")
                    enemy["Stunned"] -= 1
                    if enemy["Stunned"] <= 0:
                        del enemy["Stunned"]
                else:
                    # Handle extra turns for enemies (like rats)
                    extra_turns = enemy.get("extra_turns", 1)
                    
                    for turn in range(extra_turns):
                        enemy_damage = enemy["base_attack"]
                        if equipped_armor:
                            # Balanced flat damage reduction: defense divided by 2 (rounded down)
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
                        
                        # Show different messages for extra turns
                        if extra_turns > 1 and turn > 0:
                            print(f"The {enemy['name']} attacks again for {enemy_damage} damage!")
                        else:
                            print(f"The {enemy['name']} attacks you for {enemy_damage} damage!")
                        
                        print(f"You have {player_hp} HP remaining.")
                        
                        if player_hp <= 0:
                            print("You have been defeated!")
                            return False
            else:
                print("The training dummy doesn't fight back.")
    else:
        print("There's no enemy here to attack.")
    return True

def handle_take(current_room, inventory, armor_inventory, MAX_WEAPONS, MAX_ARMOR):
    """Handle take command"""
    # Check if there are weapons or armor to take
    has_weapons = current_room.get("weapons")
    has_armors = current_room.get("armors")
    
    if not has_weapons and not has_armors:
        print("There's nothing here to take.")
        return True
    
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
                return True
            inventory.append(item)
            current_room["weapons"].remove(item)
            print(f"You picked up the {item['name']}!")
        else:  # armor
            if len(armor_inventory) >= MAX_ARMOR:
                print("Your armor inventory is full! Drop some armor first.")
                return True
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
                        return True
                    inventory.append(item)
                    current_room["weapons"].remove(item)
                    print(f"You picked up the {item['name']}!")
                else:  # armor
                    if len(armor_inventory) >= MAX_ARMOR:
                        print("Your armor inventory is full! Drop some armor first.")
                        return True
                    armor_inventory.append(item)
                    current_room["armors"].remove(item)
                    print(f"You picked up the {item['name']}!")
            else:
                print("Invalid choice.")
        except ValueError:
            print("Please enter a valid number.")
    return True

def handle_inventory(inventory):
    """Handle inventory command"""
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
    return True

def handle_armor(armor_inventory, equipped_armor):
    """Handle armor command"""
    if armor_inventory:
        print("\nYour armor:")
        for i, armor in enumerate(armor_inventory):
            print(f"  {i+1}. {armor['name']} (Defense: {armor['defense']}, Durability: {armor['durability']})")
    else:
        print("You have no armor.")
    if equipped_armor:
        print(f"Equipped: {equipped_armor['name']} (Defense: {equipped_armor['defense']}, Durability: {equipped_armor['durability']})")
    return True

def handle_drop(inventory, current_room):
    """Handle drop command"""
    if not inventory:
        print("You have no weapons to drop.")
        return True
    
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
    return True

def handle_drop_armor(armor_inventory, equipped_armor, current_room):
    """Handle drop_armor command"""
    if not armor_inventory:
        print("You have no armor to drop.")
        return True
    
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
    return True

def handle_equip(armor_inventory):
    """Handle equip command"""
    if not armor_inventory:
        print("You have no armor to equip.")
        return True, None
    
    print("Which armor do you want to equip?")
    for i, armor in enumerate(armor_inventory):
        print(f"  {i+1}. {armor['name']} (Defense: {armor['defense']}, Durability: {armor['durability']})")
    try:
        choice = int(input("Enter number: ")) - 1
        if 0 <= choice < len(armor_inventory):
            equipped_armor = armor_inventory[choice]
            print(f"You equipped the {equipped_armor['name']}!")
            return True, equipped_armor
        else:
            print("Invalid choice.")
    except ValueError:
        print("Please enter a valid number.")
    return True, None

def handle_switch(inventory):
    """Handle switch command"""
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
    return True

def handle_absorb(current_room, player_max_hp, player_hp, player_stamina, player_max_stamina, 
                 player_mana, player_max_mana):
    """Handle absorb command"""
    if current_room.get("crystal_type") == "life":
        player_max_hp += 10
        player_hp = min(player_hp + 20, player_max_hp)
        print("You absorb the life crystal! +10 max HP, +20 current HP")
        current_room["crystal_type"] = None
    elif current_room.get("crystal_type") == "stamina":
        player_stamina = min(player_stamina + 10, player_max_stamina)
        print("You absorb the stamina crystal! +10 stamina")
        current_room["crystal_type"] = None
    elif current_room.get("crystal_type") == "mana":
        player_max_mana = min(player_max_mana + 10, 200)
        player_mana = min(player_mana + 10, player_max_mana)
        print("You absorb the mana crystal! +10 max mana, +10 current mana")
        current_room["crystal_type"] = None
    elif current_room.get("crystal_type") == "life_stamina":
        player_max_hp += 10
        player_hp = min(player_hp + 20, player_max_hp)
        player_stamina = min(player_stamina + 10, player_max_stamina)
        print("You absorb both crystals! +10 max HP, +20 current HP, +10 stamina")
        current_room["crystal_type"] = None
    elif current_room.get("crystal_type") == "life_mana":
        player_max_hp += 10
        player_hp = min(player_hp + 20, player_max_hp)
        player_max_mana = min(player_max_mana + 10, 200)
        player_mana = min(player_mana + 10, player_max_mana)
        print("You absorb both crystals! +10 max HP, +20 current HP, +10 max mana, +10 current mana")
        current_room["crystal_type"] = None
    elif current_room.get("crystal_type") == "all":
        player_max_hp += 10
        player_hp = min(player_hp + 20, player_max_hp)
        player_stamina = min(player_stamina + 10, player_max_stamina)
        player_max_mana = min(player_max_mana + 10, 200)
        player_mana = min(player_mana + 10, player_max_mana)
        print("You absorb all crystals! +10 max HP, +20 current HP, +10 stamina, +10 max mana, +10 current mana")
        current_room["crystal_type"] = None
    else:
        print("There's no crystal here to absorb.")
    
    return player_max_hp, player_hp, player_stamina, player_max_mana, player_mana

def handle_run(current_room, player_stamina, player_x, player_y):
    """Handle run command"""
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
    
    return player_stamina, player_x, player_y 