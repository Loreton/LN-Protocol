#!/bin/bash
# https://forum.arduino.cc/index.php?topic=397017.0
ECHO Creating hexadecimal binary files of ATmel328P contents...
avrdude -CC:\PROGRA~2\Arduino/hardware/tools/avr/etc/avrdude.conf -c usbasp -P usb -p ATMEGA328P -b 115200 -U flash:w:c:\x\z\backup_flash.hex:i
avrdude -CC:\PROGRA~2\Arduino/hardware/tools/avr/etc/avrdude.conf -c usbasp -P usb -p ATMEGA328P -b 115200 -U hfuse:w:c:\x\z\backup_hfuse.hex:i
avrdude -CC:\PROGRA~2\Arduino/hardware/tools/avr/etc/avrdude.conf -c usbasp -P usb -p ATMEGA328P -b 115200 -U lfuse:w:c:\x\z\backup_lfuse.hex:i

avrdude -CC:\PROGRA~2\Arduino/hardware/tools/avr/etc/avrdude.conf -c usbasp -P usb -p ATMEGA328P -b 115200 -U efuse:w:c:\x\z\backup_efuse.hex:i





CONFIG_FILE='/opt/arduino-1.8.1/hardware/tools/avr/etc/avrdude.conf'
avrdude -C $CONFIG_FILE -c usbasp -P usb -p ATMEGA328P -b 115200 -U efuse:w:c:\x\z\backup_efuse.hex:i



avr-objdump -j .sec1 -d -m avr5 yourFileHere.hex