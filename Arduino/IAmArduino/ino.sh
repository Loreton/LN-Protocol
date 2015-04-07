#!/bin/bash

BOARD='nano328'
USB='/dev/Arduino3'

echo "ino build -m $BOARD
echo  ino upload -m n $BOARD -p $USB
echo  ino serial -p $USB
