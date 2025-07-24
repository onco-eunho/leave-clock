@echo off

REM Navigate to the project root
pushd "%~dp0"

echo Building application with PyInstaller...
pyinstaller --onefile --windowed --name "leave-clock" --icon "statics/icon.png" --add-data "statics;statics" --add-data ".ini;." main.py

IF %ERRORLEVEL% EQU 0 (
    echo PyInstaller build successful. Moving application...
    REM Move the .exe to the project root
    IF EXIST "dist\leave-clock.exe" (
        move "dist\leave-clock.exe" .
        echo Moved leave-clock.exe to project root.
    ) ELSE (
        echo Could not find built application in dist\.
    )
    echo Cleaning up build files...
    rmdir /s /q build\
    rmdir /s /q dist\
    del "leave-clock.spec"
    echo Cleanup complete.
) ELSE (
    echo PyInstaller build failed.
)

popd

