import random
import json
import os

# File to track discovered unique items
UNIQUE_ITEMS_FILE = "unique_items.json"

# Dictionary to track which unique items have been discovered
discovered_uniques = {}

def load_unique_items():
    """Load the list of discovered unique items from file"""
    global discovered_uniques
    if os.path.exists(UNIQUE_ITEMS_FILE):
        try:
            with open(UNIQUE_ITEMS_FILE, "r") as f:
                discovered_uniques = json.load(f)
        except:
            discovered_uniques = {}
    else:
        discovered_uniques = {}

def save_unique_items():
    """Save the list of discovered unique items to file"""
    with open(UNIQUE_ITEMS_FILE, "w") as f:
        json.dump(discovered_uniques, f)

def is_unique_discovered(unique_id):
    """Check if a unique item has already been discovered"""
    return unique_id in discovered_uniques

def mark_unique_discovered(unique_id, location_info=None):
    """Mark a unique item as discovered"""
    discovered_uniques[unique_id] = {
        "discovered": True,
        "location": location_info or {},
        "timestamp": "now"  # Could add actual timestamp if needed
    }
    save_unique_items()

def get_unique_item(unique_id, x, y, floor):
    """Get a unique item if it hasn't been discovered yet"""
    if is_unique_discovered(unique_id):
        return None  # Already discovered
    
    # Check if this unique should spawn at this location
    if not should_unique_spawn_here(unique_id, x, y, floor):
        return None
    
    # This is where we'll add unique item definitions
    # For now, return None (no uniques defined yet)
    return None

def should_unique_spawn_here(unique_id, x, y, floor):
    """Check if a unique item should spawn at the given location"""
    # Define specific spawn conditions for each unique
    unique_spawn_conditions = {
        # The Wanderer's Cloak - spawns after 100+ rooms from (0,0) on Floor 1
        "wanderers_cloak": {
            "floor": 1,
            "min_distance": 100,  # Must be at least 100 rooms away from (0,0)
            "room_type": "normal"  # Can spawn in any normal room
        }
        # Example format:
        # "sword_of_flames": {"floor": 5, "x": 10, "y": 15, "room_type": "special"},
        # "crown_of_kings": {"floor": 10, "x": 0, "y": 0, "room_type": "boss_room"},
        # Add specific conditions here when we add unique items
    }
    
    if unique_id not in unique_spawn_conditions:
        return False
    
    conditions = unique_spawn_conditions[unique_id]
    
    # Check floor requirement
    if "floor" in conditions and floor != conditions["floor"]:
        return False
    
    # Check specific coordinates (only if specified)
    if "x" in conditions and "y" in conditions:
        if x != conditions["x"] or y != conditions["y"]:
            return False
    
    # Check minimum distance requirement
    if "min_distance" in conditions:
        from world_generation import distance_from_start
        distance = distance_from_start(x, y)
        if distance < conditions["min_distance"]:  # Must be at least min_distance (100)
            return False
    
    # Check room type (if specified)
    if "room_type" in conditions:
        # This will be checked in the main game when room type is known
        pass
    
    return True

def check_for_unique_items(x, y, floor, room_type="normal"):
    """Check if any unique items should spawn in this room"""
    unique_items = []
    
    # List of all possible unique IDs (will be populated when we create uniques)
    all_unique_ids = [
        "wanderers_cloak",  # The Wanderer's Cloak - unique armor
        # "sword_of_flames",
        # "crown_of_kings", 
        # Add unique IDs here when we create them
    ]
    
    for unique_id in all_unique_ids:
        if should_unique_spawn_here(unique_id, x, y, floor):
            # Check room type if specified
            unique_spawn_conditions = {
                "wanderers_cloak": {
                    "floor": 1,
                    "min_distance": 100,
                    "room_type": "normal"
                }
            }
            
            if unique_id in unique_spawn_conditions:
                conditions = unique_spawn_conditions[unique_id]
                if "room_type" in conditions and room_type != conditions["room_type"]:
                    continue
            
            # Create the unique item based on its type
            if unique_id == "wanderers_cloak":
                unique_item = create_unique_armor(unique_id, x, y, floor)
            else:
                # Default to weapon creation for other uniques
                unique_item = create_unique_weapon(unique_id, x, y, floor)
                
            if unique_item:
                unique_items.append(unique_item)
    
    return unique_items

def create_unique_weapon(unique_id, x, y, floor):
    """Create a unique weapon with special properties"""
    if is_unique_discovered(unique_id):
        return None
    
    # Placeholder for unique weapon creation
    # Will be implemented when we add specific unique items
    return None

def create_unique_armor(unique_id, x, y, floor):
    """Create a unique armor with special properties"""
    if is_unique_discovered(unique_id):
        return None
    
    if unique_id == "wanderers_cloak":
        from world_generation import distance_from_start
        
        # Calculate distance from starting point
        distance = distance_from_start(x, y)
        
        # The Wanderer's Cloak scales with distance but caps at 100 for balance
        # Base defense: 8, scaling: +1 per 10 rooms (capped at 100 rooms)
        capped_distance = min(distance, 100)
        base_defense = 8
        scaling_bonus = capped_distance // 10
        
        # Create the unique armor
        wanderers_cloak = {
            "name": "The Wanderer's Cloak",
            "type": "armor",
            "defense": base_defense + scaling_bonus,
            "durability": 60,
            "max_durability": 60,
            "unique_id": "wanderers_cloak",
            "description": f"A legendary cloak that grows stronger with distance. Found {distance} rooms from the starting point.",
            "rarity": "unique"
        }
        
        return wanderers_cloak
    
    # Placeholder for other unique armor items
    return None

def create_unique_consumable(unique_id, x, y, floor):
    """Create a unique consumable item with special properties"""
    if is_unique_discovered(unique_id):
        return None
    
    # Placeholder for unique consumable creation
    # Will be implemented when we add specific unique items
    return None

def show_unique_collection():
    """Display all discovered unique items"""
    if not discovered_uniques:
        print("You haven't discovered any unique items yet.")
        return
    
    print("\n=== UNIQUE ITEMS COLLECTION ===")
    for unique_id, info in discovered_uniques.items():
        print(f"  • {unique_id}")
        if info.get("location"):
            loc = info["location"]
            if "floor" in loc and "x" in loc and "y" in loc:
                print(f"    Found at: Floor {loc['floor']} ({loc['x']}, {loc['y']})")
    print("================================")

# Initialize unique items system
# Note: load_unique_items() is called when needed, not at module import
# This prevents persistent state issues during testing 