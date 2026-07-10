@echo off
REM Castle Crydee Godot Walkthrough Launcher
REM Double-click to launch the project ready for WASD exploration

setlocal enabledelayedexpansion

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0

REM Path to Godot executable
set GODOT_EXE=%SCRIPT_DIR%Godot_v4.6.2-stable_win64.exe\Godot_v4.6.2-stable_win64.exe

REM Path to the Godot project
set GODOT_PROJECT=%SCRIPT_DIR%godot

REM Launch Godot with the project and the main scene
REM Using --scene to load the walkthrough directly
"%GODOT_EXE%" --path "%GODOT_PROJECT%" --scene "res://scenes/castle_crydee_ground_walkthrough.tscn"

REM If Godot is not found, show error
if errorlevel 1 (
    echo.
    echo ERROR: Could not launch Godot. Make sure:
    echo 1. Godot_v4.6.2-stable_win64.exe folder exists in: %SCRIPT_DIR%
    echo 2. The file is in: %GODOT_EXE%
    echo.
    pause
)
