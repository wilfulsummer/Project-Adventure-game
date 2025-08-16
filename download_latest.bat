@echo off
echo ========================================
echo Adventure Game - Latest Version Downloader
echo ========================================
echo.

echo Downloading latest version from GitHub...
echo.

REM Get the latest release info
curl -s "https://api.github.com/repos/wilfulsummer/Project-Adventure-game/releases/latest" > release_info.json

REM Extract download URL (this is a simplified version)
echo Latest release information downloaded.
echo.
echo Please visit: https://github.com/wilfulsummer/Project-Adventure-game/releases
echo.
echo Download the latest Adventure_Game.exe from there.
echo.
pause
