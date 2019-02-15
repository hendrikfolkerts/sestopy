#!/bin/bash
# go to directory of this script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR
# icons to py
pyrcc5 -o icons_rc.py icons.qrc
# ui to py
pyuic5 -o main_ui.py main_ui.ui
