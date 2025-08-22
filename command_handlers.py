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
            elif "troll" in enemy["name"].lower():
                print("The troll is strong but its very slow!")
                print("You ran away successfully!")
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
                 discovered_enemies, mysterious_keys, player_floor, player_money, learned_spells, spells, using_fists=False,
                 attack_count=0, critical_hits=0, total_damage_dealt=0, total_damage_taken=0, 
                 enemies_defeated=0, bosses_defeated=0, weapons_broken=0, armor_broken=0):
    """Handle attack command"""
    # Increment attack count
    attack_count += 1
    
    if current_room.get("enemy"):
        enemies = current_room["enemy"]
        
        # Handle single enemy (convert to list for consistency)
        if not isinstance(enemies, list):
            enemies = [enemies]
        
        # Check if all enemies are defeated
        if not enemies:
            print("There are no enemies here to attack.")
            return True
        
        # Show enemy status
        print(f"Enemies here: {len(enemies)}")
        for i, enemy in enumerate(enemies):
            if enemy["hp"] > 0:
                print(f"  {i+1}. {enemy['name']} (HP: {enemy['hp']})")
        
        # Choose target
        if len(enemies) > 1:
            try:
                choice = int(input(f"Which enemy do you want to attack? (1-{len(enemies)}): ")) - 1
                if choice < 0 or choice >= len(enemies):
                    print("Invalid choice.")
                    return True
            except ValueError:
                print("Please enter a valid number.")
                return True
        else:
            choice = 0
        
        target_enemy = enemies[choice]
        
        # Check if target is already defeated
        if target_enemy["hp"] <= 0:
            print(f"The {target_enemy['name']} is already defeated!")
            return True
        
        # Use fists if no weapons available or if using_fists is True
        if not inventory or using_fists:
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
                print(f"You attack the {target_enemy['name']} with your {weapon_name} for {damage} damage!")
        else:
            # Use the first weapon in inventory
            weapon = inventory[0]
            weapon_name = weapon["name"]
            
            # Special handling for Spell Book
            if weapon_name == "Spell Book":
                if not learned_spells:
                    print("You have a Spell Book but don't know any spells!")
                    print("Buy spell scrolls from shops and use 'use' to learn them, or use waypoint scrolls to teleport.")
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
                                target_enemy[spell["effect"]] = {
                                    "damage": spell["effect_damage"],
                                    "duration": spell["effect_duration"]
                                }
                                print(f"The {target_enemy['name']} is {spell['effect']}!")
                            elif spell["effect"] == "Stunned":
                                target_enemy["Stunned"] = spell["effect_duration"]
                                print(f"The {target_enemy['name']} is Stunned!")
                    else:
                        print("Invalid choice.")
                        return True
                except ValueError:
                    print("Please enter a valid number.")
                    return True
            else:
                # Check if weapon is broken - broken weapons cannot be used
                if weapon.get("is_broken"):
                    print(f"Your {weapon_name} is broken and cannot be used in combat!")
                    print("You need to repair it at a shop first.")
                    return True
                
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
                
                # Check for critical hits using weapon properties
                crit_chance = weapon.get("crit_chance", 0.05)  # Use weapon's crit chance or default to 5%
                crit_multiplier = weapon.get("crit_damage", 2.0)  # Use weapon's crit damage or default to 2x
                
                # Apply weapon-specific bonuses on top of base properties
                if weapon_name == "Dagger":
                    crit_chance += 0.15  # +15% chance (total 20%)
                    crit_multiplier = max(crit_multiplier, 2.6)  # At least 2.6x damage
                
                # Axes get bonus critical damage (heavier, more powerful hits)
                elif weapon_name == "Axe":
                    crit_multiplier = max(crit_multiplier, 2.8)  # At least 2.8x damage
                
                # Roll for critical hit
                if random.random() < crit_chance:
                    original_damage = damage
                    damage = int(damage * crit_multiplier)
                    critical_hits += 1
                    
                    if weapon_name == "Dagger":
                        print(f"*** CRITICAL HIT! *** Your dagger strikes true! {original_damage} → {damage} damage!")
                    elif weapon_name == "Axe":
                        print(f"*** CRITICAL HIT! *** Your axe delivers a devastating blow! {original_damage} → {damage} damage!")
                    else:
                        print(f"*** CRITICAL HIT! *** {original_damage} → {damage} damage!")
                else:
                    # Normal attack message
                    if weapon.get("requires_mana"):
                        print(f"You attack the {target_enemy['name']} with your {weapon_name} for {damage} damage! (Mana used: {mana_cost})")
                    else:
                        print(f"You attack the {target_enemy['name']} with your {weapon_name} for {damage} damage!")
                
                # Reduce weapon durability (except for training dummy)
                if not target_enemy.get("is_training_dummy"):
                    weapon["durability"] -= 1
                    if weapon["durability"] <= 0:
                        print(f"Your {weapon['name']} breaks!")
                        inventory.pop(0)
                        weapons_broken += 1
                else:
                    print("Your weapon doesn't lose durability against the training dummy.")
        
        # Deal damage to target enemy
        target_enemy["hp"] -= damage
        total_damage_dealt += damage
        
        # Check if target enemy is defeated
        if target_enemy["hp"] <= 0:
            if target_enemy.get("is_training_dummy"):
                print("Congrats! You wasted your time...")
            else:
                print(f"You defeated the {target_enemy['name']}!")
            
            # Add enemy to discovered enemies and show unlock message
            if target_enemy["name"] not in discovered_enemies:
                discovered_enemies.add(target_enemy["name"])
                print(f"{target_enemy['name']}'s File Unlocked!")
            
            # Track enemy defeat statistics
            enemies_defeated += 1
            if target_enemy.get("is_boss"):
                bosses_defeated += 1
            
            # Boss drops mysterious key for current floor
            if target_enemy.get("is_boss"):
                if player_floor not in mysterious_keys:
                    mysterious_keys[player_floor] = True
                    print(f"The boss drops a mysterious key for Floor {player_floor}!")
                else:
                    print(f"The boss drops a mysterious key for Floor {player_floor}, but you already have one!")
            else:
                # Regular enemy drops money (but not training dummy)
                if not target_enemy.get("is_training_dummy"):
                    money_drop = random.randint(5, 15)
                    player_money += money_drop
                    print(f"You found {money_drop} gold!")
            
            # Remove defeated enemy from list
            enemies.pop(choice)
            
            # Check if all enemies are defeated
            if not enemies:
                current_room["enemy"] = None
                print("All enemies have been defeated!")
                return True
            else:
                # Update room with remaining enemies
                current_room["enemy"] = enemies
        else:
            # Don't show HP remaining for training dummy
            if not target_enemy.get("is_training_dummy"):
                print(f"The {target_enemy['name']} has {target_enemy['hp']} HP remaining.")
        
        # Enemy counter-attacks (but not training dummy)
        if not target_enemy.get("is_training_dummy"):
            # Apply status effects first
            if target_enemy.get("Burning"):
                burn_damage = target_enemy["Burning"]["damage"]
                target_enemy["hp"] -= burn_damage
                target_enemy["Burning"]["duration"] -= 1
                print(f"The {target_enemy['name']} takes {burn_damage} burning damage!")
                if target_enemy["Burning"]["duration"] <= 0:
                    del target_enemy["Burning"]
                    print(f"The {target_enemy['name']} is no longer burning.")
            
            if target_enemy.get("Poisoned"):
                poison_damage = target_enemy["Poisoned"]["damage"]
                target_enemy["hp"] -= poison_damage
                target_enemy["Poisoned"]["duration"] -= 1
                print(f"The {target_enemy['name']} takes {poison_damage} poison damage!")
                if target_enemy["Poisoned"]["duration"] <= 0:
                    del target_enemy["Poisoned"]
                    print(f"The {target_enemy['name']} is no longer poisoned.")
            
            # Check if enemy died from status effects
            if target_enemy["hp"] <= 0:
                print(f"The {target_enemy['name']} dies from the effects!")
                if target_enemy["name"] not in discovered_enemies:
                    discovered_enemies.add(target_enemy["name"])
                    print(f"{target_enemy['name']}'s File Unlocked!")
                if not target_enemy.get("is_training_dummy"):
                    money_drop = random.randint(5, 15)
                    player_money += money_drop
                    print(f"You found {money_drop} gold!")
                
                # Remove defeated enemy from list
                enemies.pop(choice)
                
                # Check if all enemies are defeated
                if not enemies:
                    current_room["enemy"] = None
                    print("All enemies have been defeated!")
                    return True
                else:
                    # Update room with remaining enemies
                    current_room["enemy"] = enemies
                return True
            
            # Enemy attack (unless stunned)
            if target_enemy.get("Stunned"):
                print(f"The {target_enemy['name']} is stunned and can't attack!")
                target_enemy["Stunned"] -= 1
                if target_enemy["Stunned"] <= 0:
                    del target_enemy["Stunned"]
            else:
                # Handle extra turns for enemies (like rats)
                extra_turns = target_enemy.get("extra_turns", 1)
                
                for turn in range(extra_turns):
                    enemy_damage = target_enemy["base_attack"]
                    if equipped_armor:
                        # Balanced flat damage reduction: defense divided by 2 (rounded down)
                        damage_reduction = equipped_armor["defense"] // 2
                        # Apply armor piercing: enemies can ignore some armor
                        armor_pierce = target_enemy.get("armor_pierce", 0)
                        effective_reduction = max(0, damage_reduction - armor_pierce)
                        enemy_damage = max(1, enemy_damage - effective_reduction)
                        # Reduce armor durability
                        equipped_armor["durability"] -= 1
                        if equipped_armor["durability"] <= 0:
                            print(f"Your {equipped_armor['name']} breaks!")
                            armor_broken += 1
                            equipped_armor = None
                    
                    player_hp -= enemy_damage
                    total_damage_taken += enemy_damage
                    
                    # Show different messages for extra turns
                    if extra_turns > 1 and turn > 0:
                        print(f"The {target_enemy['name']} attacks again for {enemy_damage} damage!")
                    else:
                        print(f"The {target_enemy['name']} attacks you for {enemy_damage} damage!")
                    
                    print(f"You have {player_hp} HP remaining.")
                    
                    if player_hp <= 0:
                        print("You have been defeated!")
                        return False # Player defeated, break out of loop and return False
        else:
            print("The training dummy doesn't fight back.")
    else:
        print("There's no enemy here to attack.")
    return True

def handle_take(current_room, inventory, armor_inventory, MAX_WEAPONS, MAX_ARMOR, mysterious_keys, golden_keys):
    """Handle take command for weapons, armor, and keys"""
    # Check if there are weapons, armor, or keys to take
    has_weapons = current_room.get("weapons")
    has_armors = current_room.get("armors")
    has_mysterious_key = current_room.get("mysterious_key")
    
    if not has_weapons and not has_armors and not has_mysterious_key:
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
    if has_mysterious_key:
        available_items.append(("mysterious_key", has_mysterious_key))
    
    if len(available_items) == 1:
        # Only one item, take it automatically
        item_type, item = available_items[0]
        if item_type == "weapon":
            if len(inventory) >= MAX_WEAPONS:
                print("Your weapon inventory is full! Drop a weapon first.")
                return True
            
            # Allow picking up broken weapons (they can be repaired but cannot be used)
            if item['durability'] <= 0:
                print(f"You picked up the broken {item['name']}! (Broken weapons cannot be used but can be repaired)")
            
            inventory.append(item)
            current_room["weapons"].remove(item)
            print(f"You picked up the {item['name']}!")
        elif item_type == "armor":
            if len(armor_inventory) >= MAX_ARMOR:
                print("Your armor inventory is full! Drop some armor first.")
                return True
            
            # Allow picking up broken armor (it can be repaired)
            if item['durability'] <= 0:
                print(f"You picked up the broken {item['name']}! (Broken armor can be repaired)")
            
            armor_inventory.append(item)
            current_room["armors"].remove(item)
            print(f"You picked up the {item['name']}!")
        elif item_type == "mysterious_key":
            floor = item["floor"]
            mysterious_keys[floor] = True
            current_room["mysterious_key"] = None
            print(f"You picked up the mysterious key for Floor {floor}!")
    else:
        # Multiple items, let player choose or take all
        print("What do you want to take?")
        print("  all - Take all items (if you have space)")
        for i, (item_type, item) in enumerate(available_items, 1):
            if item_type == "weapon":
                status = " [BROKEN]" if item['durability'] <= 0 else ""
                if item.get("requires_mana"):
                    print(f"  {i}. {item['name']} (Weapon - Damage: {item['damage']}, Durability: {item['durability']}, Mana Cost: {item.get('mana_cost', 10)}){status}")
                else:
                    print(f"  {i}. {item['name']} (Weapon - Damage: {item['damage']}, Durability: {item['durability']}){status}")
            elif item_type == "armor":
                status = " [BROKEN]" if item['durability'] <= 0 else ""
                print(f"  {i}. {item['name']} (Armor - Defense: {item['defense']}, Durability: {item['durability']}){status}")
            elif item_type == "mysterious_key":
                print(f"  {i}. Mysterious Key (Floor {item['floor']})")
        
        choice = input("Enter number or 'all': ").strip().lower()
        
        if choice == "all":
            # Take all items that we can fit
            items_taken = 0
            items_skipped = 0
            
            # Take mysterious keys first (they don't take inventory space)
            for item_type, item in available_items[:]:
                if item_type == "mysterious_key":
                    floor = item["floor"]
                    mysterious_keys[floor] = True
                    current_room["mysterious_key"] = None
                    print(f"You picked up the mysterious key for Floor {floor}!")
                    items_taken += 1
                    available_items.remove((item_type, item))
            
            # Take weapons until inventory is full
            weapons_to_take = [item for item_type, item in available_items if item_type == "weapon"]
            for weapon in weapons_to_take:
                if len(inventory) < MAX_WEAPONS:
                    # Allow picking up broken weapons (they can be repaired but cannot be used)
                    if weapon['durability'] <= 0:
                        print(f"You picked up the broken {weapon['name']}! (Broken weapons cannot be used but can be repaired)")
                    
                    inventory.append(weapon)
                    current_room["weapons"].remove(weapon)
                    print(f"You picked up the {weapon['name']}!")
                    items_taken += 1
                    current_room["weapons"].remove(weapon)
                    print(f"You picked up the {weapon['name']}!")
                    items_taken += 1
                else:
                    items_skipped += 1
            
            # Take armor until inventory is full
            armors_to_take = [item for item_type, item in available_items if item_type == "armor"]
            for armor in armors_to_take:
                if len(armor_inventory) < MAX_ARMOR:
                    # Allow picking up broken armor (it can be repaired)
                    if armor['durability'] <= 0:
                        print(f"You picked up the broken {armor['name']}! (Broken armor can be repaired)")
                    
                    armor_inventory.append(armor)
                    current_room["armors"].remove(armor)
                    print(f"You picked up the {armor['name']}!")
                    items_taken += 1
                    current_room["armors"].remove(armor)
                    print(f"You picked up the {armor['name']}!")
                    items_taken += 1
                else:
                    items_skipped += 1
            
            # Summary
            if items_taken > 0:
                print(f"✅ Took {items_taken} items!")
            if items_skipped > 0:
                print(f"⚠️  Skipped {items_skipped} items (inventory full)")
            
        else:
            # Handle single item selection
            try:
                choice_num = int(choice) - 1
                if 0 <= choice_num < len(available_items):
                    item_type, item = available_items[choice_num]
                    if item_type == "weapon":
                        if len(inventory) >= MAX_WEAPONS:
                            print("Your weapon inventory is full! Drop a weapon first.")
                            return True
                        
                        # Allow picking up broken weapons (they can be repaired but cannot be used)
                        if item['durability'] <= 0:
                            print(f"You picked up the broken {item['name']}! (Broken weapons cannot be used but can be repaired)")
                        
                        inventory.append(item)
                        current_room["weapons"].remove(item)
                        print(f"You picked up the {item['name']}!")
                    elif item_type == "armor":
                        if len(armor_inventory) >= MAX_ARMOR:
                            print("Your armor inventory is full! Drop some armor first.")
                            return True
                        
                        # Allow picking up broken armor (it can be repaired)
                        if item['durability'] <= 0:
                            print(f"You picked up the broken {item['name']}! (Broken armor can be repaired)")
                        
                        armor_inventory.append(item)
                        current_room["armors"].remove(item)
                        print(f"You picked up the {item['name']}!")
                    elif item_type == "mysterious_key":
                        floor = item["floor"]
                        mysterious_keys[floor] = True
                        current_room["mysterious_key"] = None
                        print(f"You picked up the mysterious key for Floor {floor}!")
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Please enter a valid number or 'all'.")
    
    return True

def handle_inventory(inventory, using_fists=False):
    """Handle inventory command"""
    
    if inventory:
        print("\nYour weapons:")
        for i, weapon in enumerate(inventory):
            # Show broken status and enhanced stats
            broken_tag = " [BROKEN - CANNOT USE]" if weapon.get("is_broken") else ""
            crit_info = ""
            if weapon.get("crit_chance") and weapon.get("crit_damage") and not weapon.get("is_broken"):
                crit_info = f", Crit: {int(weapon['crit_chance']*100)}% ({weapon['crit_damage']}x)"
            
            max_durability = weapon.get("max_durability", weapon["durability"])
            if weapon.get("name") == "Spell Book":
                print(f"  {i+1}. {weapon['name']} (Damage: ???, Durability: {weapon['durability']}/{max_durability}){broken_tag}")
            elif weapon.get("requires_mana"):
                print(f"  {i+1}. {weapon['name']} (Damage: {weapon['damage']}, Durability: {weapon['durability']}/{max_durability}, Mana Cost: {weapon.get('mana_cost', 10)}){broken_tag}{crit_info}")
            else:
                print(f"  {i+1}. {weapon['name']} (Damage: {weapon['damage']}, Durability: {weapon['durability']}/{max_durability}){broken_tag}{crit_info}")
    
    # Show current weapon status
    if using_fists:
        print("Currently using: Fists (Damage: 4, Durability: Infinite)")
    elif inventory:
        print(f"Currently using: {inventory[0]['name']}")
    else:
        print("You have no weapons.")
        print("Currently using: Fists (Damage: 4, Durability: Infinite)")
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

def handle_drop(inventory, armor_inventory, equipped_armor, current_room):
    """Handle drop command for both weapons and armor"""
    # Check if player has anything to drop
    if not inventory and not armor_inventory:
        print("You have nothing to drop.")
        return True
    
    # Show available items to drop
    print("What do you want to drop?")
    
    # Show weapons
    if inventory:
            print("\nWeapons:")
            for i, weapon in enumerate(inventory):
                # Show broken status and enhanced stats
                broken_tag = " [BROKEN - CANNOT USE]" if weapon.get("is_broken") else ""
                crit_info = ""
                if weapon.get("crit_chance") and weapon.get("crit_damage") and not weapon.get("is_broken"):
                    crit_info = f", Crit: {int(weapon['crit_chance']*100)}% ({weapon['crit_damage']}x)"
                
                max_durability = weapon.get("max_durability", weapon["durability"])
                if weapon.get("name") == "Spell Book":
                    print(f"  {i+1}. {weapon['name']} (Damage: ???, Durability: {weapon['durability']}/{max_durability}){broken_tag}")
                elif weapon.get("requires_mana"):
                    print(f"  {i+1}. {weapon['name']} (Damage: {weapon['damage']}, Durability: {weapon['durability']}/{max_durability}, Mana Cost: {weapon.get('mana_cost', 10)}){broken_tag}{crit_info}")
                else:
                    print(f"  {i+1}. {weapon['name']} (Damage: {weapon['damage']}, Durability: {weapon['durability']}/{max_durability}){broken_tag}{crit_info}")
    
    # Show armor
    if armor_inventory:
        print("\nArmor:")
        for i, armor in enumerate(armor_inventory):
            equipped_tag = " [EQUIPPED]" if equipped_armor and equipped_armor == armor else ""
            print(f"  {len(inventory) + i + 1}. {armor['name']} (Defense: {armor['defense']}, Durability: {armor['durability']}){equipped_tag}")
    
    # Calculate total items
    total_items = len(inventory) + len(armor_inventory)
    
    try:
        choice = int(input(f"Enter number (1-{total_items}): ")) - 1
        if 0 <= choice < total_items:
            if choice < len(inventory):
                # Dropping a weapon
                dropped_item = inventory.pop(choice)
                # Check if this was the currently held weapon (first in inventory)
                if choice == 0:
                    print(f"You dropped your currently held weapon: {dropped_item['name']}")
                    if inventory:
                        print(f"You are now holding: {inventory[0]['name']}")
                    else:
                        print("You are now holding no weapon (using fists).")
                else:
                    print(f"You dropped the {dropped_item['name']}.")
                
                # Initialize weapons list if it doesn't exist
                if "weapons" not in current_room:
                    current_room["weapons"] = []
                current_room["weapons"].append(dropped_item)
                
            else:
                # Dropping armor
                armor_choice = choice - len(inventory)
                dropped_item = armor_inventory.pop(armor_choice)
                
                # Unequip if this was the equipped armor
                if equipped_armor and equipped_armor == dropped_item:
                    equipped_armor = None
                    print(f"You unequipped and dropped your equipped armor: {dropped_item['name']}")
                    print("You are now wearing no armor.")
                else:
                    print(f"You dropped the {dropped_item['name']}.")
                
                # Initialize armors list if it doesn't exist
                if "armors" not in current_room:
                    current_room["armors"] = []
                current_room["armors"].append(dropped_item)
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
        status = " [BROKEN]" if armor['durability'] <= 0 else ""
        print(f"  {i+1}. {armor['name']} (Defense: {armor['defense']}, Durability: {armor['durability']}){status}")
    try:
        choice = int(input("Enter number: ")) - 1
        if 0 <= choice < len(armor_inventory):
            equipped_armor = armor_inventory[choice]
            
            # Check if armor is broken
            if equipped_armor['durability'] <= 0:
                print(f"You cannot equip {equipped_armor['name']} - it's broken!")
                return True, None
            
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
    print("  0. Fists (Damage: 4, Durability: Infinite)")
    for i, weapon in enumerate(inventory):
        status = " [BROKEN]" if weapon['durability'] <= 0 else ""
        if weapon.get("name") == "Spell Book":
            print(f"  {i+1}. {weapon['name']} (Damage: ???, Durability: {weapon['durability']}){status}")
        elif weapon.get("requires_mana"):
            print(f"  {i+1}. {weapon['name']} (Damage: {weapon['damage']}, Durability: {weapon['durability']}, Mana Cost: {weapon.get('mana_cost', 10)}){status}")
        else:
            print(f"  {i+1}. {weapon['name']} (Damage: {weapon['damage']}, Durability: {weapon['durability']}){status}")
    try:
        choice = int(input("Enter number: ")) - 1
        if choice == -1:
            # Switch to fists
            if inventory:
                print("You switch to using your fists.")
                # Move current weapon to back of inventory
                if inventory:
                    weapon = inventory.pop(0)
                    inventory.append(weapon)
            else:
                print("You're already using your fists.")
            return True, True  # Return success and using_fists=True
        elif 0 <= choice < len(inventory):
            # Switch to weapon
            weapon = inventory[choice]
            
            # Check if weapon is broken
            if weapon['durability'] <= 0:
                print(f"You cannot switch to {weapon['name']} - it's broken!")
                return True, False
            
            # Move selected weapon to front of inventory
            weapon = inventory.pop(choice)
            inventory.insert(0, weapon)
            print(f"You switched to {weapon['name']}.")
            return True, False  # Return success and using_fists=False
        else:
            print("Invalid choice.")
    except ValueError:
        print("Please enter a valid number.")
    return True, False  # Return success and using_fists=False (default)

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

def handle_consume(current_room, player_max_hp, player_hp, player_stamina, player_max_stamina, 
                   player_mana, player_max_mana, player_potions, stamina_potions, mana_potions):
    """Handle consume command for crystals and potions"""
    
    # Check for crystals first (highest priority)
    if current_room.get("crystal_type"):
        crystal_type = current_room["crystal_type"]
        
        if crystal_type == "life":
            player_max_hp += 10
            player_hp += 20
            print("You absorb the life crystal!")
            print(f"Max HP increased to {player_max_hp}!")
            print(f"Current HP increased to {player_hp}!")
            current_room["crystal_type"] = None
            return player_max_hp, player_hp, player_stamina, player_max_mana, player_mana
            
        elif crystal_type == "stamina":
            player_max_stamina += 10
            player_stamina += 10
            print("You absorb the stamina crystal!")
            print(f"Max stamina increased to {player_max_stamina}!")
            print(f"Current stamina increased to {player_stamina}!")
            current_room["crystal_type"] = None
            return player_max_hp, player_hp, player_stamina, player_max_stamina, player_mana
            
        elif crystal_type == "mana":
            player_max_mana += 10
            player_mana += 10
            print("You absorb the mana crystal!")
            print(f"Max mana increased to {player_max_mana}!")
            print(f"Current mana increased to {player_mana}!")
            current_room["crystal_type"] = None
            return player_max_hp, player_hp, player_stamina, player_max_stamina, player_mana
            
        elif crystal_type == "life_stamina":
            player_max_hp += 10
            player_hp += 20
            player_max_stamina += 10
            player_stamina += 10
            print("You absorb both crystals!")
            print(f"Max HP increased to {player_max_hp}!")
            print(f"Current HP increased to {player_hp}!")
            print(f"Max stamina increased to {player_max_stamina}!")
            print(f"Current stamina increased to {player_stamina}!")
            current_room["crystal_type"] = None
            return player_max_hp, player_hp, player_stamina, player_max_stamina, player_mana
            
        elif crystal_type == "life_mana":
            player_max_hp += 10
            player_hp += 20
            player_max_mana += 10
            player_mana += 10
            print("You absorb both crystals!")
            print(f"Max HP increased to {player_max_hp}!")
            print(f"Current HP increased to {player_hp}!")
            print(f"Max mana increased to {player_max_mana}!")
            print(f"Current mana increased to {player_mana}!")
            current_room["crystal_type"] = None
            return player_max_hp, player_hp, player_stamina, player_max_stamina, player_mana
            
        elif crystal_type == "all":
            player_max_hp += 10
            player_hp += 20
            player_max_stamina += 10
            player_stamina += 10
            player_max_mana += 10
            player_mana += 10
            print("You absorb all three crystals!")
            print(f"Max HP increased to {player_max_hp}!")
            print(f"Current HP increased to {player_hp}!")
            print(f"Max stamina increased to {player_max_stamina}!")
            print(f"Current stamina increased to {player_stamina}!")
            print(f"Max mana increased to {player_max_mana}!")
            print(f"Current mana increased to {player_mana}!")
            current_room["crystal_type"] = None
            return player_max_hp, player_hp, player_stamina, player_max_stamina, player_mana
    
    # If no crystals, show potion options
    print("What would you like to consume?")
    
    potion_options = []
    if player_potions > 0:
        potion_options.append(("health", player_potions))
    if stamina_potions > 0:
        potion_options.append(("stamina", stamina_potions))
    if mana_potions > 0:
        potion_options.append(("mana", mana_potions))
    
    if not potion_options:
        print("You have no potions to use.")
        return player_max_hp, player_hp, player_stamina, player_max_stamina, player_mana
    
    print("Available potions:")
    for i, (potion_type, count) in enumerate(potion_options, 1):
        print(f"  {i}. {potion_type.title()} Potion ({count} available)")
    
    try:
        choice = int(input(f"Enter number (1-{len(potion_options)}): ")) - 1
        if 0 <= choice < len(potion_options):
            potion_type, count = potion_options[choice]
            
            if potion_type == "health":
                if player_potions > 0:
                    player_potions -= 1
                    player_hp = min(player_hp + 30, player_max_hp)
                    print(f"You used a health potion! HP: {player_hp}/{player_max_hp}")
                else:
                    print("You don't have any health potions!")
                    
            elif potion_type == "stamina":
                if stamina_potions > 0:
                    stamina_potions -= 1
                    player_stamina = min(player_stamina + 10, player_max_stamina)
                    print(f"You used a stamina potion! Stamina: {player_stamina}/{player_max_stamina}")
                else:
                    print("You don't have any stamina potions!")
                    
            elif potion_type == "mana":
                if mana_potions > 0:
                    mana_potions -= 1
                    player_mana = min(player_mana + 15, player_max_mana)
                    print(f"You used a mana potion! Mana: {player_mana}/{player_max_mana}")
                else:
                    print("You don't have any mana potions!")
        else:
            print("Invalid choice.")
    except ValueError:
        print("Please enter a valid number.")
    
    return player_max_hp, player_hp, player_stamina, player_max_stamina, player_mana

def handle_run(current_room, player_stamina, player_x, player_y):
    """Handle run command"""
    if current_room.get("enemy"):
        enemy = current_room["enemy"]
        enemy_name = enemy["name"]
        
        # Special logic for baby dragons
        if "baby dragon" in enemy_name.lower():
            print("You ran away successfully!")
            # Move to a random adjacent room without stamina cost
            directions = ["north", "south", "east", "west"]
            direction = random.choice(directions)
            if direction == "north": player_y += 1
            elif direction == "south": player_y -= 1
            elif direction == "east": player_x += 1
            elif direction == "west": player_x -= 1
        elif player_stamina >= 10:
            player_stamina -= 10
            print(f"You run away from the {enemy_name}!")
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

def handle_repair(current_room, inventory, armor_inventory, player_money):
    """Handle repair command at shops"""
    if not current_room.get("shop"):
        print("You can only repair items at shops.")
        return True, player_money
    
    print("What would you like to repair?")
    print("  1. Weapons")
    print("  2. Armor")
    
    try:
        choice = int(input("Enter number: "))
        
        if choice == 1:
            # Repair weapons
            if not inventory:
                print("You have no weapons to repair.")
                return True, player_money
            
            print("Which weapon do you want to repair?")
            for i, weapon in enumerate(inventory):
                if weapon.get("name") == "Spell Book":
                    print(f"  {i+1}. {weapon['name']} (Durability: {weapon['durability']})")
                elif weapon.get("requires_mana"):
                    print(f"  {i+1}. {weapon['name']} (Durability: {weapon['durability']}, Mana Cost: {weapon.get('mana_cost', 10)})")
                else:
                    print(f"  {i+1}. {weapon['name']} (Durability: {weapon['durability']})")
            
            try:
                weapon_choice = int(input("Enter number: ")) - 1
                if 0 <= weapon_choice < len(inventory):
                    weapon = inventory[weapon_choice]
                    
                    # Check if this is a blacksmith shop for special pricing
                    shop = current_room.get("shop", {})
                    is_blacksmith = shop.get("is_blacksmith", False)
                    
                    if is_blacksmith:
                        # Blacksmith pricing: fixed cost per durability point + bonus
                        base_cost = shop.get("repair_price", 10)  # Cost per durability point
                        repair_bonus = shop.get("repair_bonus", 1)  # Extra durability restored
                        print(f"[BLACKSMITH] Special pricing: {base_cost} gold per durability point (+{repair_bonus} bonus durability)")
                    else:
                        # Regular shop pricing: cost based on weapon power
                        if weapon.get("name") == "Spell Book":
                            # Spell books have high base cost due to their utility
                            base_cost = 3
                        else:
                            # Calculate cost based on damage
                            damage = weapon.get("damage", 5)
                            base_cost = max(1, damage // 4)  # 1 gold per 4 damage, minimum 1
                        repair_bonus = 0
                        print(f"[REGULAR SHOP] Standard pricing: {base_cost} gold per durability point")
                    
                    # Calculate how much durability needs to be restored
                    max_durability = weapon.get("max_durability", weapon["durability"] + 5)  # Use actual max durability
                    durability_needed = max_durability - weapon["durability"]
                    
                    if durability_needed <= 0:
                        print(f"Your {weapon['name']} is already at full durability!")
                        return True, player_money
                    
                    total_cost = base_cost * durability_needed
                    
                    print(f"Repairing {weapon['name']} will cost {total_cost} gold ({base_cost} gold per durability point).")
                    print(f"Current durability: {weapon['durability']}, Max durability: {max_durability}")
                    if repair_bonus > 0:
                        print(f"Blacksmith bonus: +{repair_bonus} durability (final durability: {min(max_durability + repair_bonus, max_durability + 5)})")
                    
                    if player_money < total_cost:
                        print(f"You need {total_cost} gold, but you only have {player_money} gold.")
                        return True, player_money
                    
                    confirm = input("Proceed with repair? (y/n): ").lower()
                    if confirm == 'y':
                        player_money -= total_cost
                        
                        # Apply blacksmith bonus if available
                        if repair_bonus > 0:
                            weapon["durability"] = min(max_durability + repair_bonus, max_durability + 5)  # Cap bonus at +5
                            print(f"[BLACKSMITH BONUS] +{repair_bonus} durability applied!")
                        else:
                            weapon["durability"] = max_durability
                        
                        # If weapon was broken, restore normal stats
                        if weapon.get("is_broken"):
                            weapon["is_broken"] = False
                            # Restore normal damage (remove 50% bonus)
                            if weapon.get("damage") != "???":
                                weapon["damage"] = int(weapon["damage"] / 1.5)
                            # Restore normal crit stats
                            weapon["crit_chance"] = 0.05
                            weapon["crit_damage"] = 2.0
                            # Restore normal mana cost for magic weapons
                            if weapon.get("requires_mana"):
                                weapon["mana_cost"] = max(10, weapon["damage"] + random.randint(-2, 2))
                            print(f"Your {weapon['name']} has been repaired and restored to normal stats!")
                        else:
                            if repair_bonus > 0:
                                print(f"Your {weapon['name']} has been repaired to {weapon['durability']}/{max_durability} durability (+{repair_bonus} bonus)!")
                            else:
                                print(f"Your {weapon['name']} has been repaired to full durability!")
                        
                        print(f"Gold remaining: {player_money}")
                    else:
                        print("Repair cancelled.")
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Please enter a valid number.")
        
        elif choice == 2:
            # Repair armor
            if not armor_inventory:
                print("You have no armor to repair.")
                return True, player_money
            
            print("Which armor do you want to repair?")
            for i, armor in enumerate(armor_inventory):
                print(f"  {i+1}. {armor['name']} (Durability: {armor['durability']})")
            
            try:
                armor_choice = int(input("Enter number: ")) - 1
                if 0 <= armor_choice < len(armor_inventory):
                    armor = armor_inventory[armor_choice]
                    
                    # Calculate repair cost based on armor defense
                    defense = armor.get("defense", 3)
                    base_cost = max(1, defense // 3)  # 1 gold per 3 defense, minimum 1
                    
                    # Calculate how much durability needs to be restored
                    max_durability = armor.get("max_durability", armor["durability"] + 10)  # Use actual max durability
                    durability_needed = max_durability - armor["durability"]
                    
                    if durability_needed <= 0:
                        print(f"Your {armor['name']} is already at full durability!")
                        return True, player_money
                    
                    total_cost = base_cost * durability_needed
                    
                    print(f"Repairing {armor['name']} will cost {total_cost} gold ({base_cost} gold per durability point).")
                    print(f"Current durability: {armor['durability']}, Max durability: {max_durability}")
                    
                    if player_money < total_cost:
                        print(f"You need {total_cost} gold, but you only have {player_money} gold.")
                        return True, player_money
                    
                    confirm = input("Proceed with repair? (y/n): ").lower()
                    if confirm == 'y':
                        player_money -= total_cost
                        armor["durability"] = max_durability
                        print(f"Your {armor['name']} has been repaired to full durability!")
                        print(f"Gold remaining: {player_money}")
                    else:
                        print("Repair cancelled.")
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Please enter a valid number.")
        
        else:
            print("Invalid choice.")
    
    except ValueError:
        print("Please enter a valid number.")
    
    return True, player_money 

def handle_waypoint(command_parts, waypoints, waypoint_scrolls, player_floor, player_x, player_y):
    """Handle enhanced waypoint command with subcommands"""
    if len(command_parts) < 2:
        print("Waypoint command usage:")
        print("  waypoint add <name> - Add a waypoint at current location")
        print("  waypoint view - List all waypoints")
        print("  waypoint delete <name> - Delete a specific waypoint")
        print("  waypoint teleport - Use waypoint scroll to teleport")
        return waypoints, waypoint_scrolls
    
    subcommand = command_parts[1].lower()
    
    if subcommand == "add":
        if len(command_parts) < 3:
            print("Usage: waypoint add <name>")
            return waypoints, waypoint_scrolls
        
        name = " ".join(command_parts[2:])
        if len(waypoints) >= 10:
            print("You can only have up to 10 waypoints!")
            return waypoints, waypoint_scrolls
        
        waypoints[name] = (player_floor, player_x, player_y)
        print(f"Waypoint '{name}' added at Floor {player_floor} ({player_x}, {player_y})")
        
    elif subcommand == "view":
        if not waypoints:
            print("No waypoints set.")
        else:
            print("\n=== WAYPOINTS ===")
            for i, (name, (floor, x, y)) in enumerate(waypoints.items(), 1):
                print(f"  {i}. {name}: Floor {floor} ({x}, {y})")
            print("==================")
    
    elif subcommand == "delete":
        if len(command_parts) < 3:
            print("Usage: waypoint delete <name>")
            return waypoints, waypoint_scrolls
        
        name = " ".join(command_parts[2:])
        if name in waypoints:
            del waypoints[name]
            print(f"Waypoint '{name}' deleted.")
        else:
            print(f"Waypoint '{name}' not found.")
    
    elif subcommand == "teleport":
        if waypoint_scrolls <= 0:
            print("You don't have any waypoint scrolls to use.")
            return waypoints, waypoint_scrolls
        
        if not waypoints:
            print("You don't have any waypoints to teleport to.")
            return waypoints, waypoint_scrolls
        
        print("\nSelect waypoint to teleport to:")
        waypoint_list = list(waypoints.items())
        for i, (name, (floor, x, y)) in enumerate(waypoint_list, 1):
            print(f"  {i}. {name} at Floor {floor} ({x}, {y})")
        
        try:
            choice = int(input("Enter number: ")) - 1
            if 0 <= choice < len(waypoint_list):
                name, (floor, x, y) = waypoint_list[choice]
                waypoint_scrolls -= 1
                print(f"You use a waypoint scroll and teleport to {name}!")
                print(f"You are now at Floor {floor} ({x}, {y})")
                print(f"Waypoint scrolls remaining: {waypoint_scrolls}")
                # Note: The actual teleportation would be handled by the main game loop
                # This function just handles the scroll consumption and waypoint selection
            else:
                print("Invalid choice.")
        except ValueError:
            print("Please enter a valid number.")
    
    else:
        print(f"Unknown waypoint subcommand: {subcommand}")
        print("Available subcommands: add, view, delete, teleport")
    
    return waypoints, waypoint_scrolls 

def handle_equipment(inventory, armor_inventory, equipped_armor, using_fists):
    """Handle equipment command to show both weapons and armor"""
    print("\n=== EQUIPMENT ===")
    
    # Show weapons section
    print("Weapons:")
    if not inventory:
        print("  None (using fists)")
    else:
        for i, weapon in enumerate(inventory):
            if weapon.get("name") == "Spell Book":
                print(f"  {i+1}. {weapon['name']} (Damage: ???, Durability: {weapon['durability']})")
            elif weapon.get("requires_mana"):
                print(f"  {i+1}. {weapon['name']} (Damage: {weapon['damage']}, Durability: {weapon['durability']}, Mana Cost: {weapon.get('mana_cost', 10)})")
            else:
                print(f"  {i+1}. {weapon['name']} (Damage: {weapon['damage']}, Durability: {weapon['durability']})")
    
    # Show armor section
    print("\nArmor:")
    if not armor_inventory:
        print("  None")
    else:
        for i, armor in enumerate(armor_inventory):
            equipped_tag = " [EQUIPPED]" if equipped_armor and equipped_armor == armor else ""
            print(f"  {i+1}. {armor['name']} (Defense: {armor['defense']}, Durability: {armor['durability']}){equipped_tag}")
    
    # Show current status
    print(f"\nCurrent Status:")
    if using_fists:
        print("  Weapon: Fists (Damage: 4, Durability: Infinite)")
    elif inventory:
        print(f"  Weapon: {inventory[0]['name']}")
    else:
        print("  Weapon: None")
    
    if equipped_armor:
        print(f"  Armor: {equipped_armor['name']}")
    else:
        print("  Armor: None")
    
    print("==================")
    return True 