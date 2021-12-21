#!/usr/bin/env sh

bluetoothctl -- remove FF:FF:A0:45:AA:A0
bluetoothctl -- remove BE:FF:A0:04:B4:6F

sleep 3

#python3 ./main.py
python3 ./test.py
