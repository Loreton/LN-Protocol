#!/usr/bin/env python3
#
#

__author__   = 'Loreto Notarantonio'
__email__    = 'nlroeto@gmail.com'

__version__  = 'v2017-03-09_09.02.35'
__status__   = 'Beta'

import os
import serial       # sudo pip3.4 install pyserial
import struct
import sys
import time
import inspect

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
CLOSE_PORT_AFTER_EACH_CALL = True
"""Default value for port closure setting."""

#####################
## Named constants ##
#####################

MODE_RTU   = 'rtu'
MODE_ASCII = 'ascii'
##############################
## Modbus instrument object ##
##############################


class LnRs485_Instrument():
# class LnRs485():
    """Instrument class for talking to instruments (slaves) via the Modbus RTU protocol (via RS485 or RS232).

    Args:
        * port (str):           The serial port name, for example '/dev/ttyUSB0' (Linux), '/dev/tty.usbserial' (OS X) or 'COM4' (Windows).
        * slaveaddress (int):   Slave address in the range 1 to 247 (use decimal numbers, not hex).
        * mode (str):           Mode selection. Can be MODE_RTU or MODE_ASCII!

    """

    def _internaLogger(self, package=None):
        ##############################################################################
        # - classe che mi permette di lavorare nel caso il logger non sia richiesto
        ##############################################################################
        class nullLogger():
                def __init__(self, package=None, stackNum=1):
                    pass
                def info(self, data):
                    self._print(data)
                def debug(self, data):
                    self._print(data)
                def error(self, data):  pass
                def warning(self, data):  pass

                def _print(self, data):
                    pass
                def _print_(self, data):
                    caller = inspect.stack()[4]
                    dummy, programFile, lineNumber, funcName, lineCode, rest = caller
                    if funcName == '<module>': funcName = '__main__'
                    str = "[{FUNC:<20}:{LINENO}] - {DATA}".format(FUNC=funcName, LINENO=lineNumber, DATA=data)
                    print (str)

        return nullLogger()


    def __init__(self, port, slaveaddress, mode='ascii', logger=None):
        self._MODE_ASCII = mode
        if port not in _SERIALPORTS or not _SERIALPORTS[port]:
            self.serial = _SERIALPORTS[port] = serial.Serial(port=port, baudrate=BAUDRATE, parity=PARITY, bytesize=BYTESIZE, stopbits=STOPBITS, timeout=TIMEOUT)
        else:
            self.serial = _SERIALPORTS[port]
            if self.serial.port is None:
                self.serial.open()

        if logger:
            self._setLogger = logger
        else:
            self._setLogger = self._internaLogger

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

        self.debug = True
        """Set this to :const:'True' to print the communication details. Defaults to :const:'False'."""

        self.bSTX = b'\x02'
        self.bETX = b'\x03'
        self.iSTX = self._byteToInt(self.bSTX)
        self.iETX = self._byteToInt(self.bETX)

        self.close_port_after_each_call = CLOSE_PORT_AFTER_EACH_CALL
        """If this is :const:'True', the serial port will be closed after each call. Defaults to :data:'CLOSE_PORT_AFTER_EACH_CALL'. To change it, set the value 'minimalmodbus.CLOSE_PORT_AFTER_EACH_CALL=True' ."""

        self.precalculate_read_size = True
        """If this is :const:'False', the serial port reads until timeout
        instead of just reading a specific number of bytes. Defaults to :const:'True'.

        New in version 0.5.
        """

        if  self.close_port_after_each_call:
            print('closing port...')
            self.serial.close()

        print ('mode:                           {0}'.format(self._MODE_ASCII))
        print ('STX:                            {0}'.format(self.iSTX))
        print ('ETX:                            {0}'.format(self.iETX))
        print ('CLOSE_PORT_AFTER_EACH_CALL:     {0}'.format(self.close_port_after_each_call))
        print ('precalculate_read_size:         {0}'.format(self.precalculate_read_size))

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
        logger = self._setLogger(package=__name__)
        crcValue = 0
        for byte in byteArray_data:
            if isinstance(byte, str): byte = ord(byte)            # onverte nel valore ascii
            logger.debug('byte: int:{0} hex: {0:02x} - crcValue int:{1} hex: {1:02x}'.format(byte, crcValue))
            b2 = byte
            if (byte < 0):
                b2 = byte + 256
            for i in range(8):
                odd = ((b2^crcValue) & 1) == 1
                crcValue >>= 1
                b2 >>= 1
                if (odd):
                    crcValue ^= 0x8C # this means crc ^= 140

        return crcValue


    # ---------------------------------------------
    # - aaaa bbbb
    # -     byte1 = aaaa !aaaa
    # -     byte2 = bbbb !bbbb
    # -     byte = byte1_HNibble * 16 + byte2_HNibble
    # ---------------------------------------------
    def _splitComplementedByte(self, byte):
        logger = self._setLogger(package=__name__)
        if isinstance(byte, str): byte = ord(byte)            # onverte nel valore ascii

        # print ('....', type(byte), byte)
        logger.debug ("converting: x{0:02X}".format(byte))

            # first nibble
        c = byte >> 4;
        byteValue = (c << 4) | (c ^ 0x0F)
        highNibble = byteValue
        logger.debug  ("    x{0:02X}".format( highNibble))

            # second nibble
        c = byte & 0x0F;
        byteValue = (c << 4) | (c ^ 0x0F)
        lowNibble = byteValue
        logger.debug  ("    x{0:02X}".format(lowNibble))


            # second two bytes
        return highNibble, lowNibble




    # ---------------------------------------------
    # -     byte1 = aaaa !aaaa
    # -     byte2 = bbbb !bbbb
    # -     byte = byte1_HNibble * 16 + byte2_HNibble
    # ---------------------------------------------
    def _combineComplementedByte(self, byte1, byte2):
        logger = self._setLogger(package=__name__)
        if isinstance(byte1, str): byte1 = ord(byte1)            # onverte nel valore ascii
        if isinstance(byte2, str): byte2 = ord(byte2)            # onverte nel valore ascii

        logger.debug("complementedData: x{0:02X} + x{1:02X}".format(byte1, byte2))

            # - check first byte
        byte1_HighNibble = (byte1 >> 4) & 0x0F
        byte1_LowNibble = ~byte1 & 0x0F
        if byte1_LowNibble != byte1_HighNibble:
            logger.error("byte1 nibbles corrupted: x{0:02X} + x{1:02X}".format(byte1_LowNibble, byte1_HighNibble))
            return None

            # - check second byte
        byte2_HighNibble = (byte2 >> 4) & 0x0F
        byte2_LowNibble = ~byte2 & 0x0F
        if byte2_LowNibble != byte2_HighNibble:
            logger.error("byte2 nibbles corrupted: x{0:02X} + x{1:02X}".format(byte2_LowNibble, byte2_HighNibble))
            return None

            # re-build real byte
        realByte = byte1_HighNibble*16 + byte2_HighNibble
        logger.debug("  resulting data BYTE: x{0:02X} char:{1}".format(realByte, chr(realByte)))

        return realByte


    #######################################################################
    # - by Loreto
    # - Scrittura dati bsato sul protocollo:
    # -     RS485 protocol library by Nick Gammon
    # - STX - data - CRC - ETX
    # - A parte STX e ETX tutti gli altri byte sono inviati come due nibble
    # -  byte complemented (incluso il CRC)
    # -  only values sent would be (in hex):
    # -    0F, 1E, 2D, 3C, 4B, 5A, 69, 78, 87, 96, A5, B4, C3, D2, E1, F0
    #######################################################################
    #@TODO: verifica che un bytearray possa essere inviato correttamente
    def writeData(self, data, TIMEOUT=5):
        logger = self._setLogger(package=__name__)

        # preparaiamo il bytearray con i dati da inviare
        dataToSend=bytearray()

            # - STX
        dataToSend.append(self.iSTX)

            # - Data
        for thisByte in data:
            byte1, byte2 = self._splitComplementedByte(thisByte)
            dataToSend.append(byte1)
            dataToSend.append(byte2)

            # - CRC
        CRC_value  = self._calculateCRC8(data)
        byte1, byte2 = self._splitComplementedByte(CRC_value)
        dataToSend.append(byte1)
        dataToSend.append(byte2)
        # dataToSend.append(CRC_value)   # per generare un errore

            # - ETX
        dataToSend.append(self.iETX)



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

        return dataToSend


    #######################################################################
    # - Lettura dati fino a EOD
    # - Ritorna una bytearray di integer
    #######################################################################
    def _readBuffer_01(self):
        logger = self._setLogger(package=__name__)

        if self.close_port_after_each_call:
            logger.debug('openig port...')
            self.serial.open()

        buffer = bytearray()
        while True:
            ch = self.serial.read(1)       # ch e' un bytes
            if ch == b'': continue

            chHex = binascii.hexlify(ch)
            chInt = int(chHex, 16)
            logger.debug(  """     Received: {chTYPE} - char: {ordCH:<4} int:{intCH:5} hex:{hexCH:02x}
                                """.format(chTYPE=type(ch), ordCH=chr(ord(ch)),  intCH=chInt, hexCH=chInt)
                        )
            buffer.append(chInt)

            if ch == self.serial.bETX:
                if self.close_port_after_each_call:
                    logger.debug('closing port...')
                    self.serial.close()

                return buffer

    #######################################################################
    # - Lettura dati fino a EOD
    # - Ritorna una bytearray di integer
    #######################################################################
    def _readBuffer_02(self):
        logger = self._setLogger(package=__name__)

        if self.close_port_after_each_call:
            logger.debug('openig port...')
            self.serial.open()

        chInt = 0
        buffer = bytearray()            # Creating an empty instance - e' un array di integer

            # ---------------------------------------------
            # - waiting for STX
            # ---------------------------------------------
        while chInt != self.serial.bSTX:
            ch = self.serial.read(1)        # ch e' un bytes
            if ch == b'': continue
            chHex = binascii.hexlify(ch)
            chInt = int(chHex, 16)
            logger.debug('STX byte received {0:02x}'.format(chInt))

            # - save STX in buffer
        buffer.append(chInt)

            # ---------------------------------------------
            # - waiting for ETX
            # ---------------------------------------------
        while chInt != self.serial.bETX:
            ch = self.serial.read(1)        # ch e' un bytes
            if ch == b'': continue
            chHex = binascii.hexlify(ch)
            chInt = int(chHex, 16)
                # - save byte in buffer
            buffer.append(chInt)

        if self.close_port_after_each_call:
            logger.debug('closing port...')
            self.serial.close()

        return buffer

    #######################################################################
    # - by Loreto
    #######################################################################
    def readData(self, TIMEOUT=5):
        logger = self._setLogger(package=__name__)
        """
            - Lettura dati bssato sul protocollo:
            -     RS485 protocol library by Nick Gammon
            - STX - data - CRC - ETX
            - A parte STX e ETX tutti gli altri byte sono inviati come due nibble
            -  byte complemented
            -  only values sent would be (in hex):
            -    0F, 1E, 2D, 3C, 4B, 5A, 69, 78, 87, 96, A5, B4, C3, D2, E1, F0
        """

        rowData = self._readBuffer_01()
        logger.debug('full data:       {0}'.format(' '.join('{:02x}'.format(x) for x in rowData)))


            # Prendiamo i dati fissi
        startOfText     = rowData[0]
        endOfText       = rowData[-1]
        payLoadNibbled  = rowData[1:-1] # skip STX and ETX - include nibbled_data+nibbled_CRC

            # ---------------------------------------------
            # - ricostruzione dei bytes originari
            # - byte = byte1_HighNibble*16 + byte2_HighNibble
            # ---------------------------------------------
            # il trick che segue ci permette di prelevare due bytes alla volta
        payLoad_crc = bytearray()
        xy = iter(payLoadNibbled)
        for ch1, ch2 in zip(xy, xy):
            realByte = self._combineComplementedByte(ch1, ch2)
            if not realByte:
                return bytearray(), rowData
            else:
                payLoad_crc.append(realByte)


            # -----------------------------------------------------------------------
            # - Una volta ricostruidi i bytes origilali,
            # - calcoliamo il CRC sui dati (ovviamento escluso il byte di CRC stesso)
            # -----------------------------------------------------------------------
        CRC_calculated  = self._calculateCRC8(payLoad_crc[:-1])

            # ---------------------------------
            # - check CRC (drop STX and ETX)
            # ---------------------------------
        CRC_received    = payLoad_crc[-1]
        payLoad         = payLoad_crc[:-1]

        logger.debug("    CRC received  : x{0:02X}".format(CRC_received))
        logger.debug("    CRC calculated: x{0:02X}".format(CRC_calculated))

        if not CRC_received == CRC_calculated:
            logger.error('Il valore di CRC non coincide')
            print ('ERROR: Il valore di CRC non coincide')
            print ()
            print ("    CRC received  : x{0:02X}".format(CRC_received))
            print ("    CRC calculated: x{0:02X}".format(CRC_calculated))
            print ()
            return bytearray(), rowData

        return payLoad, rowData



    def _byteToInt(self, byte):
        chHex = binascii.hexlify(byte)
        chInt = int(chHex, 16)
        return chInt








# import os, sys
# import datetime
# this_mod = sys.modules[__name__]
# import time

class LnClass(): pass
################################################################################
# - M A I N
# - Prevede:
# -  2 - Controllo parametri di input
# -  5 - Chiamata al programma principale del progetto
################################################################################
if __name__ == '__main__':
    Syntax = """
        Immettere:
            action.usbPortNO.EoD [EOD=endOfData, default=10='\n']

        es.:
            monitor.0   : per monitorare la porta /dev/ttyUSB0
            send.0      : per inviare messaggi sulla porta /dev/ttyUSB0
    """



    if len(sys.argv) > 1:
        token = sys.argv[1].split('.')

        if len(token) == 2:
            action, portNO = sys.argv[1].split('.')
            EOD = b'\x03'

        elif len(token) == 3:
            action, portNO, EOD = sys.argv[1].split('.')
            iEOD = int(EOD)
            EOD = bytes([iEOD])

        else:
            print (Sintax)
            sys.exit()




    LnRs485                = LnRs485_Instrument   # short pointer alla classe
    rs485                  = LnClass()
    rs485.MASTER_ADDRESS   = 0
    rs485.bSTX             = b'\x02'
    rs485.bETX             = b'\x03'
    rs485.usbDevPath       = '/dev/ttyUSB{0}'.format(portNO)
    rs485.baudRate         = 9600
    rs485.mode             = 'ascii'

    print('     .....action:', action)
    print('     .....portNO:', portNO)
    print('     .....EOD:   ', EOD)


        # ===================================================
        # = RS-485 port monitor
        # ===================================================
    if action == 'monitor':
        print('Monitoring port: {0}'.format(rs485.usbDevPath))
            # ------------------------------
            # - Inizializzazione
            # ------------------------------
        try:
            # port = gv.Prj.LnRs485.Instrument(rs485.usbDevPath, 0, rs485.mode)  # port name, slave address (in decimal)
            # monitorPort = gv.Prj.rs485.SetupPort(gv.Prj.LnRs485, rs485, 5)
            address = 5
            print('setting port {0} to address {1}'.format(rs485.usbDevPath, address))
            port = LnRs485(rs485.usbDevPath, address, rs485.mode, logger=None)  # port name, slave address (in decimal)
            port.serial.baudrate = rs485.baudRate
            port.serial.bSTX      = rs485.bSTX
            port.serial.bETX      = rs485.bETX

            print ('... press ctrl-c to stop the process.')
            while True:
                payLoad, rowData = port.readData()
                print ('rowData (Hex):  {0}'.format(' '.join('{0:02x}'.format(x) for x in rowData)))
                if payLoad:
                    print ('payLoad (Hex):      {0}'.format(' '.join('{0:02x}'.format(x) for x in payLoad)))
                    print ('payLoad (chr):      {0}'.format(' '.join('{0:>2}'.format(chr(x)) for x in payLoad)))
                else:
                    print ('payLoad ERROR....')
                print()


        except (KeyboardInterrupt) as key:
            print ("Keybord interrupt has been pressed")
            sys.exit()


    elif action == 'send':
        print('Sending data to port: {0}'.format(rs485.usbDevPath))
            # ------------------------------
            # - Inizializzazione
            # ------------------------------
        try:
            address = 5
            print('setting port {0} to address {1}'.format(rs485.usbDevPath, address))
            port = LnRs485(rs485.usbDevPath, address, rs485.mode, logger=None)  # port name, slave address (in decimal)
            port.serial.baudrate = rs485.baudRate
            port.serial.bSTX      = rs485.bSTX
            port.serial.bETX      = rs485.bETX
            # sendingPort = gv.Prj.rs485.SetupPort(gv.Prj.LnRs485, rs485, 5)
            print ('... press ctrl-c to stop the process.')
            index = 0
            basedata = 'Loreto.'
            while True:
                index += 1
                dataToSend  = '[{0}.{1:04}]'.format(basedata, index)
                line        = '[{0}:{1:04}] - {2}'.format(rs485.usbDevPath, index, dataToSend)
                print (line)
                dataSent = port.writeData(dataToSend)
                print ('sent (Hex): {0}'.format(' '.join('{0:02x}'.format(x) for x in dataSent)))
                # print ('          Chr      {0}'.format(' '.join('{0:>2}'.format(chr(x)) for x in dataSent)))
                print()
                time.sleep(5)


        except (KeyboardInterrupt) as key:
            print ("Keybord interrupt has been pressed")
            sys.exit()


    else:
        print(gv.INPUT_PARAM.actionCommand, 'not available')

