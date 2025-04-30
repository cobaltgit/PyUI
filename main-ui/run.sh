#!/bin/bash

export PYSDL2_DLL_PATH="/mnt/sdcard/Persistent/portmaster/site-packages/sdl2dll/dll"
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/usr/miyoo/lib"
killall -STOP MainUI
/mnt/sdcard/spruce/flip/bin/python3 MainUI.py
killall -CONT MainUI
