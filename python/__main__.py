#!/usr/bin/env python3
# -*- coding: iso-8859-1 -*-
#
# Scope:  ............
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import sys, os; sys.dont_write_bytecode = True
import serial
import time

import logging
import logging.handlers as Handlers
#---------------------------------------------------------------------------#
# This will send the error messages in the specified namespace to a file.
# The available namespaces in pymodbus are as follows:
#---------------------------------------------------------------------------#
# * pymodbus.*          - The root namespace
# * pymodbus.server.*   - all logging messages involving the modbus server
# * pymodbus.client.*   - all logging messages involving the client
# * pymodbus.protocol.* - all logging messages inside the protocol layer
#---------------------------------------------------------------------------#
logging.basicConfig()
log = logging.getLogger('pymodbus.server')
log = logging.getLogger()
log.setLevel(logging.DEBUG)


class LnClass(): pass

import  prjPackage as Ln
# from    prjPackage.LnMinimalModbus            import *
import  prjPackage.LnRs485  as rs485


# gv                  = GlobalVars          # shortCut alle GlobalVars
gv                  = Ln.GlobalVars          # shortCut alle GlobalVars
gv.Ln               = Ln                  # Funzioni

# xx = GlobalVars.LnClass()



__author__   = 'loreto Notarantonio'
__email__    = 'nloreto@gmail.com'
__url__      = 'http://minimalmodbus.sourceforge.net/'
__license__  = 'Apache License, Version 2.0'

__version__  = '0.1'
__status__   = 'Beta'
__revision__ = '$Rev: 200 $'
__date__     = '$Date: 2015-03-28 $'



if sys.version > '3':    import binascii

# Allow long also in Python3
# http://python3porting.com/noconv.html
if sys.version > '3':    long = int




##############################
## Modbus instrument object ##
##############################


#### L.N. ##########################
# Handling BigEndian words
# http://www.digi.com/wiki/developer/index.php/How_to_create_Modbus/RTU_request_in_Python
####################################
def u16_to_bestr( u):
    """Given word, return as big-endian binary string"""
    u = (int(u) & 0xFFFF)
    return( chr(u>>8) + chr(u&0xFF) )

def bestr_to_u16( st):
    """Given big-endian binary string, return bytes[0-1] as int"""
    return( (ord(st[0])<<8) + ord(st[1]))



def startSlave(usbDevPath):
    slave01 = rs485.Instrument(usbDevPath, 1, rs485.MODE_ASCII)  # port name, slave address (in decimal)
    # slave01.serial.baudrate = 19200
    slave01.serial.baudrate = 9600
    slave01.serial.STX      = 0x02
    slave01.serial.ETX      = 0x03
    data = slave01.readData(fDEBUG=False)

    return data




# ##########################################################################
# # setupRS485(usbDevPath)
# ##########################################################################
def setupRS485(usbDevPath):

    rs485.CLOSE_PORT_AFTER_EACH_CALL = True

    Master = rs485.Instrument(usbDevPath, 0, rs485.MODE_ASCII)  # port name, slave address (in decimal)
    # Master.serial.baudrate = 19200
    Master.serial.baudrate = 9600
    Master.serial.STX      = 0x02
    Master.serial.ETX      = 0x03

    # slaveADDR = 0x01
    # slaveADDR = int(slave)

    # data = bytearray()
    # data.append(slaveADDR)   # Address
    # data.append(0x11)
    # data.append(0x12)
    # data = Master.writeData(data, fDEBUG=True)



import time

# ##########################################################################
# # setupVirtualWire()
# ##########################################################################
def setupVirtualWire(gv, stop=False):
    import pigpio
    import vw


    if stop:
        gv.VW.rx.cancel()
        gv.VW.tx.cancel()
        gv.VW.pi.stop()
        # return

    else:
        RX_pin  = 19        # GPIO19 - pin 35
        TX_pin  = 26        # GPIO26 - pin 37
        BPS     = 2000

        gv.VW = LnClass()
        gv.VW.pi = pigpio.pi() # Connect to local Pi.

        gv.VW.rx = vw.rx(gv.VW.pi, RX_pin, BPS) # Specify Pi, rx gpio, and baud.
        gv.VW.tx = vw.tx(gv.VW.pi, TX_pin, BPS) # Specify Pi, tx gpio, and baud.

        # return vw





################################################################################
# - M A I N
#
#   MASTER di LN-Protocol
#   Provvede a dialogare su due fronti:
#       1 - RS-485 (quindi fornire il device dove si trova l'RS485 USB converter
#       1 - VirtualWire - quindi modulo Wireless
################################################################################
if __name__ == "__main__":
    gv.Lnf = Ln.preparePATHs(False)
    # Ln.testVirtualWire()
    # sys.exit()

        # ---------------------------------------------
        # - Indirizzi degli SLAVE da controllare
        # ---------------------------------------------
    slaveADRESS = [1, 2]

    if len(sys.argv) != 2:
        print ("immettere:")
        print ("    USBdev (per la parte RS485):   ttyUSBx")
        sys.exit()

        # Verifica della presenza del device
    usbDevPath = Ln.isUsbDevice(sys.argv[1])
    if not Ln.isUsbDevice(usbDevPath):
        print('{0} - is not a valid USB device'.format(sys.argv[1]))
        sys.exit()


    try:
        setupRS485(usbDevPath)
        setupVirtualWire(gv)

    except (KeyboardInterrupt) as key:
        print ("Keybord interrupt has been pressed")
        sys.exit()



    setupVirtualWire(gv, stop=True)
    sys.exit()


    while True:
        try:
            # key = str(getKey())
            # print ("Key: x{0:02X}".format(key))

            data = startSlave(usbDevPath)
            print ("received data:", end=' ')
            for ch in data:
                print (" x{0:02X}".format(ch), end="")

            print()

        except (KeyboardInterrupt) as key:
            print (key)
            # choice      = input().strip()
            # if choice.upper() == 'X': break
            break


