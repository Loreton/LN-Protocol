#!/bin/bash

# rm -f lib/LnFunctions
# rm -f lib/RS485_protocol
cd /home/pi/GIT-REPO/HW-Projects/LnProtocol/Arduino-code/pio-Rs485-Slave

ln -s /home/pi/GIT-REPO/HW-Projects/LnProtocol/LnLibraries/LnFunctions    lib/LnFunctions
ln -s /home/pi/GIT-REPO/HW-Projects/LnProtocol/LnLibraries/RS485_protocol lib/RS485_protocol

# platformio run

# Change directory to example

# Build project
platformio run --environment nano

# Upload firmware
platformio run --target upload

# Build specific environment
# --- platformio run -e flora8

# Upload firmware for the specific environment
# --- platformio run -e flora8 --target upload

# Clean build files
# --- platformio run --target clean

function comandiVari {
    platformio device list
    platformio device monitor
    platformio devise monitor -p /dev/ttyUSBx
}