#!/usr/bin/env python
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

import prjPackage as Ln
from prjPackage.minimalmodbus_ORIG            import *
import  prjPackage.minimalmodbus_ORIG         as mbus


# gv                  = GlobalVars          # shortCut alle GlobalVars
gv                  = Ln.GlobalVars          # shortCut alle GlobalVars
gv.Ln               = Ln                  # Funzioni

# xx = GlobalVars.LnClass()



"""

.. moduleauthor:: Jonas Berg <pyhys@users.sourceforge.net>

MinimalModbus: A Python driver for the Modbus RTU protocol via serial port (via RS485 or RS232).

This Python file was changed (committed) at $Date: 2014-06-22 01:29:19 +0200 (Sun, 22 Jun 2014) $,
which was $Revision: 200 $.

"""

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

if sys.version > '3':
    import binascii

# Allow long also in Python3
# http://python3porting.com/noconv.html
if sys.version > '3':
    long = int

_NUMBER_OF_BYTES_PER_REGISTER = 2
_SECONDS_TO_MILLISECONDS = 1000
_ASCII_HEADER = ':'
_ASCII_FOOTER = '\r\n'

# Several instrument instances can share the same serialport
_SERIALPORTS = {}
_LATEST_READ_TIMES = {}

####################
## Default values ##
####################

BAUDRATE = 19200
"""Default value for the baudrate in Baud (int)."""

PARITY   = serial.PARITY_NONE
"""Default value for the parity. See the pySerial module for documentation. Defaults to serial.PARITY_NONE"""

BYTESIZE = 8
"""Default value for the bytesize (int)."""

STOPBITS = 1
"""Default value for the number of stopbits (int)."""

TIMEOUT  = 0.05
"""Default value for the timeout value in seconds (float)."""

CLOSE_PORT_AFTER_EACH_CALL = False
"""Default value for port closure setting."""

#####################
## Named constants ##
#####################

MODE_RTU   = 'rtu'
MODE_ASCII = 'ascii'

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



# Feeding Input into the routine

# While your first instinct might be to create routines such as make_func3(slv,offset,count) and make_func16(slv,offset,count,data), these don't make very good use of Python - plus they don't encourage creative negative testing long-term. For example, how would you create a func-3 call with a bad CRC or too much data requested - create a second routine called make_func3_badcrc() ?
# Instead I suggest you fill in a dictionary holding the inputs, with some suitably defaulted if missing. While the key names are up to you, here is the list I've used with good results:
# ['dest'] is the Unit Id or slave address
# ['func'] is the Modbus code, such as 3 or 16
# ['protErr'] is the Modbus exception code
# ['rdOffset'] is the zero-based offset, so register 4x00001 is offset zero (0)
# ['rdCount'] is the word or bit count for the function
# ['rdData'] is a tuple or list holding words read
# ['wrOffset'] is like 'rdOffset', but used for writes - or for read/write functions
# ['wrCount'] is like 'rdCount', but used for writes - or for read/write functions
# ['wrData'] is a tuple or list holding words to write
# ['badCrc'] (for example) could be added to force a bad CRC to any request created
# Now we can create a read of 10 registers from 4x00001 with the call:
#     mbrtu_make_request( {'dest':1, 'func':3, 'rdOffset':0, 'rcCount':10})
# Below is a quick example - note that it does NOT survive missing keys to reduce the complexity.
def mbrtu_make_request( inDct):
    pass
'''
   inDct.update({'error':"", 'request':None })  # indicate no error

   dest = int(inDct.get('dest',1))  # default unit id to 1
   if((dest < 0) or (dest >255)):
      inDct.update({'error':"Bad Unit Id or Slave Address"})
      return inDct

   func = int(inDct.get('func',-1)) # default is -1/error

   req = None

   if(func in [1,2,3,4]):
      req = chr(dest) + chr(func) +
         u16_to_bestr(inDct['rdOffset']) + u16_to_bestr(inDct['rdCount'])

   elif( fnc == 5):
      if(inDct['wrData'][0]):
         # if first item is True, so 0xFF00 (not 0xFFFF)
         dat = 0xFF00
      else: # is False
         dat = 0x0000
      req = chr(dest) + chr(func) +
         u16_to_bestr(inDct['wrOffset']) + u16_to_bestr(dat)

   elif( fnc == 6):
      req = chr(dest) + chr(func) +
         u16_to_bestr(inDct['wrOffset']) + u16_to_bestr(inDct['wrData'][0])

   # elif( fnc == 15): not here yet

   # elif( fnc == 16): not here yet

   else:
      inDct.update({'error':"Unsupported Function"})
      return inDct

   # at this point we have the basic Modbus message
   if( req):
      crc = crc16.calcString( req, 0xFFFF)
      # oddly, we need to add the CRC as LittleEndian
      req += chr(crc&0xFF) + chr(crc>>8)
      inDct.update({'request':req})

   return inDct
'''



################################################################################
# - M A I N
#
#   http://minimalmodbus.sourceforge.net/apiminimalmodbus.html
################################################################################
if __name__ == "__main__":
    gv.Lnf = Ln.preparePATHs(False)
    # SER1 = LnClass()
    # SER1.REQ = gv.REQ
    # SER1.REQ.addr = 1                                   #slave address (in decimal)
    SER1 = mbus.Instrument('/dev/ttyUSB1', 1, mbus.MODE_RTU)  # port name, slave address (in decimal)
    SER2 = mbus.Instrument('/dev/ttyUSB2', 2, mbus.MODE_RTU)  # port name, slave address (in decimal)
    SER1.serial.baudrate =  115200
    print (SER2.serial.baudrate)
    print (SER1.serial)
    print (SER1)





