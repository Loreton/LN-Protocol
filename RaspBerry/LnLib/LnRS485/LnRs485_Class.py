#!/usr/bin/env python3
#
# modified by Loreto:           2017-03-10_14.50.01
# #####################################################

__author__   = 'Loreto Notarantonio'
__email__    = 'nloreto@gmail.com'

__version__  = 'LnVer_2017-04-06_17.57.23'
__status__   = 'Beta'

import os
import serial       # sudo pip3.4 install pyserial
import sys
import inspect
import string



####################
## Default values ##
####################
# Several instrument instances can share the same serialport
_SERIALPORTS = {}


BYTESIZE = 8
"""Default value for the bytesize (int)."""

PARITY   = serial.PARITY_NONE
"""Default value for the parity. See the pySerial module for documentation. Defaults to serial.PARITY_NONE"""

STOPBITS = 1
"""Default value for the number of stopbits (int)."""

TIMEOUT  = 0.05
"""Default value for the timeout value in seconds (float)."""

# CLOSE_PORT_AFTER_EACH_CALL = False
# CLOSE_PORT_AFTER_EACH_CALL = True
"""Default value for port closure setting."""

#####################
## Named constants ##
#####################

MODE_RTU   = 'rtu'
MODE_ASCII = 'ascii'
##############################
## Modbus instrument object ##
##############################


# -----------------------------------------------------------------------
# - con il gioco del complementedByte, gli unici byte che dovrebbero
# - circolare sono i seguenti al di là dello STX ed ETX
# -----------------------------------------------------------------------
validBytesHex = [
                '0x0F',
                '0x1E',
                '0x2D',
                '0x3C',
                '0x4B',
                '0x5A',
                '0x69',
                '0x78',
                '0x87',
                '0x96',
                '0xA5',
                '0xB4',
                '0xC3',
                '0xD2',
                '0xE1',
                '0xF0'
              ]


class LnRs485_Instrument():
# class LnRs485():
    """Instrument class for talking to instruments (slaves) via the Modbus RTU protocol (via RS485 or RS232).

    Args:
        * port (str):           The serial port name, for example '/dev/ttyUSB0' (Linux), '/dev/tty.usbserial' (OS X) or 'COM4' (Windows).
        * slaveaddress (int):   Slave address in the range 1 to 247 (use decimal numbers, not hex).
        * mode (str):           Mode selection. Can be MODE_RTU or MODE_ASCII!

    """

    # def __init__(self, port, slaveaddress, mode='ascii', baudrate=9600, logger=None):
    def __init__(self, port, mode='ascii', baudrate=9600, logger=None):
        self._MODE_ASCII = mode
        if port not in _SERIALPORTS or not _SERIALPORTS[port]:
            try:
                self.serial = _SERIALPORTS[port] = serial.Serial(
                                                    port=port,
                                                    baudrate=baudrate,
                                                    parity=PARITY,
                                                    bytesize=BYTESIZE,
                                                    stopbits=STOPBITS,
                                                    timeout=TIMEOUT)
                                                    # rtscts=1,
            except (Exception) as why:
                print ('ERROR:  ', str(why))
                sys.exit()
        else:
            self.serial = _SERIALPORTS[port]
            if self.serial.port is None:
                self.serial.open()

        if logger:
            self._setLogger = logger
        else:
            self._setLogger = self._internaLogger

        self._validBytes=bytearray([int(i, 16) for i in validBytesHex]) # creiamo un array di integer
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


        self.mode = mode
        """Slave mode (str), can be MODE_RTU or MODE_ASCII.  Most often set by the constructor (see the class documentation).

        New in version 0.6.
        """

        self.debug = True
        """Set this to :const:'True' to print the communication details. Defaults to :const:'False'."""

        self.STX = int('0x02', 16) # integer
        self.ETX = int('0x03', 16) # integer
        # self.CRC = True

        self.close_port_after_each_call = False
        """If this is :const:'True', the serial port will be closed after each call. """
        if  self.close_port_after_each_call: self.serial.close()

        self.precalculate_read_size = True
        """If this is :const:'False', the serial port reads until timeout
        instead of just reading a specific number of bytes. Defaults to :const:'True'.

        New in version 0.5.
        """



    def ClosePortAfterEachCall(self, openPortAEC):
        logger = self._setLogger(package=__name__)
        self.close_port_after_each_call = openPortAEC

        if openPortAEC:
            if self.serial.isOpen():
                logger.info('closing port...')
                self.serial.close()
        else:
            if not self.serial.isOpen():
                logger.info('opening port...')
                self.serial.open()



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
                    caller = inspect.stack()[3]
                    dummy, programFile, lineNumber, funcName, lineCode, rest = caller
                    if funcName == '<module>': funcName = '__main__'
                    str = "[{FUNC:<20}:{LINENO}] - {DATA}".format(FUNC=funcName, LINENO=lineNumber, DATA=data)
                    print (str)

        return nullLogger()


    def __repr__(self):
        """String representation of the :class:'.Instrument' object."""
            # address                    = {ADDRESS},
        return """{MOD}.{CLASS}
            <class-id                  = 0x{ID:x},
            mode                       = {MODE},
            close_port_after_each_call = {CPAEC},
            precalculate_read_size     = {PRS},
            debug                      = {DEBUG},
            STX                        = 0x{STX:02x},
            ETX                        = 0x{ETX:02x},
            serial-id                  = {SERIAL},>
                """.format(
                        MOD=self.__module__,
                        CLASS=self.__class__.__name__,
                        ID=id(self),
                        MODE=self.mode,
                        CPAEC=self.close_port_after_each_call,
                        PRS=self.precalculate_read_size,
                        DEBUG=self.debug,
                        SERIAL=self.serial,
                        STX=self.STX,
                        ETX=self.ETX
            )
                        # ADDRESS=self.address,

    # def displayPortParameters(self):
    #     print ('mode:                           {0}'.format(self._MODE_ASCII))
    #     print ('STX:                            0x{0:02x}'.format(self.STX))
    #     print ('ETX:                            0x{0:02x}'.format(self.ETX))
    #     print ('CLOSE_PORT_AFTER_EACH_CALL:     {0}'.format(self.close_port_after_each_call))
    #     print ('precalculate_read_size:         {0}'.format(self.precalculate_read_size))


    def _getCRC8(self, byteArray_data):
        logger = self._setLogger(package=__name__)
        crcValue = 0
        for byte in byteArray_data:
            # if isinstance(byte, str): byte = ord(byte)            # onverte nel valore ascii
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
        logger.debug ("byte to be converted: {0} - type: {1}".format(byte, type(byte)))
        # if isinstance(byte, str): byte = ord(byte)            # onverte nel valore ascii

        # print ('....', type(byte), byte)
        # logger.debug ("converting: x{0:02X}".format(byte))

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
        # if isinstance(byte1, str): byte1 = ord(byte1)            # onverte nel valore ascii
        # if isinstance(byte2, str): byte2 = ord(byte2)            # onverte nel valore ascii

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
    # - Lettura dati fino a:
    # -     EOD = None ... fino al primo NULL byte
    # -     EOD = xxx ... fino al char xxx
    # - Ritorna una bytearray di integer
    #######################################################################
    def _readBufferRaw(self, EOD=None):
        logger = self._setLogger(package=__name__)

        if self.close_port_after_each_call:
            logger.debug('openig port...')
            self.serial.open()

        # print ('..............', EOD)
        buffer = bytearray()

        if EOD:
            chInt=-1
            while chInt != EOD:
                ch = self.serial.read(1)       # ch e' un bytes
                if ch == b'': continue
                chInt = int.from_bytes(ch, 'little')
                buffer.append(chInt)
                logger.debug( "Received byte: {0:02x}... waiting for {1:02x}".format(chInt, EOD) )

        else:
            while True:
                ch = self.serial.read(1)       # ch e' un bytes
                if ch == b'':
                    # print ('break')
                    break
                chInt = int.from_bytes(ch, 'little')
                buffer.append(chInt)
                logger.debug( "Received byte: {0:02x}... waiting for NULL".format(chInt) )

        if self.close_port_after_each_call:
            logger.debug('closing port...')
            self.serial.close()

        return buffer

    #######################################################################
    # - by Loreto
    # - EOD = int('0x0A', 16) # integer
    # - EOD = None   ... legge fino al primo byte null
    #######################################################################

    def readRawData(self, EOD=None, hex=False, text=False, char=False):
        logger = self._setLogger(package=__name__)

        printableIChars = [ord(c) for c in string.printable]

        line = self._readBufferRaw(EOD=EOD)
        # hexData         = ' '.join('{0:02x}'.format(x) for x in line)
        # print (hexData)

        if line:
            if isinstance(line, bytes):
                line = line.decode('utf-8')


            printableChars = []
            for i in line:
                cc = chr(i)
                if i > 31 and i < 127:
                    printableChars.append(cc)
                else:
                    printableChars.append(" ")


            if hex:
                hexData         = ' '.join('{0:02x}'.format(x) for x in line)
                print ('{DESCR:^10}:  {DATA}'.format(DESCR="raw", DATA=hexData))

            if char:
                print ('{DESCR:^10}:  {DATA}'.format(DESCR="chr", DATA='  '.join(printableChars)))

            if text:
                print ('{DESCR:^10}:  {DATA}'.format(DESCR="line", DATA=''.join(printableChars)))


        return line



    #######################################################################
    # - Lettura dati da StartOfData fino a EndOfData
    # - Ritorna una bytearray di integer
    #######################################################################
    def _readBuffer(self):
        logger = self._setLogger(package=__name__)

        if self.close_port_after_each_call:
            logger.debug('openig port...')
            self.serial.open()

        buffer = bytearray()

        chInt=-1
        while chInt != self.STX:
            ch = self.serial.read(1)       # ch e' un bytes
            if ch == b'': continue
            chInt = int.from_bytes(ch, 'little')


        buffer.append(chInt)
        logger.debug( "Received: STX")
        chInt=-1
        while chInt != self.ETX:
            ch = self.serial.read(1)       # ch e' un bytes
            if ch == b'': continue
            chInt = int.from_bytes(ch, 'little')
            buffer.append(chInt)
            logger.debug( "Received: byte hex: {0:02x}... waiting for {1:02x}".format(chInt, self.ETX) )

        if self.close_port_after_each_call:
            logger.debug('closing port...')
            self.serial.close()

        return buffer





    #######################################################################
    # - by Loreto
    # - Lettura dati bsato sul protocollo:
    # -     RS485 protocol library by Nick Gammon
    # - STX - data - CRC - ETX
    # - A parte STX e ETX tutti gli altri byte sono inviati come due nibble
    # -  byte complemented (incluso il CRC)
    # -  only values sent would be (in hex):
    # -    0F, 1E, 2D, 3C, 4B, 5A, 69, 78, 87, 96, A5, B4, C3, D2, E1, F0
    # -  Con il fatto che solo i byte di sopra possono essere inviati,
    # -  il controllo su di essi forse fa venire meno il CRC e quindi
    # -  l'ho inserito come flag
    #
    # - credo che questa funzione venga chiamata non direttamente da me
    # - in quanto ho notato che non prende ulteriori parametri.
    #######################################################################
    def readData(self, fDEBUG=False):
        logger = self._setLogger(package=__name__)


        rawData = self._readBuffer()
        msg = '{TITLE:<15}: ({LEN}) {DATA}'.format(TITLE='full data', LEN=len(rawData), DATA=' '.join('{:02X}'.format(x) for x in rawData))
        logger.debug(msg)

            # Prendiamo i dati fissi
        if not rawData[0] == self.STX:
            msg = 'ERROR: STX missed'
            print(msg)
            logger.error(msg)
            return bytearray(), rawData

        if not rawData[-1] == self.ETX:
            msg = 'ERROR: ETX missed'
            print(msg)
            logger.error(msg)
            return bytearray(), rawData


            # ---------------------------------------------
            # - ricostruzione dei bytes originari
            # - byte = byte1_HighNibble*16 + byte2_HighNibble
            # - si potrebbe usare la funzione _combineComplementedByte
            # -    che provvede anche a fare la verifica che
            # -    il secondo nibble sia il complemento del primo ma
            # -    avendo verificato che il byte si trova nei self._validBytes
            # ---------------------------------------------

            # il trick che segue ci permette di prelevare due bytes alla volta
        payLoad = bytearray()
        payLoadNibbled  = rawData[1:-1] # skip STX and ETX - include nibbled_data+nibbled_CRC
        xy = iter(payLoadNibbled)
        for byte1, byte2 in zip(xy, xy):
                # re-build real byte
            if byte1 in self._validBytes and byte2 in self._validBytes:
                byte1_HighNibble = (byte1 >> 4) & 0x0F
                byte2_HighNibble = (byte2 >> 4) & 0x0F
                realByte = byte1_HighNibble*16 + byte2_HighNibble


            else:
                msg = 'ERROR: some byte corrupted byte1:{0:02x} byte2:{1:02x}'.format(byte1, byte2)
                print(msg)
                logger.error(msg)
                return bytearray(), rawData

            payLoad.append(realByte)


            # -----------------------------------------------------------------------
            # - Una volta ricostruidi i bytes origilali,
            # - calcoliamo il CRC sui dati (ovviamento escluso il byte di CRC stesso)
            # -----------------------------------------------------------------------
        CRC_calculated  = self._getCRC8(payLoad[:-1])
            # ---------------------------------
            # - check CRC (drop STX and ETX)
            # ---------------------------------
        CRC_received    = payLoad[-1]
        payLoad         = payLoad[:-1]

        logger.debug("    CRC received  : x{0:02X}".format(CRC_received))
        logger.debug("    CRC calculated: x{0:02X}".format(CRC_calculated))



        if not CRC_received == CRC_calculated:
            logger.error('Il valore di CRC non coincide')
            print ('ERROR: Il valore di CRC non coincide')
            print ()
            print ("    CRC received  : x{0:02X}".format(CRC_received))
            print ("    CRC calculated: x{0:02X}".format(CRC_calculated))
            print ()
            return bytearray(), rawData

        if fDEBUG:
            print('from {sADDR:03}  to {dADDR:03}'.format(sADDR=payLoad[0], dADDR=payLoad[1]))
            print ('{DESCR:<10}: {DATA}'.format(DESCR="raw data", DATA=' '.join('{0:02x}'.format(x) for x in rawData)))
            print ('{DESCR:<10}: {DATA}'.format(DESCR="payload", DATA=' '.join('{0:02x}'.format(x) for x in payLoad)))
            print ('{DESCR:<10}:       {DATA}'.format(DESCR="payload", DATA=' '.join('{0:>2}'.format(chr(x)) for x in payLoad[2:])))


        return payLoad, rawData



    #######################################################################
    # - writeDataSDD - con parametri di input diversi
    # -    richiama comunque writeData
    #######################################################################
    def writeDataSDD(self, sourceAddress, destAddress, dataStr, fDEBUG=False):
        ''' formato esplicito dei parametri '''
        dataToSend = bytearray()
        dataToSend.append(sourceAddress)
        dataToSend.append(destAddress)
        for x in dataStr:
            dataToSend.append(ord(x))

        dataSent = self.writeData(dataToSend, fDEBUG=fDEBUG)
        return dataSent


    #######################################################################
    # - writeDataCMD - con parametri di input diversi
    # -    richiama comunque writeData
    #######################################################################
    def writeDataCMD(self, command, fDEBUG=False):
        ''' formato CLASS dei parametri '''
        dataToSend = bytearray()
        dataToSend.append(command.sourceAddr)
        dataToSend.append(command.destAddr)
        for x in command.dataStr:
            dataToSend.append(ord(x))

        dataSent = self.writeData(dataToSend, fDEBUG=fDEBUG)
        return dataSent




    #######################################################################
    # - by Loreto
    # - Scrittura dati basato sul protocollo:
    # -     RS485 protocol library by Nick Gammon
    # - STX - data - CRC - ETX
    # - A parte STX e ETX tutti gli altri byte sono inviati come due nibble
    # -  byte complemented (incluso il CRC)
    # -  only values sent would be (in hex):
    # -    0F, 1E, 2D, 3C, 4B, 5A, 69, 78, 87, 96, A5, B4, C3, D2, E1, F0
    #######################################################################
    def writeData(self, data, fDEBUG=False):
        ''' formato in bytearray dei parametri '''
        logger = self._setLogger(package=__name__)
        if fDEBUG:
            print()
            print('source: {sADDR:03}  dest: {dADDR:03}'.format(sADDR=data[0], dADDR=data[1]))
            print ('{DESCR:<10}: {DATA}'.format(DESCR="payload", DATA=' '.join('{0:02x}'.format(x) for x in data)))

            # - preparaiamo il bytearray con i dati da inviare
        dataToSend=bytearray()

            # - STX nell'array
        dataToSend.append(self.STX)

            # - Data nell'array
        for thisByte in data:
            byte1, byte2 = self._splitComplementedByte(thisByte)
            dataToSend.append(byte1)
            dataToSend.append(byte2)

            # - CRC nell'array
        if self.CRC:
            CRC_value    = self._getCRC8(data)
            byte1, byte2 = self._splitComplementedByte(CRC_value)
            dataToSend.append(byte1)
            dataToSend.append(byte2)

            # - ETX
        dataToSend.append(self.ETX)

        if self.close_port_after_each_call:
            self.serial.open()

            # INVIO dati
        self.serial.write(dataToSend)


        if self.close_port_after_each_call:
            self.serial.close()

        if fDEBUG:
            print ('{DESCR:<10}: {DATA}'.format(DESCR="raw data", DATA=' '.join('{0:02x}'.format(x) for x in dataToSend)))

        return dataToSend




class LnClass(): pass
################################################################################
# - M A I N
# - Prevede:
# -  2 - Controllo parametri di input
# -  5 - Chiamata al programma principale del progetto
################################################################################
if __name__ == '__main__':
    import time
    Sintax = """
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
    else:
        print (Sintax)
        sys.exit()




    LnRs485                = LnRs485_Instrument   # short pointer alla classe
    rs485                  = LnClass()
    rs485.MASTER_ADDRESS   = 0
    rs485.bSTX             = b'\x02'
    rs485.bETX             = b'\x03'
    rs485.usbDevPath       = '/dev/ttyUSB{0}'.format(portNO)
    # rs485.baudRate         = 9600
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
            address = 5
            print('setting port {0} to address {1}'.format(rs485.usbDevPath, address))
            monPort = LnRs485(rs485.usbDevPath, address, rs485.mode, logger=None)  # port name, slave address (in decimal)
            monPort.CRC = True

            print ('... press ctrl-c to stop the process.')
            while True:
                payLoad, rawData = monPort.readData()
                print ('rawData (Hex):  {0}'.format(' '.join('{0:02x}'.format(x) for x in rawData)))
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
            wrPort = LnRs485(rs485.usbDevPath, address, rs485.mode, logger=None)  # port name, slave address (in decimal)
            # - setting di alcuni parametri delle funzioni
            # - me li ritrovo come self.PARAM
            wrport.CRC       = False
            print ('... press ctrl-c to stop the process.')
            index = 0
            basedata = 'Loreto.'
            while True:
                index += 1
                dataToSend  = '[{0}.{1:04}]'.format(basedata, index)
                line        = '[{0}:{1:04}] - {2}'.format(rs485.usbDevPath, index, dataToSend)
                print (line)
                dataSent = wrPort.writeData(dataToSend, CRC=True)
                print ('sent (Hex): {0}'.format(' '.join('{0:02x}'.format(x) for x in dataSent)))
                print()
                time.sleep(5)


        except (KeyboardInterrupt) as key:
            print ("Keybord interrupt has been pressed")
            sys.exit()


    else:
        print(gv.INPUT_PARAM.actionCommand, 'not available')


