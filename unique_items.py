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
    
    # Check specific coordinates
    if "x" in conditions and x != conditions["x"]:
        return False
    if "y" in conditions and y != conditions["y"]:
        return False
    
    # Check room type (if specified)
    if "room_type" in conditions:
        # This will be checked in the main game when room type is known
        pass
    
    return True

def check_for_unique_items(x, y, floor, room_type="normal"):
    """Check if any unique items should spawn in this room"""
    unique_items = []
    
    # List of all possible unique IDs (will be populated when we add uniques)
    all_unique_ids = [
        # "sword_of_flames",
        # "crown_of_kings", 
        # Add unique IDs here when we create them
    ]
    
    for unique_id in all_unique_ids:
        if should_unique_spawn_here(unique_id, x, y, floor):
            # Check room type if specified
            unique_spawn_conditions = {
                # Define conditions here when we add uniques
            }
            
            if unique_id in unique_spawn_conditions:
                conditions = unique_spawn_conditions[unique_id]
                if "room_type" in conditions and room_type != conditions["room_type"]:
                    continue
            
            # Create the unique item
            unique_item = get_unique_item(unique_id, x, y, floor)
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
    
    # Placeholder for unique armor creation
    # Will be implemented when we add specific unique items
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
load_unique_items() 