# 🚀 Automated Game Releases

## How It Works

This repository uses **GitHub Actions** to automatically build and release new versions of the game whenever you push a version tag.

## 🏷️ Creating a New Release

### 1. Tag Your Version
```bash
git tag v1.1.0
git push origin v1.1.0
```

### 2. What Happens Automatically
- ✅ **GitHub Actions triggers** the build pipeline
- ✅ **Game compiles** into `Adventure_Game.exe`
- ✅ **Release created** with executable and assets
- ✅ **Downloadable** from GitHub Releases page

## 📥 Getting the Latest Version

### Option 1: GitHub Releases Page
1. Go to [Releases](https://github.com/wilfulsummer/Project-Adventure-game/releases)
2. Download the latest `Adventure_Game.exe`
3. Run the game!

### Option 2: Use the Download Script
1. Run `download_latest.bat` (Windows)
2. Follow the instructions to get the latest version

## 🔧 Build Process

The pipeline automatically:
- **Installs Python 3.9** on Windows
- **Installs PyInstaller** for compilation
- **Builds single-file executable** (`--onefile --windowed`)
- **Creates release assets** with README and executable
- **Uploads to GitHub Releases** with auto-generated notes

## 📋 Release Assets

Each release includes:
- `Adventure_Game.exe` - The game executable
- `README.md` - Game documentation
- `LICENSE` - License file (if present)
- **Auto-generated release notes** from commit history

## 🎯 Benefits

- **Always up-to-date** - No more old .exe versions
- **Automatic builds** - No manual compilation needed
- **Professional releases** - Consistent release process
- **Easy distribution** - Users can always get the latest version

## 🚨 Important Notes

- **Only triggers on version tags** (`v*` pattern)
- **Requires GitHub Actions permissions** to be enabled
- **Builds on Windows** to ensure .exe compatibility
- **Uses PyInstaller** for reliable executable creation

---

**Happy Gaming! 🎮✨**
