#!/bin/bash
action=$1
VERBOSE=-v
VERBOSE=
# device=/dev/ttyUSB0
device=$2
if [[ "$device" = "" ]]; then
    echo "immettere l'azione ed il device da programmare:"
    echo "azione: (anche più di uno senza spazi intermedi)"
    echo "      b - build"
    echo "      c - clear"
    echo "      s - read serial"
    echo "      u - upload"
    echo
    echo "device:"
    echo "      Es. /dev/ttyUSB0"
    echo
    exit
fi

function creaLink() {
    ln -s /home/pi/485d_Loreto/Arduino/LnLibraries/LnFunctions      /home/pi/485d_Loreto/Arduino/rs485-Full/lib/LnFunctions
    ln -s /home/pi/485d_Loreto/Arduino/LnLibraries/RS485_protocol   /home/pi/485d_Loreto/Arduino/rs485-Full/lib/RS485_protocol
}

function deleteLink() {
    rm -f /home/pi/485d_Loreto/Arduino/rs485-Full/lib/LnFunctions
    rm -f /home/pi/485d_Loreto/Arduino/rs485-Full/lib/RS485_protocol
}


#cleam
if [[ "$action" =~ "c" ]]; then
    echo "------"
    echo "CLEAN"
    echo "------"
    echo
    platformio run --target clean
fi

#build
creaLink
if [[ "$action" =~ "b" ]]; then
    echo "------"
    echo "BUILD"
    echo "------"
    echo
    platformio run  --environment nano
fi

#upload
if [[ "$action" =~ "u" ]]; then
    echo "------"
    echo "UPLOAD"
    echo "------"
    echo
    platformio run --target upload --upload-port $device
fi
deleteLink


#monitor
if [[ "$action" =~ "s" ]]; then
    echo "------"
    echo "MONITOR"
    echo "------"
    echo
    platformio device monitor -p $device
fi