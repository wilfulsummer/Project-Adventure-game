#!/usr/bin/env python3
"""
Bug Reporting System for Adventure Game
Automatically generates bug reports when errors occur
"""

import os
import sys
import traceback
import datetime
import json
from pathlib import Path

# Bug reports directory
BUG_REPORTS_DIR = "bug_reports"

def ensure_bug_reports_directory():
    """Ensure the bug reports directory exists"""
    if not os.path.exists(BUG_REPORTS_DIR):
        os.makedirs(BUG_REPORTS_DIR)

def generate_bug_report(error, error_type, error_value, traceback_info, game_state=None):
    """Generate a comprehensive bug report"""
    ensure_bug_reports_directory()
    
    # Create timestamp for filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"bug_report_{timestamp}.txt"
    filepath = os.path.join(BUG_REPORTS_DIR, filename)
    
    # Get system information
    system_info = {
        "python_version": sys.version,
        "platform": sys.platform,
        "executable": sys.executable,
        "cwd": os.getcwd()
    }
    
    # Create bug report content
    bug_report = f"""=== ADVENTURE GAME BUG REPORT ===
Generated: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

ERROR DETAILS:
Type: {error_type.__name__}
Value: {error_value}
Description: {str(error)}

TRACEBACK:
{traceback_info}

SYSTEM INFORMATION:
Python Version: {system_info['python_version']}
Platform: {system_info['platform']}
Executable: {system_info['executable']}
Working Directory: {system_info['cwd']}

GAME STATE (if available):
{json.dumps(game_state, indent=2) if game_state else "No game state captured"}

INSTRUCTIONS FOR PLAYER:
1. This bug report has been saved to: {filepath}
2. Please describe what you were doing when this error occurred
3. Include any relevant details about your game progress
4. You can find this file in the 'bug_reports' folder
5. Consider sharing this report with the game developers

INSTRUCTIONS FOR DEVELOPER:
1. Check the traceback above for the error location
2. Review the game state to understand the context
3. Test the specific scenario that caused this error
4. Fix the issue and update the game

Thank you for helping improve the game!
==============================================="""
    
    # Save bug report to file
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(bug_report)
        return filepath, bug_report
    except Exception as e:
        # If we can't save the file, return just the content
        return None, f"Could not save bug report: {e}\n\n{bug_report}"

def display_bug_report(bug_report_content):
    """Display the bug report on screen for the player"""
    print("\n" + "="*60)
    print("🐛 BUG REPORT GENERATED 🐛")
    print("="*60)
    print(bug_report_content)
    print("="*60)
    print("🐛 END OF BUG REPORT 🐛")
    print("="*60)

def handle_error_with_report(error, error_type, error_value, traceback_info, game_state=None):
    """Main function to handle errors and generate reports"""
    print(f"\n❌ An error occurred: {error_type.__name__}: {error_value}")
    print("📝 Generating bug report...")
    
    # Generate bug report
    filepath, bug_report_content = generate_bug_report(
        error, error_type, error_value, traceback_info, game_state
    )
    
    # Display on screen
    display_bug_report(bug_report_content)
    
    if filepath:
        print(f"📁 Bug report saved to: {filepath}")
    else:
        print("⚠️  Could not save bug report file, but content displayed above")
    
    print("\n💡 The game will attempt to continue. If problems persist, please restart.")
    return filepath

def manual_bug_report(error, context="Unknown", game_state=None):
    """Manually trigger a bug report for caught exceptions"""
    error_type = type(error)
    error_value = str(error)
    traceback_info = ''.join(traceback.format_tb(error.__traceback__))
    
    print(f"\n🐛 Manual bug report triggered from: {context}")
    return handle_error_with_report(error, error_type, error_value, traceback_info, game_state)

def capture_game_state():
    """Capture current game state for bug reports"""
    try:
        # Import main game variables (this might fail if called from wrong context)
        import main
        game_state = {
            "player_position": f"Floor {getattr(main, 'player_floor', 'Unknown')}, ({getattr(main, 'player_x', 'Unknown')}, {getattr(main, 'player_y', 'Unknown')})",
            "player_stats": {
                "hp": getattr(main, 'player_hp', 'Unknown'),
                "max_hp": getattr(main, 'player_max_hp', 'Unknown'),
                "stamina": getattr(main, 'player_stamina', 'Unknown'),
                "mana": getattr(main, 'player_mana', 'Unknown')
            },
            "inventory_count": len(getattr(main, 'inventory', [])),
            "armor_count": len(getattr(main, 'armor_inventory', [])),
            "current_command": "Unknown"
        }
        return game_state
    except Exception:
        return {"error": "Could not capture game state"}

def setup_global_exception_handler():
    """Set up a global exception handler for uncaught errors"""
    def global_exception_handler(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            # Don't handle keyboard interrupts
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        
        # Generate bug report
        traceback_str = ''.join(traceback.format_tb(exc_traceback))
        game_state = capture_game_state()
        
        handle_error_with_report(
            exc_value, exc_type, exc_value, traceback_str, game_state
        )
        
        # Continue with normal exception handling
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
    
    sys.excepthook = global_exception_handler

def create_bug_reports_readme():
    """Create a README file explaining the bug reports folder"""
    readme_content = """# Bug Reports Folder

This folder contains automatically generated bug reports when errors occur in the game.

## What happens when a bug occurs:

1. **Automatic Detection**: The game detects an error or exception
2. **Report Generation**: A detailed bug report is created with:
   - Error details and traceback
   - System information
   - Game state at time of error
   - Timestamp and unique filename
3. **On-Screen Display**: The bug report is shown to the player
4. **File Storage**: Report is saved to this folder

## File Naming Convention:
- `bug_report_YYYYMMDD_HHMMSS.txt`
- Example: `bug_report_20241201_143022.txt`

## What's in each report:
- **Error Details**: Type, value, and description
- **Full Traceback**: Exact location of the error
- **System Info**: Python version, platform, etc.
- **Game State**: Player position, stats, inventory
- **Instructions**: For both players and developers

## For Players:
- Reports are automatically generated
- You can find them in this folder
- Include them when reporting bugs to developers
- They help developers fix issues faster

## For Developers:
- Check traceback for error location
- Review game state for context
- Test the specific scenario
- Fix the underlying issue

## Note:
- This folder is committed to git for transparency
- Individual bug report files are ignored by git
- Only the folder structure is tracked
"""
    
    readme_path = os.path.join(BUG_REPORTS_DIR, "README.md")
    try:
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        return readme_path
    except Exception:
        return None

# Initialize the bug reporting system
if __name__ == "__main__":
    # Create the bug reports directory and README
    ensure_bug_reports_directory()
    create_bug_reports_readme()
    print(f"Bug reporting system initialized. Directory: {BUG_REPORTS_DIR}")
else:
    # When imported, ensure directory exists
    ensure_bug_reports_directory()
