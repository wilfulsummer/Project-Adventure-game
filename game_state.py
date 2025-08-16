# --- Game State ---
worlds = {}  # Dictionary of floors: {floor: world}
player_floor = 1
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
waypoint_scrolls = 1  # Can hold up to 3 waypoint scrolls
mysterious_keys = {}  # Dictionary of floor-specific mysterious keys: {floor: True}
golden_keys = 0  # Can hold up to 3 golden keys
unlocked_floors = set()  # Set of floors that can be accessed with mysterious keys
waypoints = {}  # Dictionary to store waypoints: {name: (floor, x, y)}
discovered_enemies = set()  # Track which enemies have been defeated
learned_spells = []  # List of learned spells in order
spell_scrolls = {}  # Dictionary of spell scrolls: {spell_name: count}
using_fists = False  # Track if player is using fists instead of weapons

# --- Leveling System ---
player_level = 1
player_xp = 0
player_xp_to_next = 100
max_level = 100

# --- Statistics Tracking ---
enemies_defeated = 0
bosses_defeated = 0
total_damage_dealt = 0
total_damage_taken = 0
critical_hits = 0
attack_count = 0
rooms_explored = 0
floors_visited = set()
move_count = 0
items_collected = 0
weapons_broken = 0
gold_earned = 0 