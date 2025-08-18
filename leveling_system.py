"""
Leveling System for Adventure Game
Handles XP calculations, leveling up, and stat bonuses
"""

import math

def calculate_xp_reward(enemy_name, enemy_x, enemy_y, enemy_floor):
    """
    Calculate XP reward for defeating an enemy
    XP scales with distance from (0,0) and floor level
    """
    # Base XP for different enemy types
    base_xp = {
        "Training Dummy": 5,
        "Rat": 8,
        "Hungry Wolf": 12,
        "Orc": 15,
        "Troll": 75,  # Buffed from 25 to 75 (3x increase)
        "Example Boss": 30
    }
    
    # Get base XP for this enemy type, default to 10 if unknown
    xp = base_xp.get(enemy_name, 10)
    
    # Scale XP with distance from (0,0) - more XP for enemies further away
    distance = abs(enemy_x) + abs(enemy_y)
    distance_multiplier = 1 + (distance / 100)  # +1% per 100 distance, caps at +100%
    distance_multiplier = min(distance_multiplier, 2.0)  # Cap at 2x
    
    # Scale XP with floor level - higher floors give more XP
    floor_multiplier = 1 + (enemy_floor - 1) * 0.2  # +20% per floor
    
    # Calculate final XP
    final_xp = int(xp * distance_multiplier * floor_multiplier)
    
    return max(1, final_xp)  # Minimum 1 XP

def calculate_xp_to_next_level(current_level):
    """
    Calculate XP needed for next level
    Uses a scaling formula: base * (level ^ 1.5)
    """
    if current_level >= 100:
        return 0  # Max level reached
    
    base_xp = 100
    xp_needed = int(base_xp * (current_level ** 1.5))
    return xp_needed

def add_xp_and_level_up(current_xp, current_level, current_hp, current_max_hp):
    """
    Add XP and handle leveling up
    Returns: (new_xp, new_level, new_hp, new_max_hp, levels_gained, xp_to_next, skill_points_gained)
    """
    xp_to_next = calculate_xp_to_next_level(current_level)
    levels_gained = 0
    skill_points_gained = 0
    new_xp = current_xp
    new_level = current_level
    new_hp = current_hp
    new_max_hp = current_max_hp
    
    # Check if we can level up
    while new_xp >= xp_to_next and new_level < 100:
        new_xp -= xp_to_next
        new_level += 1
        levels_gained += 1
        skill_points_gained += 1  # +1 skill point per level
        
        # Apply level up bonuses
        new_max_hp += 2  # +2 max HP per level
        new_hp += 1      # +1 current HP per level
        
        # Calculate XP needed for next level
        xp_to_next = calculate_xp_to_next_level(new_level)
    
    return new_xp, new_level, new_hp, new_max_hp, levels_gained, xp_to_next, skill_points_gained

def get_level_progress(current_xp, current_level):
    """
    Get level progress information
    Returns: (current_xp, xp_needed, progress_percentage)
    """
    xp_needed = calculate_xp_to_next_level(current_level)
    if xp_needed == 0:
        return current_xp, 0, 100.0  # Max level
    
    progress = (current_xp / xp_needed) * 100
    return current_xp, xp_needed, progress

def get_level_bonuses(level):
    """
    Calculate total bonuses from leveling up
    Returns: (total_hp_bonus, total_max_hp_bonus)
    """
    if level <= 1:
        return 0, 0
    
    # Level 1 gives no bonuses, so subtract 1 from level
    effective_levels = level - 1
    total_hp_bonus = effective_levels * 1      # +1 HP per level
    total_max_hp_bonus = effective_levels * 2  # +2 max HP per level
    
    return total_hp_bonus, total_max_hp_bonus
