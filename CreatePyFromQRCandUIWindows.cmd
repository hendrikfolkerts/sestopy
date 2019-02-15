@echo off

REM change in path of the current file
REM d is the drive, p is the path and 0 is the filename of this file (%0 is the filename of the current file)
pushd "%~dp0"

REM icons: convert command .qrc to .py
pyrcc5 -o icons_rc.py icons.qrc

REM pixmaps: convert command .qrc to .py
REM pyrcc5 -o pixmaps_rc.py pixmaps/pixmaps.qrc

REM UI: convert command .ui to .py
pyuic5 -o main_ui.py main_ui.ui