#!/bin/bash

export PYSDL2_DLL_PATH="/mnt/sdcard/Persistent/portmaster/site-packages/sdl2dll/dll"

killall -STOP MainUI
/mnt/sdcard/spruce/flip/bin/python3 mainui.py
killall -CONT MainUI
