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
    "An underground tunnel that echoes your steps.",
    "A mineshaft with bones and dust litted around the walls.",
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