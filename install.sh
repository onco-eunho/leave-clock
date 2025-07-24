#!/bin/bash

# Navigate to the project root
cd "$(dirname "$0")"

echo "Building application with PyInstaller..."
pyinstaller --onefile --windowed --name "leave-clock" --icon "statics/icon.png" --add-data "statics:statics" --add-data ".ini:." main.py

# Check if build was successful
if [ $? -eq 0 ]; then
    echo "PyInstaller build successful. Moving application..."
    # Move the .app bundle (macOS) or executable (Linux) to the project root
    if [ -d "dist/leave-clock.app" ]; then
        mv "dist/leave-clock.app" .
        echo "Moved leave-clock.app to project root."
    elif [ -f "dist/leave-clock" ]; then
        mv "dist/leave-clock" .
        echo "Moved leave-clock executable to project root."
    else
        echo "Could not find built application in dist/."
    fi
    echo "Cleaning up build files..."
    rm -rf build/
    rm -rf dist/
    rm -f "leave-clock.spec"
    echo "Cleanup complete."
else
    echo "PyInstaller build failed."
fi
