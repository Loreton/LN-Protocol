#!/usr/bin/env python3
#
# modified by Loreto:           2017-03-10_14.50.01
# #####################################################

# updated by ...: Loreto Notarantonio
# Version ......: 06-12-2017 17.16.59

import LnLib as Ln
import os
import serial       # sudo pip3.4 install pyserial
import sys
import inspect
import string
import time

class LnClass():
    def __init__(self):
        self.rCode  = 0
        self.errMsg = None

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

read_TIMEOUT  = 0.05
"""Default value for the timeout value in seconds (float)."""

#####################
## Named constants ##
#####################

MODE_RTU   = 'rtu'
MODE_ASCII = 'ascii'



# -----------------------------------------------------------------------
# - con il gioco del complementedByte, gli unici byte che dovrebbero
# - circolare sono i seguenti al di là dello STX ed ETX
# -----------------------------------------------------------------------
LnRs485_validBytesHex = [
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




from . LnRs485_Formatter import Formatter485

#####################################################################
# - MAIN LnRS485 CLASS
#####################################################################
class LnRs485_Instrument():
    def __init__(self, port, mode='ascii', baudrate=9600, logger=None, myDict=LnClass):

        if logger:
            self._setLogger = logger
        else:
            self._setLogger = self._internaLogger

        logger = self._setLogger(package=__package__)
        self._myDict = myDict


        if port not in _SERIALPORTS or not _SERIALPORTS[port]:
            try:
                logger.info('opening port...')
                self.serial = _SERIALPORTS[port] = serial.Serial(
                                                    port     = port,
                                                    baudrate = baudrate,
                                                    parity   = serial.PARITY_NONE,
                                                    bytesize = serial.EIGHTBITS,
                                                    stopbits = serial.STOPBITS_ONE,
                                                    rtscts   = False,
                                                    xonxoff  = False,
                                                    dsrdtr   = False,
                                                    timeout  = read_TIMEOUT)

            except (Exception) as why:
                print ('ERROR:  ', str(why))
                sys.exit()

        else:
            self.serial = _SERIALPORTS[port]
            if self.serial.port is None:
                logger.info('opening port...')
                self.serial.open()
                # - chissà se sono importanti....
                self.serial.reset_input_buffer()        # clear input  buffer
                self.serial.reset_output_buffer()       # clear output buffer

        self._validBytes=bytearray([int(i, 16) for i in LnRs485_validBytesHex]) # creiamo un array di integer

        self.mode = mode
        """Slave mode (str), can be MODE_RTU or MODE_ASCII.  Most often set by the constructor (see the class documentation).
        New in version 0.6.
        """

        self._printableChars                = list(range(31,126))
        self._sendCounter = 0

        self._STX = 0xF0
        self._ETX = 0xF1
        self._CRC = True

        self._close_port_after_each_call = False
        """If this is :const:'True', the serial port will be closed after each call. """
        if  self._close_port_after_each_call: self.serial.close()

            # classe per formattare i dati
        self.formatter = Formatter485

        self._rs485RxRawData    = bytearray()    # contiene i dati letti o da scrivere sulla rs485
        self._rs485RxPayLoad    = bytearray()    # contiene i dati letti ripuliti da STX, CRC, ETX
        self._rs485RxRawHexData = ''             # contiene i dati raw convertiti in Hex



    def _internaLogger(self, package=None):
        ##############################################################################
        # - classe che mi permette di lavorare nel caso il logger non sia richiesto
        ##############################################################################
        class nullLogger():
                def __init__(self, package=None, stackNum=1):
                    pass
                def info(self, data): pass
                def debug(self, data): pass
                    # self._print(data)
                def error(self, data):  pass
                def warning(self, data):  pass

        return nullLogger()


    def __repr__(self):
        """String representation of the :class:'.Instrument' object."""
            # address                    = {ADDRESS},
        return """{MOD}.{CLASS}
            <class-id                  = 0x{ID:x},
            mode                       = {MODE},
            close_port_after_each_call = {CPAEC},
            CRC                        = {CRC},
            STX                        = 0x{STX:02x},
            ETX                        = 0x{ETX:02x},
            serial-id                  = {SERIAL},>
                """.format(
                        MOD=self.__module__,
                        CLASS=self.__class__.__name__,
                        ID=id(self),
                        MODE=self.mode,
                        CPAEC=self._close_port_after_each_call,
                        SERIAL=self.serial,
                        CRC=self._CRC,
                        STX=self._STX,
                        ETX=self._ETX
            )
                        # ADDRESS=self.address,



    # =====================================================
    # - _getCRC8
    # =====================================================
    def _getCRC8(self, byteArray_data):
        logger = self._setLogger(package=__package__)
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
    def _prepareRs485Data(self, payload):
        assert type(payload)==bytearray
        logger = self._setLogger(package=__package__)

             # - preparaiamo il bytearray con i dati da inviare
        dataToSend=bytearray()

            # - STX nell'array
        dataToSend.append(self._STX)

            # - Data nell'array
        for thisByte in payload:
            byte1, byte2 = self._splitComplementedByte(thisByte)
            dataToSend.append(byte1)
            dataToSend.append(byte2)

            # - CRC nell'array
        if self._CRC:
            CRC_value    = self._getCRC8(txData)
            byte1, byte2 = self._splitComplementedByte(CRC_value)
            dataToSend.append(byte1)
            dataToSend.append(byte2)

            # - ETX
        dataToSend.append(self._ETX)

        return dataToSend


    # ---------------------------------------------
    # -     byte1 = aaaa !aaaa
    # -     byte2 = bbbb !bbbb
    # -     byte = byte1_HNibble * 16 + byte2_HNibble
    # ---------------------------------------------
    def _combineComplementedByte(self, byte1, byte2):
        logger = self._setLogger(package=__package__)

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



    # ---------------------------------------------
    # - aaaa bbbb
    # -     byte1 = aaaa !aaaa
    # -     byte2 = bbbb !bbbb
    # -     byte = byte1_HNibble * 16 + byte2_HNibble
    # ---------------------------------------------
    def _splitComplementedByte(self, byte):
        logger = self._setLogger(package=__package__)
        logger.debug ("byte to be converted: {0} - type: {1}".format(byte, type(byte)))

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






    #######################################################################
    # - Lettura dati fino a:
    # - Ritorna: una bytearray di integer ed gli stessi formattati HEX
    # -    raw_data:  bytearray di integer  oppure vuoto
    # -    hex_data:  dati in Hex oppure None
    #######################################################################
    def _serialRead(self, timeoutValue=1000, fDEBUG=False):
        logger = self._setLogger(package=__package__)

        if self._close_port_after_each_call:
            logger.debug('opening port...')
            self.serial.open()

        _dataBuffer = bytearray()
        fLOOP        = True
        fDATA_AVAIL  = False

        # facciamo partire il timer
        timeStart = time.time()*1000
        timeEnd   = timeStart+timeoutValue
        TIMEOUT = True      # flag per indicare se siamo andati in timeout o meno
        logger.debug( "starting timer... for {} mSec".format(timeoutValue))


        # loop fino a che non abbiamo ricevuto dati
        while True:
            elapsed = int((time.time()*1000)-timeStart)
                # - in attesa di un byte
            ch    = self.serial.read(1)       # ch e' un type->bytes

                # ------------------------------------------
                # - se riceviamo un NULL:
                # -     - se non abbiamo nulla:
                # -         - se scaduto timeOut... usciamo
                # -         - else continue
                # - quindi usciamo solo per timeOut oppure
                # - dopo un NULL dopo avere ricevuto qualcosa
                # ------------------------------------------
            if ch == b'':
                if fDATA_AVAIL:
                    break
                elif elapsed >= timeoutValue:
                    logger.debug( "elapsed {0}/{1}".format(elapsed, timeoutValue))
                    break
                else:
                    continue

            chInt = int.from_bytes(ch, 'little')
            _dataBuffer.append(chInt)
            fDATA_AVAIL = True
            logLine = "Received byte: {0:02x}".format(chInt)


        if self._close_port_after_each_call:
            logger.debug('closing port...')
            self.serial.close()

        self._rs485RxRawData    = _dataBuffer
        self._rs485RxRawHexData = ' '.join('{0:02x}'.format(x) for x in self._rs485RxRawData)



    #######################################################################
    # - Scrittura dati sulla seriale
    #######################################################################
    def _serialWrite(self, txData):
        assert type(txData)==bytearray

        logger = self._setLogger(package=__package__)

        if self._close_port_after_each_call:
            self.serial.open()

            # INVIO dati
        logger.info('xmitting data on serial port')
        self.serial.write(txData)

        if self._close_port_after_each_call:
            self.serial.close()



    #######################################################################
    # - Scrittura dati sulla seriale
    #######################################################################
    def _rs485Write(self, payload):
        assert type(txData)==bytearray

            # - preparaiamo il bytearray con i dati da inviare
        dataToSend=bytearray()

            # - STX nell'array
        dataToSend.append(self._STX)

            # - Data nell'array
        for thisByte in payload:
            byte1, byte2 = self._splitComplementedByte(thisByte)
            dataToSend.append(byte1)
            dataToSend.append(byte2)

            # - CRC nell'array
        if self._CRC:
            CRC_value    = self._getCRC8(txData)
            byte1, byte2 = self._splitComplementedByte(CRC_value)
            dataToSend.append(byte1)
            dataToSend.append(byte2)

            # - ETX
        dataToSend.append(self._ETX)

            # INVIO dati
         self._serialWrite(txData)




    #######################################################################
    # # PUBLIC methods
    #######################################################################



    def getSeqCounter(self):
        self._sendCounter += 1
        yy = self._sendCounter.to_bytes(2, byteorder='big')
        return yy

    def SetSTX(self, value):
        logger = self._setLogger(package=__package__)
        if isinstance(value, str):
            value = int(value, 16)
        self._STX = value
        logger.info('setting STX to {}'.format(self._STX))

    def SetETX(self, value):
        logger = self._setLogger(package=__package__)
        if isinstance(value, str):
            value = int(value, 16)
        self._ETX = value
        logger.info('setting ETX to {}'.format(self._ETX))

    def SetCRC(self, bFlag):
        logger = self._setLogger(package=__package__)
        self._CRC = eval(bFlag)
        logger.info('setting CRC to {}'.format(self._CRC))

    def ClosePortAfterEachCall(self, bFlag):
        logger = self._setLogger(package=__package__)
        self._close_port_after_each_call = bFlag

        if bFlag:
            if self.serial.isOpen():
                logger.info('closing port...')
                self.serial.close()
        else:
            if not self.serial.isOpen():
                logger.info('opening port...')
                self.serial.open()

    def Close(self):
        logger = self._setLogger(package=__package__)
        if self.serial.isOpen():
            logger.info('closing port...')
            self.serial.close()



    # def _getSeqNumber(self):
    #     self._sendCounter += 1
    #     yy = self._sendCounter.to_bytes(2, byteorder='big')
    #     return yy




    ######################################################
    # - @property
    # - Utilizzo i metodi come fossero attributi
    # - se compare l'utput di __repr__ vuol dire che
    # - è stato omesso @property
    ######################################################
    @property
    def rawData(self):
        return self._rs485RxRawData

    @property
    def cleanRxData(self):
        self._rs485RxRawData = bytearray()
        self._rs485RxRawHexData = ''
        self._rs485RxPayLoad = ''

    @property
    def rawHex(self):
        hexData, hexMsg = self.formatter._toHex(self._rs485RxRawData)
        return hexMsg

    @property
    def rawText(self):
        text, char = self.formatter._toText(self)
        return text

    @property
    def rawChr(self):
        text, char = self.formatter._toText(self)
        return char




    @property
    def payload(self):
        self.formatter._verifyData(self)
        return self._rs485RxPayLoad


    @property
    def payloadHex(self):
        self.formatter._verifyData(self)
        hexData, hexMsg = self.formatter._toHex(self._rs485RxPayLoad)
        return hexMsg

    @property
    def payloadToDict(self):
        # if not self._rs485RxPayLoad:
        self.formatter._verifyData(self)
        myDict = self.formatter._payloadToDict(self)
        return myDict

    # @property
    def toRs485(self, payload):
        self._rs485TxRawData = payload
        self._rs485TxRawData = _prepareRs485Data(self, self._rs485TxRawData)
        # _serialWrite(self, self._rs485TxRawData):







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
                dataSent = wrPort.sendData(dataToSend, CRC=True)
                print ('sent (Hex): {0}'.format(' '.join('{0:02x}'.format(x) for x in dataSent)))
                print()
                time.sleep(5)


        except (KeyboardInterrupt) as key:
            print ("Keybord interrupt has been pressed")
            sys.exit()


    else:
        print(gv.INPUT_PARAM.actionCommand, 'not available')







