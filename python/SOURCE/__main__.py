#!/usr/bin/env python3
# -*- coding: iso-8859-1 -*-
#
# Scope:  ............
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import sys, os; sys.dont_write_bytecode = True
import subprocess


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
log.setLevel(logging.INFO)


class LnClass(): pass

import  prjPackage as Ln
# from    prjPackage.LnMinimalModbus            import *
import  prjPackage.LnModbus  as ModBus


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

import os
import serial
import struct
import sys
import time

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





ModBus.CLOSE_PORT_AFTER_EACH_CALL = True

################################################################################
# - M A I N
#
#   http://minimalmodbus.sourceforge.net/apiminimalmodbus.html
################################################################################
if __name__ == "__main__":
    gv.Lnf = Ln.preparePATHs(False)

    # it = iter([1,2,3,4,5,6])
    # for x, y in zip(it, it):
    #     print (x, y)

    # for i in range(0,10,2): print(i) sys.exit()

    slave01 = ModBus.Instrument('/dev/ttyUSB1', 1, ModBus.MODE_ASCII)  # port name, slave address (in decimal)
    slave01.serial.baudrate =  9600
    data = slave01.readData(STX=0x02, ETX=0x03, fDEBUG=False)


    print ("received data:", end='')
    for ch in data:
        print (" x%02X" %(ch), end="")

    print()

    # for ch in data[::2]:
    #     print ("printing: %03d - x%02X" %(ch, ch))
    # print()

    # it = iter(data)
    # for ch1, ch2 in zip(it, it):
    #     print ("    printing: x%02X + x%02X" %(ch1, ch2))

    # print('...')
    # print(Ln.byteArrayCheckSum(data))
    # print(Ln.calculateCRC8(data))

