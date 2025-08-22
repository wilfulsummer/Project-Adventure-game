"""
Mod Loader for Adventure Game
This system allows modders to extend the game without modifying core files.

Modders can:
- Add new unique items
- Add new enemies
- Add new weapons/armor
- Add new commands
- Modify game mechanics
- Add new room types
- Add new spells
- Add custom guide sections

This version is completely localized to avoid conflicts with multiple game versions.
"""

import os
import importlib
import json
from typing import Dict, List, Any, Optional
import sys # Added for exec-based loading

class ModLoader:
    """Main mod loading system - completely localized"""
    
    def __init__(self):
        self.loaded_mods = {}
        self.mod_data = {
            'unique_items': {},
            'enemies': {},
            'weapons': {},
            'armors': {},
            'spells': {},
            'commands': {},
            'room_types': {},
            'hooks': {},
            'guides': {},
            'events': {}  # New event system
        }
        
        # Get the absolute path to THIS mod loader file
        self.this_file_path = os.path.abspath(__file__)
        
        # Check if we're running from a compiled .exe
        if getattr(sys, 'frozen', False):
            # Running from compiled .exe
            self.game_root = os.path.dirname(sys.executable)
            self.mods_directory = os.path.join(self.game_root, "mods")
            print(f"Running from compiled executable: {sys.executable}")
        else:
            # Running from source code
            self.mods_directory = os.path.dirname(self.this_file_path)
            self.game_root = os.path.dirname(self.mods_directory)
            print(f"Running from source code: {self.game_root}")
        
        print(f"Game root: {self.game_root}")
        print(f"Mods directory: {self.mods_directory}")
        
        self.enabled_mods = []
        
        # Create a unique identifier for this game instance
        self.instance_id = f"game_{os.path.basename(self.game_root)}_{hash(self.game_root)}"
        
        print(f"Mod Loader initialized for: {self.game_root}")
        print(f"Instance ID: {self.instance_id}")
    
    def load_mods(self, force_reload=False):
        """Load all available mods"""
        # Check if mods are already loaded to prevent double-loading
        if self.loaded_mods and not force_reload:
            print("Mods already loaded, skipping reload...")
            return
        
        # Check if mods directory exists
        if not os.path.exists(self.mods_directory):
            print(f"Warning: Mods directory not found: {self.mods_directory}")
            print("This is normal when running from source code.")
            print("Mods will be available when running the compiled game.")
            return
            
        if force_reload:
            print("Force reloading mods...")
            self.loaded_mods.clear()
            self.mod_data = {
                'unique_items': {},
                'enemies': {},
                'weapons': {},
                'armors': {},
                'spells': {},
                'commands': {},
                'room_types': {},
                'hooks': {},
                'guides': {}
            }
        else:
            print("Loading mods...")
        
        # Create mods directory if it doesn't exist
        if not os.path.exists(self.mods_directory):
            os.makedirs(self.mods_directory)
            print(f"Created {self.mods_directory} directory")
            return
        
        # Look for mod configuration in THIS mods directory
        mod_config_file = os.path.join(self.mods_directory, "mods.json")
        if os.path.exists(mod_config_file):
            try:
                with open(mod_config_file, 'r') as f:
                    config = json.load(f)
                    self.enabled_mods = config.get('enabled_mods', [])
            except:
                print("Warning: Could not load mods.json, no mods will be loaded")
                return
        else:
            print(f"Warning: No mods.json found in {self.mods_directory}")
            return
        
        # Load each enabled mod
        for mod_name in self.enabled_mods:
            self.load_mod(mod_name)
        
        print(f"Loaded {len(self.loaded_mods)} mod(s)")
    
    def force_reload_mods(self):
        """Force reload all mods (useful for development)"""
        self.load_mods(force_reload=True)
    
    def reload_specific_mod(self, mod_name: str):
        """Reload a specific mod (useful for development)"""
        if mod_name in self.loaded_mods:
            print(f"Reloading mod: {mod_name}")
            # Remove the mod from loaded mods
            del self.loaded_mods[mod_name]
            # Remove mod data
            for data_type in self.mod_data:
                keys_to_remove = [k for k in self.mod_data[data_type] if k.startswith(f"{mod_name}.")]
                for key in keys_to_remove:
                    del self.mod_data[data_type][key]
            # Reload the mod
            self.load_mod(mod_name)
            print(f"Mod {mod_name} reloaded successfully!")
        else:
            print(f"Mod {mod_name} is not currently loaded.")
    
    def auto_reload_changed_mods(self):
        """Automatically reload mods that have changed files (for development)"""
        if not hasattr(self, '_mod_file_timestamps'):
            self._mod_file_timestamps = {}
        
        print("Checking for mod file changes...")
        changed_mods = []
        
        for mod_name in self.loaded_mods:
            mod_path = os.path.join(self.mods_directory, mod_name)
            if not os.path.exists(mod_path):
                continue
            
            # Check if any files have changed
            current_timestamp = self._get_mod_timestamp(mod_path)
            if mod_name not in self._mod_file_timestamps:
                self._mod_file_timestamps[mod_name] = current_timestamp
            elif current_timestamp > self._mod_file_timestamps[mod_name]:
                changed_mods.append(mod_name)
                self._mod_file_timestamps[mod_name] = current_timestamp
        
        # Reload changed mods
        for mod_name in changed_mods:
            print(f"Auto-reloading changed mod: {mod_name}")
            self.reload_specific_mod(mod_name)
        
        if changed_mods:
            print(f"Auto-reloaded {len(changed_mods)} mod(s): {', '.join(changed_mods)}")
        else:
            print("No mods have changed.")
    
    def _get_mod_timestamp(self, mod_path: str) -> float:
        """Get the latest modification time of any file in a mod directory"""
        latest_time = 0
        for root, dirs, files in os.walk(mod_path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    file_time = os.path.getmtime(file_path)
                    latest_time = max(latest_time, file_time)
                except:
                    pass
        return latest_time
    
    def load_mod(self, mod_name: str):
        """Load a specific mod"""
        mod_path = os.path.join(self.mods_directory, mod_name)
        
        if not os.path.exists(mod_path):
            print(f"Warning: Mod '{mod_name}' not found in {mod_path}")
            return
        
        # Check mod dependencies
        if not self.check_mod_dependencies(mod_name, mod_path):
            print(f"Warning: Mod '{mod_name}' has unmet dependencies, skipping...")
            return
        
        # Validate mod structure
        if not self.validate_mod_structure(mod_name, mod_path):
            print(f"Warning: Mod '{mod_name}' has invalid structure, skipping...")
            return
        
        # Look for mod.py file
        mod_file = os.path.join(mod_path, "mod.py")
        if not os.path.exists(mod_file):
            print(f"Warning: Mod '{mod_name}' has no mod.py file")
            return
        
        try:
            # Create a new module namespace
            mod_module = type(sys.modules[__name__])(mod_name)
            
            # Read and execute the mod file
            with open(mod_file, 'r') as f:
                mod_code = f.read()
            
            # Execute the mod code in the module namespace
            exec(mod_code, mod_module.__dict__)
            
            # Register the mod
            self.loaded_mods[mod_name] = mod_module
            
            # Load mod data
            self.load_mod_data(mod_name, mod_module)
            
            print(f"Loaded mod: {mod_name}")
            
        except Exception as e:
            print(f"Error loading mod '{mod_name}': {e}")
    
    def load_mod_data(self, mod_name: str, mod_module):
        """Load data from a mod module"""
        # Load unique items
        if hasattr(mod_module, 'unique_items'):
            for item_id, item_data in mod_module.unique_items.items():
                self.mod_data['unique_items'][f"{mod_name}.{item_id}"] = item_data
        
        # Load enemies
        if hasattr(mod_module, 'enemies'):
            for enemy_id, enemy_data in mod_module.enemies.items():
                self.mod_data['enemies'][f"{mod_name}.{enemy_id}"] = enemy_data
        
        # Load weapons
        if hasattr(mod_module, 'weapons'):
            for weapon_id, weapon_data in mod_module.weapons.items():
                self.mod_data['weapons'][f"{mod_name}.{weapon_id}"] = weapon_data
        
        # Load armors
        if hasattr(mod_module, 'armors'):
            for armor_id, armor_data in mod_module.armors.items():
                self.mod_data['armors'][f"{mod_name}.{armor_id}"] = armor_data
        
        # Load spells
        if hasattr(mod_module, 'spells'):
            for spell_id, spell_data in mod_module.spells.items():
                self.mod_data['spells'][f"{mod_name}.{spell_id}"] = spell_data
        
        # Load commands
        if hasattr(mod_module, 'commands'):
            for cmd_name, cmd_data in mod_module.commands.items():
                self.mod_data['commands'][f"{mod_name}.{cmd_name}"] = cmd_data
        
        # Load room types
        if hasattr(mod_module, 'room_types'):
            for room_type, room_data in mod_module.room_types.items():
                self.mod_data['room_types'][f"{mod_name}.{room_type}"] = room_data
        
        # Load hooks
        if hasattr(mod_module, 'hooks'):
            for hook_name, hook_func in mod_module.hooks.items():
                self.mod_data['hooks'][f"{mod_name}.{hook_name}"] = hook_func
        
        # Load guides
        if hasattr(mod_module, 'guides'):
            for guide_name, guide_data in mod_module.guides.items():
                self.mod_data['guides'][f"{mod_name}.{guide_name}"] = guide_data
        
        # Auto-load guide files from mod directory
        self.load_mod_guide_files(mod_name)
        
        # Auto-load weapon files from mod directory
        self.load_mod_weapon_files(mod_name)
        
        # Auto-load enemy files from mod directory
        self.load_mod_enemy_files(mod_name)
        
        # Auto-load armor files from mod directory
        self.load_mod_armor_files(mod_name)
        
        # Auto-load mod configuration files
        self.load_mod_config_files(mod_name)
    
    def load_mod_guide_files(self, mod_name: str):
        """Automatically load guide files from mod directory for easy guide creation"""
        mod_path = os.path.join(self.mods_directory, mod_name)
        
        # Look for guide.txt file
        guide_file = os.path.join(mod_path, "guide.txt")
        if os.path.exists(guide_file):
            try:
                with open(guide_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                if len(lines) >= 2:  # Need at least guide name + content
                    guide_name = lines[0].strip()
                    guide_content = ''.join(lines[1:]).strip()  # Everything after first line
                    
                    if guide_name and guide_content:
                        # Create a simple guide function that displays the content
                        def create_guide_function(content):
                            def show_guide():
                                print(content)
                            return show_guide
                        
                        # Register the guide automatically
                        guide_id = f"{mod_name}.file_guide"
                        self.mod_data['guides'][guide_id] = {
                            "name": guide_name,
                            "title": f"{guide_name} Guide",
                            "description": f"Guide section: {guide_name}",
                            "function": create_guide_function(guide_content),
                            "requires_permission": False,
                            "source": "file"
                        }
                        
                        print(f"Auto-loaded guide '{guide_name}' from {mod_name}/guide.txt")
                    
            except Exception as e:
                print(f"Warning: Could not load guide file for {mod_name}: {e}")
        
        # Look for guides/ directory with multiple guide files
        guides_dir = os.path.join(mod_path, "guides")
        if os.path.exists(guides_dir) and os.path.isdir(guides_dir):
            try:
                for filename in os.listdir(guides_dir):
                    if filename.endswith('.txt'):
                        guide_file_path = os.path.join(guides_dir, filename)
                        
                        with open(guide_file_path, 'r', encoding='utf-8') as f:
                            lines = f.readlines()
                        
                        if len(lines) >= 2:  # Need at least guide name + content
                            guide_name = lines[0].strip()
                            guide_content = ''.join(lines[1:]).strip()  # Everything after first line
                            
                            if guide_name and guide_content:
                                # Create a guide function for this specific guide
                                def create_guide_function(content):
                                    def show_guide():
                                        print(content)
                                    return show_guide
                                
                                guide_id = f"{mod_name}.{guide_name}"
                                self.mod_data['guides'][guide_id] = {
                                    "name": guide_name,
                                    "title": f"{guide_name} Guide",
                                    "description": f"Guide section: {guide_name}",
                                    "function": create_guide_function(guide_content),
                                    "requires_permission": False,
                                    "source": "file"
                                }
                                
                                print(f"Auto-loaded guide '{guide_name}' from {mod_name}/{filename}")
                            
            except Exception as e:
                print(f"Warning: Could not load guides directory for {mod_name}: {e}")
    
    def load_mod_weapon_files(self, mod_name: str):
        """Automatically load weapon files from mod directory for easy weapon creation"""
        mod_path = os.path.join(self.mods_directory, mod_name)
        
        # Look for weapons/ directory
        weapons_dir = os.path.join(mod_path, "weapons")
        if os.path.exists(weapons_dir) and os.path.isdir(weapons_dir):
            try:
                for filename in os.listdir(weapons_dir):
                    if filename.endswith('.txt'):
                        weapon_file_path = os.path.join(weapons_dir, filename)
                        
                        with open(weapon_file_path, 'r', encoding='utf-8') as f:
                            lines = f.readlines()
                        
                        if len(lines) >= 2:  # Need at least weapon name + one stat
                            weapon_name = lines[0].strip()
                            weapon_data = {"name": weapon_name}
                            
                            # Parse weapon stats from the file
                            for line in lines[1:]:
                                line = line.strip()
                                if ':' in line:
                                    key, value = line.split(':', 1)
                                    key = key.strip().lower()
                                    value = value.strip()
                                    
                                    # Parse different stat types
                                    if key == 'damage':
                                        weapon_data['damage'] = int(value)
                                    elif key == 'durability':
                                        weapon_data['durability'] = int(value)
                                    elif key == 'crit_chance':
                                        weapon_data['crit_chance'] = float(value)
                                    elif key == 'crit_damage':
                                        weapon_data['crit_damage'] = float(value)
                                    elif key == 'mana_cost':
                                        weapon_data['mana_cost'] = int(value)
                                    elif key == 'description':
                                        weapon_data['description'] = value
                            
                            # Set defaults for missing stats
                            if 'damage' not in weapon_data:
                                weapon_data['damage'] = 10
                            if 'durability' not in weapon_data:
                                weapon_data['durability'] = 50
                            if 'crit_chance' not in weapon_data:
                                weapon_data['crit_chance'] = 0.05
                            if 'crit_damage' not in weapon_data:
                                weapon_data['crit_damage'] = 2.0
                            if 'mana_cost' not in weapon_data:
                                weapon_data['mana_cost'] = 0
                            if 'description' not in weapon_data:
                                weapon_data['description'] = f"A custom weapon: {weapon_name}"
                            
                            # Register the weapon
                            weapon_id = f"{mod_name}.{weapon_name.lower().replace(' ', '_')}"
                            self.mod_data['weapons'][weapon_id] = weapon_data
                            
                            print(f"Auto-loaded weapon '{weapon_name}' from {mod_name}/{filename}")
                            
            except Exception as e:
                print(f"Warning: Could not load weapon files for {mod_name}: {e}")
    
    def load_mod_enemy_files(self, mod_name: str):
        """Automatically load enemy files from mod directory for easy enemy creation"""
        mod_path = os.path.join(self.mods_directory, mod_name)
        
        # Look for enemies/ directory
        enemies_dir = os.path.join(mod_path, "enemies")
        if os.path.exists(enemies_dir) and os.path.isdir(enemies_dir):
            try:
                for filename in os.listdir(enemies_dir):
                    if filename.endswith('.txt'):
                        enemy_file_path = os.path.join(enemies_dir, filename)
                        
                        with open(enemy_file_path, 'r', encoding='utf-8') as f:
                            lines = f.readlines()
                        
                        if len(lines) >= 2:  # Need at least enemy name + stats
                            enemy_name = lines[0].strip()
                            enemy_data = {"name": enemy_name}
                            
                            # Parse enemy stats from the file
                            for line in lines[1:]:
                                line = line.strip()
                                if ':' in line:
                                    key, value = line.split(':', 1)
                                    key = key.strip().lower()
                                    value = value.strip()
                                    
                                    # Parse different stat types
                                    if key == 'health':
                                        enemy_data['health'] = int(value)
                                    elif key == 'damage':
                                        enemy_data['damage'] = int(value)
                                    elif key == 'crit_chance':
                                        enemy_data['crit_chance'] = float(value)
                                    elif key == 'crit_damage':
                                        enemy_data['crit_damage'] = float(value)
                                    elif key == 'description':
                                        enemy_data['description'] = value
                            
                            # Set defaults for missing stats
                            if 'health' not in enemy_data:
                                enemy_data['health'] = 100
                            if 'damage' not in enemy_data:
                                enemy_data['damage'] = 10
                            if 'crit_chance' not in enemy_data:
                                enemy_data['crit_chance'] = 0.05
                            if 'crit_damage' not in enemy_data:
                                enemy_data['crit_damage'] = 2.0
                            if 'description' not in enemy_data:
                                enemy_data['description'] = f"A custom enemy: {enemy_name}"
                            
                            # Register the enemy
                            enemy_id = f"{mod_name}.{enemy_name.lower().replace(' ', '_')}"
                            self.mod_data['enemies'][enemy_id] = enemy_data
                            
                            print(f"Auto-loaded enemy '{enemy_name}' from {mod_name}/{filename}")
                            
            except Exception as e:
                print(f"Warning: Could not load enemy files for {mod_name}: {e}")
    
    def load_mod_armor_files(self, mod_name: str):
        """Automatically load armor files from mod directory for easy armor creation"""
        mod_path = os.path.join(self.mods_directory, mod_name)
        
        # Look for armors/ directory
        armors_dir = os.path.join(mod_path, "armors")
        if os.path.exists(armors_dir) and os.path.isdir(armors_dir):
            try:
                for filename in os.listdir(armors_dir):
                    if filename.endswith('.txt'):
                        armor_file_path = os.path.join(armors_dir, filename)
                        
                        with open(armor_file_path, 'r', encoding='utf-8') as f:
                            lines = f.readlines()
                        
                        if len(lines) >= 2:  # Need at least armor name + stats
                            armor_name = lines[0].strip()
                            armor_data = {"name": armor_name}
                            
                            # Parse armor stats from the file
                            for line in lines[1:]:
                                line = line.strip()
                                if ':' in line:
                                    key, value = line.split(':', 1)
                                    key = key.strip().lower()
                                    value = value.strip()
                                    
                                    # Parse different stat types
                                    if key == 'defense':
                                        armor_data['defense'] = int(value)
                                    elif key == 'durability':
                                        armor_data['durability'] = int(value)
                                    elif key == 'description':
                                        armor_data['description'] = value
                            
                            # Set defaults for missing stats
                            if 'defense' not in armor_data:
                                armor_data['defense'] = 10
                            if 'durability' not in armor_data:
                                armor_data['durability'] = 50
                            if 'description' not in armor_data:
                                armor_data['description'] = f"A custom armor: {armor_name}"
                            
                            # Register the armor
                            armor_id = f"{mod_name}.{armor_name.lower().replace(' ', '_')}"
                            self.mod_data['armors'][armor_id] = armor_data
                            
                            print(f"Auto-loaded armor '{armor_name}' from {mod_name}/{filename}")
                            
            except Exception as e:
                print(f"Warning: Could not load armor files for {mod_name}: {e}")
    
    def load_mod_config_files(self, mod_name: str):
        """Automatically load mod-specific configuration files (e.g., mod.json)"""
        mod_path = os.path.join(self.mods_directory, mod_name)
        
        # Look for mod.json file
        config_file = os.path.join(mod_path, "mod.json")
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    config_data = json.load(f)
                    # Merge config data into mod_data
                    for key, value in config_data.items():
                        if key.startswith(f"{mod_name}."):
                            self.mod_data[key.replace(f"{mod_name}.", '')][key] = value
                        else:
                            self.mod_data[key] = value # Handle global config
                print(f"Loaded mod-specific config from {mod_name}/mod.json")
            except Exception as e:
                print(f"Warning: Could not load mod.json for {mod_name}: {e}")
        
        # Look for config/ directory with multiple config files
        config_dir = os.path.join(mod_path, "config")
        if os.path.exists(config_dir) and os.path.isdir(config_dir):
            try:
                for filename in os.listdir(config_dir):
                    if filename.endswith('.json'):
                        config_file_path = os.path.join(config_dir, filename)
                        
                        with open(config_file_path, 'r') as f:
                            config_data = json.load(f)
                            # Merge config data into mod_data
                            for key, value in config_data.items():
                                if key.startswith(f"{mod_name}."):
                                    self.mod_data[key.replace(f"{mod_name}.", '')][key] = value
                                else:
                                    self.mod_data[key] = value # Handle global config
                        print(f"Loaded mod-specific config from {mod_name}/{filename}")
                            
            except Exception as e:
                print(f"Warning: Could not load config directory for {mod_name}: {e}")
    
    def get_unique_item(self, item_id: str) -> Optional[Dict[str, Any]]:
        """Get a unique item from mods"""
        return self.mod_data['unique_items'].get(item_id)
    
    def get_enemy(self, enemy_id: str) -> Optional[Dict[str, Any]]:
        """Get an enemy from mods"""
        return self.mod_data['enemies'].get(enemy_id)
    
    def get_weapon(self, weapon_id: str) -> Optional[Dict[str, Any]]:
        """Get a weapon from mods"""
        return self.mod_data['weapons'].get(weapon_id)
    
    def get_armor(self, armor_id: str) -> Optional[Dict[str, Any]]:
        """Get an armor from mods"""
        return self.mod_data['armors'].get(armor_id)
    
    def get_spell(self, spell_id: str) -> Optional[Dict[str, Any]]:
        """Get a spell from mods"""
        return self.mod_data['spells'].get(spell_id)
    
    def get_command(self, cmd_name: str) -> Optional[Dict[str, Any]]:
        """Get a command from mods"""
        return self.mod_data['commands'].get(cmd_name)
    
    def get_room_type(self, room_type: str) -> Optional[Dict[str, Any]]:
        """Get a room type from mods"""
        return self.mod_data['room_types'].get(room_type)
    
    def call_hook(self, hook_name: str, *args, **kwargs):
        """Call a mod hook function"""
        hook_func = self.mod_data['hooks'].get(hook_name)
        if hook_func:
            try:
                return hook_func(*args, **kwargs)
            except Exception as e:
                print(f"Error calling hook '{hook_name}': {e}")
        return None
    
    def register_event(self, event_name: str, handler_func, mod_name: str):
        """Register an event handler for a specific event"""
        if event_name not in self.mod_data['events']:
            self.mod_data['events'][event_name] = []
        
        self.mod_data['events'][event_name].append({
            'handler': handler_func,
            'mod': mod_name
        })
        print(f"Registered event handler for '{event_name}' from mod '{mod_name}'")
    
    def trigger_event(self, event_name: str, *args, **kwargs):
        """Trigger an event and call all registered handlers"""
        if event_name in self.mod_data['events']:
            print(f"Triggering event: {event_name}")
            results = []
            for handler_info in self.mod_data['events'][event_name]:
                try:
                    result = handler_info['handler'](*args, **kwargs)
                    results.append(result)
                except Exception as e:
                    print(f"Error in event handler for '{event_name}' from mod '{handler_info['mod']}': {e}")
            return results
        return []
    
    def call_startup_hooks(self):
        """Call startup hooks for all mods - this can ask for user input"""
        print("Calling mod startup hooks...")
        for mod_name in self.loaded_mods:
            startup_hook = self.mod_data['hooks'].get(f"{mod_name}.startup")
            if startup_hook:
                try:
                    print(f"Running startup hook for {mod_name}...")
                    startup_hook()
                except Exception as e:
                    print(f"Error in startup hook for {mod_name}: {e}")
        print("Startup hooks completed.")
    
    def get_mod_guides(self) -> Dict[str, Any]:
        """Get all registered mod guide sections"""
        return self.mod_data['guides']
    
    def has_mod_guide(self, mod_name: str) -> bool:
        """Check if a mod has registered a guide section"""
        return f"{mod_name}.guide" in self.mod_data['guides']
    
    def get_mod_guide(self, mod_name: str) -> Optional[Any]:
        """Get a specific mod's guide section"""
        return self.mod_data['guides'].get(f"{mod_name}.guide")
    
    def list_mods(self) -> List[str]:
        """List all loaded mods"""
        return list(self.loaded_mods.keys())
    
    def get_mod_info(self, mod_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific mod"""
        if mod_name in self.loaded_mods:
            mod_module = self.loaded_mods[mod_name]
            return {
                'name': mod_name,
                'version': getattr(mod_module, 'version', 'Unknown'),
                'author': getattr(mod_module, 'author', 'Unknown'),
                'description': getattr(mod_module, 'description', 'No description'),
                'unique_items': len([k for k in self.mod_data['unique_items'] if k.startswith(f"{mod_name}.")]),
                'enemies': len([k for k in self.mod_data['enemies'] if k.startswith(f"{mod_name}.")]),
                'weapons': len([k for k in self.mod_data['weapons'] if k.startswith(f"{mod_name}.")]),
                'armors': len([k for k in self.mod_data['armors'] if k.startswith(f"{mod_name}.")]),
                'spells': len([k for k in self.mod_data['spells'] if k.startswith(f"{mod_name}.")]),
                'commands': len([k for k in self.mod_data['commands'] if k.startswith(f"{mod_name}.")]),
            }
        return None
    
    def get_instance_info(self) -> Dict[str, Any]:
        """Get information about this mod loader instance"""
        return {
            'instance_id': self.instance_id,
            'game_root': self.game_root,
            'mods_directory': self.mods_directory,
            'this_file': self.this_file_path,
            'loaded_mods_count': len(self.loaded_mods),
            'mods_available': os.path.exists(self.mods_directory),
            'is_compiled': getattr(sys, 'frozen', False)
        }
    
    def are_mods_available(self) -> bool:
        """Check if mods are available (either from source or compiled)"""
        return os.path.exists(self.mods_directory)
    
    def get_mods_status(self) -> str:
        """Get a human-readable status of mod availability"""
        if getattr(sys, 'frozen', False):
            if os.path.exists(self.mods_directory):
                return "Available (compiled game with mods)"
            else:
                return "Not found (compiled game missing mods folder)"
        else:
            if os.path.exists(self.mods_directory):
                return "Available (source code with mods)"
            else:
                return "Not available (source code without mods)"
    
    def validate_mod_structure(self, mod_name: str, mod_path: str) -> bool:
        """Validate that a mod has the correct structure"""
        required_files = ["mod.py"]
        optional_dirs = ["weapons", "guides", "enemies", "armors", "config"]
        optional_files = ["mod.json", "guide.txt", "README.md"]
        
        print(f"  Validating mod structure for {mod_name}...")
        
        # Check required files
        for required_file in required_files:
            if not os.path.exists(os.path.join(mod_path, required_file)):
                print(f"  ❌ Missing required file: {required_file}")
                return False
            else:
                print(f"  ✅ Found required file: {required_file}")
        
        # Check for valid optional directories and files
        found_items = []
        for item in os.listdir(mod_path):
            item_path = os.path.join(mod_path, item)
            if os.path.isdir(item_path):
                if item in optional_dirs:
                    print(f"  ✅ Found optional directory: {item}/")
                    found_items.append(item)
                else:
                    print(f"  ⚠️  Unknown directory: {item}/ (will be ignored)")
            elif os.path.isfile(item_path):
                if item in optional_files:
                    print(f"  ✅ Found optional file: {item}")
                    found_items.append(item)
        
        if found_items:
            print(f"  📁 Mod has {len(found_items)} optional components: {', '.join(found_items)}")
        
        return True
    
    def check_mod_dependencies(self, mod_name: str, mod_path: str) -> bool:
        """Check if a mod's dependencies are met"""
        # Look for dependencies.json file
        deps_file = os.path.join(mod_path, "dependencies.json")
        if not os.path.exists(deps_file):
            return True  # No dependencies specified
        
        try:
            with open(deps_file, 'r') as f:
                deps_data = json.load(f)
            
            required_mods = deps_data.get('required_mods', [])
            if not required_mods:
                return True  # No dependencies specified
            
            print(f"  📋 Checking dependencies for {mod_name}...")
            missing_deps = []
            
            for required_mod in required_mods:
                if required_mod not in self.loaded_mods:
                    missing_deps.append(required_mod)
                    print(f"    ❌ Missing dependency: {required_mod}")
                else:
                    print(f"    ✅ Found dependency: {required_mod}")
            
            if missing_deps:
                print(f"  ❌ Mod {mod_name} cannot load - missing dependencies: {', '.join(missing_deps)}")
                return False
            
            print(f"  ✅ All dependencies satisfied for {mod_name}")
            return True
            
        except Exception as e:
            print(f"  ⚠️  Warning: Could not check dependencies for {mod_name}: {e}")
            return True  # Continue loading if dependency check fails

# Global mod loader instance
mod_loader = ModLoader()

# Convenience functions for modders
def register_unique_item(item_id: str, item_data: Dict[str, Any]):
    """Register a unique item (for use in mods)"""
    mod_loader.mod_data['unique_items'][item_id] = item_data

def register_enemy(enemy_id: str, enemy_data: Dict[str, Any]):
    """Register an enemy (for use in mods)"""
    mod_loader.mod_data['enemies'][enemy_id] = enemy_data

def register_weapon(weapon_id: str, weapon_data: Dict[str, Any]):
    """Register a weapon (for use in mods)"""
    mod_loader.mod_data['weapons'][weapon_id] = weapon_data

def register_armor(armor_id: str, armor_data: Dict[str, Any]):
    """Register an armor (for use in mods)"""
    mod_loader.mod_data['armors'][armor_id] = armor_data

def register_spell(spell_id: str, spell_data: Dict[str, Any]):
    """Register a spell (for use in mods)"""
    mod_loader.mod_data['spells'][spell_id] = spell_data

def register_command(cmd_name: str, cmd_data: Dict[str, Any]):
    """Register a command (for use in mods)"""
    mod_loader.mod_data['commands'][cmd_name] = cmd_data

def register_room_type(room_type: str, room_data: Dict[str, Any]):
    """Register a room type (for use in mods)"""
    mod_loader.mod_data['room_types'][room_type] = room_data

def register_hook(hook_name: str, hook_func):
    """Register a hook function (for use in mods)"""
    mod_loader.mod_data['hooks'][hook_name] = hook_func

def register_guide(guide_name: str, guide_data: Dict[str, Any]):
    """Register a guide section (for use in mods)"""
    mod_loader.mod_data['guides'][guide_name] = guide_data

# Flag to prevent auto-loading during testing
_auto_load_enabled = True

def disable_auto_load():
    """Disable automatic mod loading (useful for testing)"""
    global _auto_load_enabled
    _auto_load_enabled = False

def enable_auto_load():
    """Enable automatic mod loading"""
    global _auto_load_enabled
    _auto_load_enabled = True

# Only auto-load if not disabled (prevents issues during testing)
if _auto_load_enabled:
    try:
        mod_loader.load_mods()
    except Exception as e:
        print(f"Warning: Could not auto-load mods: {e}")
        # Don't fail if mods can't be loaded
