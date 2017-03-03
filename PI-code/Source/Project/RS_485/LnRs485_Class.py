#!/usr/bin/env python3
#
#

__author__   = 'Loreto Notarantonio'
__email__    = 'nlroeto@gmail.com'

__version__  = 'v2017-03-03_08.42.47'
__status__   = 'Beta'

import os
import serial       # sudo pip3.4 install pyserial
import struct
import sys
import time

# Allow long also in Python3
# http://python3porting.com/noconv.html
if sys.version > '3':
    import binascii
    long = int



####################
## Default values ##
####################
# Several instrument instances can share the same serialport
_SERIALPORTS = {}

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
# class LnRs485():
    """Instrument class for talking to instruments (slaves) via the Modbus RTU protocol (via RS485 or RS232).

    Args:
        * port (str):           The serial port name, for example '/dev/ttyUSB0' (Linux), '/dev/tty.usbserial' (OS X) or 'COM4' (Windows).
        * slaveaddress (int):   Slave address in the range 1 to 247 (use decimal numbers, not hex).
        * mode (str):           Mode selection. Can be MODE_RTU or MODE_ASCII!

    """

    def __init__(self, port, slaveaddress, mode='ascii'):
        self._MODE_ASCII = mode
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

        self.STX = int(0x02)
        self.ETX = int(0x03)

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


    def _calculateCRC8(self, byteArray_data):
        result = 0
        for byte in byteArray_data:
            # print ('byte: {0} - result {1}'.format( byte, result))
            b2 = byte
            if (byte < 0):
                b2 = byte + 256
            for i in range(8):
                odd = ((b2^result) & 1) == 1
                result >>= 1
                b2 >>= 1
                if (odd):
                    result ^= 0x8C # this means crc ^= 140

        return result


        # - send a byte complemented, repeated
        # - only values sent would be (in hex):
        # -   0F, 1E, 2D, 3C, 4B, 5A, 69, 78, 87, 96, A5, B4, C3, D2, E1, F0
        # -   invia prima l'HighNibble e poi il LowNibble
    def sendComplemented(self, what, fDEBUG=False):
        if fDEBUG: print ("Sending: x{0:02X}".format(what))

        # first nibble
        c = what >> 4;
        byteValue = (c << 4) | (c ^ 0x0F)
        if fDEBUG: print ("  x{0:02X}".format(byteValue), end="")
        self.serial.write(bytes(byteValue))

        # second nibble
        c = what & 0x0F;
        byteValue = (c << 4) | (c ^ 0x0F)
        if fDEBUG: print ("               x{0:02X}".format(byteValue))
        self.serial.write(bytes(byteValue))

        return byte1, byte2

    def getComplemented(self, what, fDEBUG=False):
        if fDEBUG: print ("Sending: x{0:02X}".format(what))

        # first nibble
        c = what >> 4;
        byteValue = (c << 4) | (c ^ 0x0F)
        byte1 = byteValue
        if fDEBUG: print ("               x{0:02X}".format(byte1))

        # second nibble
        c = what & 0x0F;
        byteValue = (c << 4) | (c ^ 0x0F)
        byte2 = byteValue
        if fDEBUG: print ("               x{0:02X}".format(byte2))

        return byte1, byte2


    #######################################################################
    # - by Loreto
    # - Lettura dati bsato sul protocollo:
    # -     RS485 protocol library by Nick Gammon
    # - STX - data - CRC - ETX
    # - A parte STX e ETX tutti gli altri byte sono inviati come due nibble
    # -  byte complemented
    # -  only values sent would be (in hex):
    # -    0F, 1E, 2D, 3C, 4B, 5A, 69, 78, 87, 96, A5, B4, C3, D2, E1, F0
    #######################################################################
    #@TODO: verifica che un bytearray possa essere inviato correttamente
    def writeData(self, data, TIMEOUT=5, fDEBUG=False):

        # preparaiamo il bytearray con i dati da inviare
        dataToSend=bytearray()

            # - STX
        dataToSend.append(self.STX)

            # - Data
        for thisByte in data:
            byte1, byte2 = self.getComplemented(thisByte, fDEBUG=True)
            dataToSend.append(byte1)
            dataToSend.append(byte2)

            # - CRC
        CRC_value  = self._calculateCRC8(data)
        byte1, byte2 = self.getComplemented(CRC_value, fDEBUG=True)
        dataToSend.append(byte1)
        dataToSend.append(byte2)
        # dataToSend.append(CRC_value)   # per generare un errore

            # - ETX
        dataToSend.append(self.ETX)



        if self.close_port_after_each_call:
            self.serial.open()

            # INVIO dati
        self.serial.write(dataToSend)

        """
            .... oppure
        import struct
        for byteVal in dataToSend:
            self.serial.write(struct.pack('>B', byteVal))
        """

        if self.close_port_after_each_call:
            self.serial.close()

        return



    #######################################################################
    # - by Loreto
    #######################################################################
    def readData(self, TIMEOUT=5, fDEBUG=False):
        """
            - Lettura dati bsato sul protocollo:
            -     RS485 protocol library by Nick Gammon
            - STX - data - CRC - ETX
            - A parte STX e ETX tutti gli altri byte sono inviati come due nibble
            -  byte complemented
            -  only values sent would be (in hex):
            -    0F, 1E, 2D, 3C, 4B, 5A, 69, 78, 87, 96, A5, B4, C3, D2, E1, F0
        """

        if self.close_port_after_each_call:
            self.serial.open()

        chInt = 0
        buffer = bytearray()            # Creating an empty instance - e' un array di integer

            # ---------------------------------------------
            # - waiting for STX
            # ---------------------------------------------
        while chInt != self.serial.STX:
            ch = self.serial.read(1)        # ch e' un bytes
            if ch == b'': continue
            chHex = binascii.hexlify(ch)
            chInt = int(chHex, 16)

            # - save STX in buffer
        buffer.append(chInt)

            # ---------------------------------------------
            # - waiting for ETX
            # ---------------------------------------------
        while chInt != self.serial.ETX:
            ch = self.serial.read(1)        # ch e' un bytes
            if ch == b'': continue
            chHex = binascii.hexlify(ch)
            chInt = int(chHex, 16)
            if fDEBUG: print ("Reading: {0} - {1:<10} - {2:<10} {3:<10} - {4:<10} {5:<10} ".format(type(ch), ch, type(chInt), chInt, type(chHex), chHex))
            buffer.append(chInt)

        if self.close_port_after_each_call:
            self.serial.close()

            # ---------------------------------------------
            # - print Received Data
            # ---------------------------------------------
        if fDEBUG:
            print ("received Data:", end="")
            for ch in buffer:
                print (" x{0:02X}".format(ch), end="")
            print ()


            # ---------------------------------------------
            # --- verifica STX & ETX
            # ---------------------------------------------
        if buffer[0] != self.serial.STX or buffer[-1] != self.serial.ETX:
            return bytearray()

        retVal = bytearray()
        ERROR  = False

            # ---------------------------------------------
            # - process payload
            # - byte = ch1_HNibble * 16 + ch2_HNibble
            # ---------------------------------------------
        xy = iter(buffer[1:-1])
        for ch1, ch2 in zip(xy, xy):
            if ERROR:
                return bytearray()

            if fDEBUG: print ("complementedData: x{0:02X} + x{1:02X}".format(ch1, ch2), end="")
                # - check first byte
            ch1_HNibble = (ch1 >> 4) & 0x0F
            ch1_LNibble = ~ch1 & 0x0F
            if ch1_LNibble != ch1_HNibble:
                ERROR = True

                # - check second byte
            ch2_HNibble = (ch2 >> 4) & 0x0F
            ch2_LNibble = ~ch2 & 0x0F
            if ch2_LNibble != ch2_HNibble:
                ERROR = True

                # re-build real byte
            realByte = ch1_HNibble*16 + ch2_HNibble
            if fDEBUG: print ("    -   resulting data BYTE: x{0:02X}".format(realByte))
            retVal.append(realByte)


            # --- check CRC
        CRC_received    = retVal[-1]
        CRC_calculated  = self._calculateCRC8(retVal[:-1])
        if not CRC_received == CRC_calculated:
            return bytearray()

        if fDEBUG:
            # print ("CRC received  : x%02X" % (CRC_received))
            print ("CRC received  : x{0:02X}".format(CRC_received))
            xx = self._calculateCRC8(retVal[:-1])
            print ("CRC calculated: x{0:02X}".format(CRC_calculated))
            print ()

        return retVal[:-1]                      # Escludiamo il CRC

