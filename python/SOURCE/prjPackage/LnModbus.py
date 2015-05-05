#!/usr/bin/env python3
#
#   Copyright 2014 Jonas Berg
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
#   http://minimalmodbus.sourceforge.net/apiminimalmodbus.html

"""

.. moduleauthor:: Jonas Berg <pyhys@users.sourceforge.net>

MinimalModbus: A Python driver for the Modbus RTU protocol via serial port (via RS485 or RS232).

This Python file was changed (committed) at $Date: 2014-06-22 01:29:19 +0200 (Sun, 22 Jun 2014) $,
which was $Revision: 200 $.

"""

import  prjPackage as Ln

__author__   = 'Jonas Berg'
__email__    = 'pyhys@users.sourceforge.net'
__url__      = 'http://minimalmodbus.sourceforge.net/'
__license__  = 'Apache License, Version 2.0'

__version__  = '0.6'
__status__   = 'Beta'
__revision__ = '$Rev: 200 $'
__date__     = '$Date: 2014-06-22 01:29:19 +0200 (Sun, 22 Jun 2014) $'

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

BAUDRATE = 115200
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


class Instrument():
    """Instrument class for talking to instruments (slaves) via the Modbus RTU protocol (via RS485 or RS232).

    Args:
        * port (str):           The serial port name, for example '/dev/ttyUSB0' (Linux), '/dev/tty.usbserial' (OS X) or 'COM4' (Windows).
        * slaveaddress (int):   Slave address in the range 1 to 247 (use decimal numbers, not hex).
        * mode (str):           Mode selection. Can be MODE_RTU or MODE_ASCII!

    """

    def __init__(self, port, slaveaddress, mode=MODE_ASCII):
        if port not in _SERIALPORTS or not _SERIALPORTS[port]:
            self.serial = _SERIALPORTS[port] = serial.Serial(port=port, baudrate=BAUDRATE, parity=PARITY, bytesize=BYTESIZE, stopbits=STOPBITS, timeout=TIMEOUT)
        else:
            self.serial = _SERIALPORTS[port]
            if self.serial.port is None:
                self.serial.open()
        """The serial port object as defined by the pySerial module. Created by the constructor.

        Attributes:
            - port (str):      Serial port name.
                - Most often set by the constructor (see the class documentation).
            - baudrate (int):  Baudrate in Baud.
                - Defaults to :data:'BAUDRATE'.
            - parity (probably int): Parity. See the pySerial module for documentation.
                - Defaults to :data:'PARITY'.
            - bytesize (int):  Bytesize in bits.
                - Defaults to :data:'BYTESIZE'.
            - stopbits (int):  The number of stopbits.
                - Defaults to :data:'STOPBITS'.
            - timeout (float): Timeout value in seconds.
                - Defaults to :data:'TIMEOUT'.
        """


        self.address = slaveaddress
        """Slave address (int). Most often set by the constructor (see the class documentation). """

        self.mode = mode
        """Slave mode (str), can be MODE_RTU or MODE_ASCII.  Most often set by the constructor (see the class documentation).

        New in version 0.6.
        """

        self.debug = False
        """Set this to :const:'True' to print the communication details. Defaults to :const:'False'."""

        self.close_port_after_each_call = CLOSE_PORT_AFTER_EACH_CALL
        """If this is :const:'True', the serial port will be closed after each call. Defaults to :data:'CLOSE_PORT_AFTER_EACH_CALL'. To change it, set the value 'minimalmodbus.CLOSE_PORT_AFTER_EACH_CALL=True' ."""

        self.precalculate_read_size = True
        """If this is :const:'False', the serial port reads until timeout
        instead of just reading a specific number of bytes. Defaults to :const:'True'.

        New in version 0.5.
        """

        if  self.close_port_after_each_call:
            self.serial.close()

    def __repr__(self):
        """String representation of the :class:'.Instrument' object."""
        return "{}.{}<id=0x{:x}, address={}, mode={}, close_port_after_each_call={}, precalculate_read_size={}, debug={}, serial={}>".format(
            self.__module__,
            self.__class__.__name__,
            id(self),
            self.address,
            self.mode,
            self.close_port_after_each_call,
            self.precalculate_read_size,
            self.debug,
            self.serial,
            )



    #######################################################################
    # Lettura di una riga con il presupposto che '\n' indica fine riga
    #######################################################################
    def readLine(self):
        line = self.serial.readline()
        if line:
            if isinstance(line, bytes):
                line = line.decode('utf-8')
            destAddr = line[6]
            # print ("byte0 = [{0}]".format(byte0))
            if destAddr == address:
                if trimNewLine: line=line.strip('\n')
                print ("[{0}] - {1}".format(port.port, line))
                return line
            # else:
            #     print ("message skipped")


    #######################################################################
    # - Lettura di una riga con il presupposto che ETX indica fine dati
    # - a parte STX e ETX tutti gli altri byte sono inviati come due nibble
    # -  byte complemented
    # -  only values sent would be (in hex):
    # -    0F, 1E, 2D, 3C, 4B, 5A, 69, 78, 87, 96, A5, B4, C3, D2, E1, F0
    #######################################################################
    def readData(self, STX=0x02, ETX=0x03, fDEBUG=False):

        if self.close_port_after_each_call:
            self.serial.open()

        # ---------------------------------------------
        # --- lettura dati da seriale fino a ETX
        # --- Non controlliamo i complementi
        # ---------------------------------------------
        chInt = 0
        buffer = bytearray()            # Creating an empty instance - e' un array di integer

            # ---------------------------------------------
            # - waiting for STX
            # ---------------------------------------------
        while chInt != STX:
            ch = self.serial.read(1)        # ch e' un bytes
            if ch == b'': continue
            chHex = binascii.hexlify(ch)
            chInt = int(chHex, 16)

        buffer.append(chInt)

            # ---------------------------------------------
            # - waiting for ETX
            # ---------------------------------------------
        while chInt != ETX:
            ch = self.serial.read(1)        # ch e' un bytes
            if ch == b'': continue
            chHex = binascii.hexlify(ch)
            chInt = int(chHex, 16)
            if fDEBUG: print ("Reading: {0} - {1:<10} - {2:<10} {3:<10} - {4:<10} {5:<10} ".format(type(ch), ch, type(chInt), chInt, type(chHex), chHex))
            buffer.append(chInt)


        bufferLen = len(buffer)
        if fDEBUG:print ('TROVATO')
        if self.close_port_after_each_call:
            self.serial.close()

        # --- print Received Data
        if fDEBUG:
            print ("received Data:", end="")
            for ch in buffer:
                print (" x%02X" %(ch), end="")
            print ()


        # --- verifica STX & ETX
        if buffer[0] != STX or buffer[-1] != ETX:
            return bytearray()

        # --- elaborazione payload + CRC
        retVal = bytearray()
        xy = iter(buffer[1:-1])
        ERROR = False
        for ch1, ch2 in zip(xy, xy):
            if fDEBUG: print ("complementedData: x%02X + x%02X" %(ch1, ch2), end="")
            if ERROR: break

            ch1_HNibble = (ch1 >> 4) & 0x0F
            ch1_LNibble = ~ch1 & 0x0F
            if ch1_LNibble != ch1_HNibble:
                ERROR = True

            ch2_HNibble = (ch2 >> 4) & 0x0F
            ch2_LNibble = ~ch2 & 0x0F
            if ch2_LNibble != ch2_HNibble:
                ERROR = True

                # ricostruzione byte
            newByte = ch2_HNibble + ch1_HNibble*16
            if fDEBUG: print ("    -   resulting data BYTE: x%02X" %(newByte))
            retVal.append(newByte)

        if ERROR:
            return bytearray()

        CRC_received    = retVal[-1]
        CRC_calculated  = Ln.byteArrayCheckSum(retVal[:-1])
        if CRC_received != CRC_calculated:
            return bytearray()

        if fDEBUG:
            print ("CRC received  : x%02X" % (CRC_received))
            xx = Ln.byteArrayCheckSum(retVal[:-1])
            print ("CRC calculated: x%02X" % (CRC_calculated))
            print ()

        return retVal[:-1]                      # Escludiamo il CRC





        '''
        # ---------------------------------------------
        # - ricerca del STX e ritorna solo la parte
        # - compresa tra STX-[returnedData]-ETX
        # ---------------------------------------------
        retVal = None
        bufferLen = len(buffer)
        for inx, ch in enumerate(reversed(buffer)):   # ch e' un INTEGER
            if fDEBUG:print ("Checking[{2}]: {0} - {1:<10}".format(type(ch), ch, inx))
            if ch == STX:
                if fDEBUG:print ("found STX: {0}".format(inx))
                retVal = buffer[bufferLen-inx:-1]
                break
        '''

        # ---------------------------------------------
        # - recuperiamo i dati reali
        # ---------------------------------------------

        print()
        # print("CRC={0}".format(retVal[-1]))
        # return retVal[:-1]  # elimina il CRC
        return retVal



        '''
        while True:
            ch = self.serial.read(1)
            if ch == b'': continue
            chHex  = binascii.hexlify(ch)
            print ("{0} - {1} {2}".format(type(ch), ch, chHex))
            # if chHex == b'20': continue
            retVal.append(ord(ch))
            if chHex == ETX:
                print ('TROVATO')
                if self.close_port_after_each_call:
                    self.serial.close()
                return retVal
        '''


