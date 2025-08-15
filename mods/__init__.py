# Mods package for Adventure Game
# This allows modders to extend the game without modifying core files

# Import all available mods
from . import mod_loader

# Make mod_loader available at package level
__all__ = ['mod_loader']
