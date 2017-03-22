#!/bin/bash
# https://forum.arduino.cc/index.php?topic=397017.0
# ECHO Creating hexadecimal binary files of ATmel328P contents...
# avrdude -CC:\PROGRA~2\Arduino/hardware/tools/avr/etc/avrdude.conf -c usbasp -P usb -p ATMEGA328P -b 115200 -U flash:w:c:\x\z\backup_flash.hex:i
# avrdude -CC:\PROGRA~2\Arduino/hardware/tools/avr/etc/avrdude.conf -c usbasp -P usb -p ATMEGA328P -b 115200 -U hfuse:w:c:\x\z\backup_hfuse.hex:i
# avrdude -CC:\PROGRA~2\Arduino/hardware/tools/avr/etc/avrdude.conf -c usbasp -P usb -p ATMEGA328P -b 115200 -U lfuse:w:c:\x\z\backup_lfuse.hex:i
# avrdude -CC:\PROGRA~2\Arduino/hardware/tools/avr/etc/avrdude.conf -c usbasp -P usb -p ATMEGA328P -b 115200 -U efuse:w:c:\x\z\backup_efuse.hex:i

# Explanation for command
# avrdude –c usbasp –p m16 –u –U flash:w:io.hex
#   -c : Indicates the programmer type. Since we are using the USBasp programmer, argument “usbasp” is mentioned.
#   -p : Processor. We are using ATmega16, hence “m16”. Note ATmega16 has two variants, one is “ATmega16L” (slow speed version) and “ATmega16” normal 16MHz version. However their device signature is same and hence you will have to use “m16” as parameter for both the AVRs. This applies to all AVRs having “L” variants.
#   -u : Disables the default behavior of reading out the fuses three times before programming, then verifying at the end of programming that the fuses have not changed. Always use this option. Many times it happens that we forget to switch on the AVR’s +5V power supply, then at the end of programming cycle, avrdude detects inconsistent fuses and tries to reprogram them. Since there is no power supply, fuses gets programmed incorrectly and entire microcontroller gets screwed up(means becomes useless). Thus always use this option.
#   -U  :  memtype:op:filename[:format]
#
# Perform a memory operation. Multiple ‘-U’ options can be speciﬁed in order to operate on multiple memories on the same command-line invocation.
#
#     memtype
#
#     The memtype ﬁeld speciﬁes the memory type to operate on.
#
#     calibration   One or more bytes of RC oscillator calibration data.
#     eeprom       The EEPROM of the device.
#     efuse         The extended fuse byte.
#     flash          The ﬂash ROM of the device.
#     fuse           The fuse byte in devices that have only a single fuse byte.
#     hfuse          The high fuse byte.
#     lfuse           The low fuse byte.
#     lock            The lock byte.
#
#    op
#
#     The op ﬁeld speciﬁes what operation to perform:
#
#     r       read the speciﬁed device memory and write to the speciﬁed ﬁle
#     w       read the speciﬁed ﬁle and write it to the speciﬁed device memory
#     v       read the speciﬁed device memory and the speciﬁed ﬁle and perform a verify operation
#
#    filename
#
#     Specify the hex file name. If file is not in current directory specify file name with appropriate path.
#
#    format
#
#     Format need not be specified, for hex files, avrdude will automatically detect the format.
#
# The trick to do it quickly : The Batch file :



# -----
# ----- ricavato da platformIO in verbose mode
#   avrdude -v -p atmega328p -C /home/pi/.platformio/packages/tool-avrdude/avrdude.conf -c arduino -b 57600 -P "/dev/ttyUSB3" -D -U flash:w:.pioenvs/nano/firmware.hex:i
# -----

# CONFIG_FILE='/opt/arduino-1.8.1/hardware/tools/avr/etc/avrdude.conf'


# - READ
function readFrom() {
    PORT="$1"
    MODE='r'
    avrdude -v -p atmega328p -C ${CONFIG_FILE} -c arduino -b 57600 -P ${PORT} -D -U flash:$MODE:${fileName}:i
}


# - WRITE
function writeTo() {
    PORT="$1"
    MODE='w'
    avrdude -v -p atmega328p -C ${CONFIG_FILE} -c arduino -b 57600 -P ${PORT} -D -U flash:$MODE:${fileName}:i
}

# - VERIFIY
function verifyCode() {
    PORT="$1"
    MODE='v'
    avrdude -v -p atmega328p -C ${CONFIG_FILE} -c arduino -b 57600 -P ${PORT} -D -U flash:$MODE:${fileName}:i
}


##############################
# M A I N
##############################
CONFIG_FILE='/home/pi/.platformio/packages/tool-avrdude/avrdude.conf'
fileName='/tmp/firmwareUSB1.hex'
fromDEV="/dev/ttyUSB0"
  toDEV="/dev/ttyUSB1"

    readFrom    $fromDEV
    writeTo     $toDEV
    verifyCode  $toDEV
