# Bug Reports Folder

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
