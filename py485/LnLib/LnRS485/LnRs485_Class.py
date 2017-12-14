#!/usr/bin/env python3
#
# modified by Loreto:           2017-03-10_14.50.01
# #####################################################

# updated by ...: Loreto Notarantonio
# Version ......: 14-12-2017 09.42.29

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
class LnRs485():
    def __init__(self, port, mode='ascii', baudrate=9600, logger=None, myDict=LnClass):

        if logger:
            self._setLogger = logger
        else:
            self._setLogger = self._internaLogger

        logger = self._setLogger(package=__name__)
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

        # self._rs485RxRawData    = bytearray()    # contiene i dati letti o da scrivere sulla rs485
        self._rs485RxPayLoad    = bytearray()    # contiene i dati letti ripuliti da STX, CRC, ETX
        # self._rs485RxRawHexData = ''             # contiene i dati raw convertiti in Hex

        self._TxDataRaw         =  bytearray()   # raw data in uscita   dalla seriale
        self._TxDataHex         =  ''            # raw data in uscita   dalla seriale

        # self._Rx                = self._myDict()
        # self._Tx                = self._myDict()

        # self._cleanData(self._Rx)
        # self._cleanData(self._Tx)

        # self._RxDataRaw         =  bytearray()   # raw data in ingresso dalla seriale
        # self._RxDataHex         =  ''            # raw data in ingresso dalla seriale
        self._fld               =  None            # dict che contiene i nomi dei campi del payload e la loro posizione nel pacchetto


        # - clean delle variabili di RX e TX
    # def _cleanData(self, ptr):
    #     ptr.raw           = self._myDict()
    #     ptr.payload       = self._myDict()

    #     ptr.raw.data      = bytearray()
    #     ptr.raw.hexd      = None
    #     ptr.raw.hexm      = None
    #     ptr.raw.fmted     = False

    #     ptr.payload.data  = bytearray()
    #     ptr.payload.hexd  = None
    #     ptr.payload.hexm  = None
    #     ptr.payload.fmted = False


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
    def _prepareRs485Packet(self, payload):
        assert type(payload)==bytearray
        logger = self._setLogger(package=__name__)

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

        self._rs485TxRawData = dataToSend
        # return dataToSend


    # ---------------------------------------------
    # -     byte1 = aaaa !aaaa
    # -     byte2 = bbbb !bbbb
    # -     byte = byte1_HNibble * 16 + byte2_HNibble
    # ---------------------------------------------
    def _combineComplementedByte(self, byte1, byte2):
        logger = self._setLogger(package=__name__)

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
        logger = self._setLogger(package=__name__)
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
    # - Lettura dati dalla seriale
    # - Ritorna: una bytearray di integer con i dati ricevuti oppure vuoto
    #######################################################################
    def _serialRead(self, timeoutValue=1000):
        logger = self._setLogger(package=__name__)

        if self._close_port_after_each_call:
            logger.debug('opening port...')
            self.serial.open()


        # facciamo partire il timer
        timeStart = time.time()*1000
        timeEnd   = timeStart+timeoutValue
        TIMEOUT = True      # flag per indicare se siamo andati in timeout o meno
        logger.debug( "starting timer... for {} mSec".format(timeoutValue))


        # loop fino a che non abbiamo ricevuto dati
        _dataBuffer = bytearray()
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
                if _dataBuffer:
                    break
                elif elapsed >= timeoutValue:
                    logger.debug( "elapsed {0}/{1}".format(elapsed, timeoutValue))
                    break
                else:
                    continue

            chInt = int.from_bytes(ch, 'little')
            _dataBuffer.append(chInt)
            logger.debug("Received byte: {0:02x}".format(chInt))


        if self._close_port_after_each_call:
            logger.debug('closing port...')
            self.serial.close()

        logger.debug("data received: {}".format(' '.join('{0:02x}'.format(x) for x in _dataBuffer)))
        return _dataBuffer






    #######################################################################
    # - Scrittura dati sulla seriale
    #######################################################################
    def _serialWrite(self, txData):
        logger = self._setLogger(package=__name__)
        assert type(txData)==bytearray


        if self._close_port_after_each_call:
            self.serial.open()

            # INVIO dati
        _HexData = ' '.join('{0:02x}'.format(x) for x in txData)
        _HexMsg = '{DESCR:^10}:  <data>{DATA}</data>'.format(DESCR="hex", DATA=_HexData)
        logger.info('xmitting data on serial port: ')
        logger.info(_HexMsg)
        self.serial.write(txData)

        if self._close_port_after_each_call:
            self.serial.close()






    #######################################################################
    # - Scrittura dati sulla seriale
    #######################################################################
    def _rs485Read(self, timeoutValue=2000, FORMAT=False):
        logger = self._setLogger(package=__name__)

        rawDict = self._myDict()
        plDict  = self._myDict()
        rawData = self._serialRead(timeoutValue=timeoutValue) # return bytearray
        rawDict.data = rawData
        plDict.data = None

        if rawData:
            if FORMAT:
                _rawDataFMTed = self.formatter._fmtData(self, rawData)
                rawDict.hexd = _rawDataFMTed['HEXD']
                rawDict.hexm = _rawDataFMTed['HEXM']
                rawDict.text = _rawDataFMTed['TEXT']
                rawDict.char = _rawDataFMTed['CHAR']

            payload = self._extractPayload(rawData)
            plDict.data = payload
            if payload and FORMAT:
                _payloadFMTed = self.formatter._fmtData(self, payload)
                plDict.hexd = _payloadFMTed['HEXD']
                plDict.hexm = _payloadFMTed['HEXM']
                plDict.text = _payloadFMTed['TEXT']
                plDict.char = _payloadFMTed['CHAR']
                plDict.dict = self.formatter._payloadToDict(self, payload)

        return rawDict, plDict


    #######################################################################
    # - Scrittura dati sulla seriale
    #######################################################################
    def _rs485Write(self, payload, fDEBUG=False):
        logger = self._setLogger(package=__name__)
        assert type(payload)==bytearray
        logger.info('payload: {}'.format(Formatter485._toHex(payload)[0]))

            # - prepariamo il bytearray per i dati da inviare
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
            CRC_value    = self._getCRC8(payload)
            byte1, byte2 = self._splitComplementedByte(CRC_value)
            dataToSend.append(byte1)
            dataToSend.append(byte2)

            # - ETX
        dataToSend.append(self._ETX)

        logger.info('dataToSend: {}'.format(Formatter485._toHex(dataToSend)[0]))

        # INVIO dati
        self._serialWrite(dataToSend)
        return dataToSend




    ######################################################
    # - unpack data
    # - partendo dal rawData:
    # -    1. riconosce STX ed ETX
    # -    2. verifica la correttezza del pacchetto CRC
    # -    3. ricostruisce i byte originali (2bytes --> 1 byte)
    # -    4. estrae il payload
    # -    5. ritorna payload in un bytearray
    ######################################################
    def _extractPayload(self, rawData):
        assert type(rawData) == bytearray
        logger = self._setLogger(package=__name__)

        logger.error('analizing rawData: {}'.format(' '.join('{0:02x}'.format(x) for x in rawData)))
            # cerchiamo STX
        for index, byte in enumerate(rawData):
            if byte == self._STX:
                rawData = rawData[index:]
                logger.info('STX has been found')
                break

            # cerchiamo ETX
        for index, byte in enumerate(rawData):
            if byte == self._ETX:
                rawData = rawData[:index+1]
                logger.info('ETX has been found')
                break


        if not rawData or not rawData[0] == self._STX or not rawData[-1] == self._ETX:
            errMsg = 'STX or ETX missed'
            logger.error(errMsg)
            return bytearray()


            # ---------------------------------------------
            # - ricostruzione dei bytes originari
            # - byte = byte1_HighNibble*16 + byte2_HighNibble
            # il trick che segue ci permette di prelevare due bytes alla volta
            # ---------------------------------------------
        _payloadData = bytearray()
        xy = iter(rawData[1:-1]) # skip STX and ETX
        for byte1, byte2 in zip(xy, xy):
                # re-build real byte
            if byte1 in self._validBytes and byte2 in self._validBytes:
                byte1_HighNibble = (byte1 >> 4) & 0x0F
                byte2_HighNibble = (byte2 >> 4) & 0x0F
                realByte = byte1_HighNibble*16 + byte2_HighNibble
                _payloadData.append(realByte)

            else:
                errMsg = 'some byte corrupted byte1:{0:02x} byte2:{1:02x}'.format(byte1, byte2)
                logger.error(errMsg)
                return bytearray()




            # -----------------------------------------------------------------------
            # - Una volta ricostruiti i bytes origilali,
            # - calcoliamo il CRC sui dati (ovviamento escluso il byte di CRC stesso)
            # -----------------------------------------------------------------------
        _CRC_calculated  = self._getCRC8(_payloadData[:-1]) # skipping ETX
        _CRC_received    = _payloadData[-1]

        logger.debug("    CRC received  : x{0:02X}".format(_CRC_received))
        logger.debug("    CRC calculated: x{0:02X}".format(_CRC_calculated))

            # ---------------------------------
            # - check CRC (drop STX and ETX)
            # ---------------------------------
        if not _CRC_calculated == _CRC_received:
            errMsg = 'Il valore di CRC non coincide'
            logger.error ('-')
            logger.error ("    CRC received  : x{0:02X}".format(_CRC_received))
            logger.error ("    CRC calculated: x{0:02X}".format(_CRC_calculated))
            logger.error ('-')
            Ln.Exit(9999)
            return bytearray()

        return _payloadData[:-1] # drop CRC



    #######################################################################
    # # PUBLIC methods
    #######################################################################



    def getSeqCounter(self):
        self._sendCounter += 1
        yy = self._sendCounter.to_bytes(2, byteorder='big')
        return yy

    def SetPayloadFieldName(self, mydict):
        logger = self._setLogger(package=__name__)
        assert type(mydict) == self._myDict

            # ---- solo per logging ------------
            # - per fare il logging ordinato per value
            # - trasformiamo il dict in una LIST di tuple
            # ---- solo per logging ------------
        xx = sorted(mydict.items(), key=lambda x:x[1])
        logger.debug('Payload fields name:')
        for k, v in xx:
            logger.debug('  {:<15}:{}'.format(k,v))
        self._fld = mydict



    def SetSTX(self, value):
        logger = self._setLogger(package=__name__)
        if isinstance(value, str):
            value = int(value, 16)
        self._STX = value
        logger.info('setting STX to {}'.format(self._STX))

    def SetETX(self, value):
        logger = self._setLogger(package=__name__)
        if isinstance(value, str):
            value = int(value, 16)
        self._ETX = value
        logger.info('setting ETX to {}'.format(self._ETX))

    def SetCRC(self, bFlag):
        # assert type(bFlag) == bool or type(bFlag) == str
        logger = self._setLogger(package=__name__)
        if isinstance(bFlag, bool):
            self._CRC = bFlag
        elif isinstance(bFlag, str):
            self._CRC = eval(bFlag)
        else:
            self._CRC = True
        logger.info('setting CRC to {}'.format(self._CRC))

    def ClosePortAfterEachCall(self, bFlag):
        logger = self._setLogger(package=__name__)
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
        logger = self._setLogger(package=__name__)
        if self.serial.isOpen():
            logger.info('closing port...')
            self.serial.close()


    # def formatData(self, rawData):
    #     _formattedData = self.formatter._fmtData(self, rs485data)
    #     _myData.payload.hexd = _formattedData['HEXD']
    #     _myData.payload.hexm = _formattedData['HEXM']
    #     _myData.payload.text = _formattedData['TEXT']
    #     _myData.payload.char = _formattedData['CHAR']

    ######################################################
    # - @property
    # - Utilizzo i metodi come fossero attributi
    # - se compare l'utput di __repr__ vuol dire che
    # - è stato omesso @property
    ######################################################





    def VerifyRs485Data(self, rawData):
        '''
            Prende in input un bytearray dei dati letti da seriale
            li valida per il protocollo RS485
            Se validi... formatta sia il payload che il formato raw
            ritornando un dictionary con due rami
        '''
        logger = self._setLogger(package=__name__)
        assert type(rawData) == bytearray
        _myData              = self._myDict()
        _myData.raw          = self._myDict()
        _myData.payload      = self._myDict()
            # default value
        _myData.raw.data     = bytearray()
        _myData.payload.data = bytearray()

        logger.debug('rawData: {}'.format(' '.join('{0:02x}'.format(x) for x in rawData)))
            # ritorna payload bytearray
        if rawData:
            rs485data = self._extractPayload(rawData)
            logger.debug('payload: {}'.format(' '.join('{0:02x}'.format(x) for x in rs485data)))

            if rs485data:
                _myData.raw.data     = rawData
                _myData.payload.data = rs485data

                _formattedData = self.formatter._fmtData(self, rs485data)
                _myData.payload.hexd = _formattedData['HEXD']
                _myData.payload.hexm = _formattedData['HEXM']
                _myData.payload.text = _formattedData['TEXT']
                _myData.payload.char = _formattedData['CHAR']

                _formattedData = self.formatter._fmtData(self, rawData)
                _myData.raw.hexd = _formattedData['HEXD']
                _myData.raw.hexm = _formattedData['HEXM']
                _myData.raw.text = _formattedData['TEXT']
                _myData.raw.char = _formattedData['CHAR']



        return _myData

    def FormatRawData(self, rawData):
        '''
            Prende in input un bytearray dei dati letti da seriale
            li formatta ritornando un dictionary con i diversi formati
        '''
        assert type(rawData) == bytearray
        _myData              = self._myDict()

            # default value
        _myData.data     = bytearray()

            # ritorna payload bytearray
        if rawData:
            _myData.data = rawData

            _formattedData = self.formatter._fmtData(self, rawData)
            _myData.hexd = _formattedData['HEXD']
            _myData.hexm = _formattedData['HEXM']
            _myData.text = _formattedData['TEXT']
            _myData.char = _formattedData['CHAR']

        return _myData


    # @property
    # def rawHex(self):
    #     hexData, hexMsg = self.formatter._toHex(self._RxDataRaw)
    #     return hexMsg

    # # @property
    # def RxRaw(self, text=False, hexd=False, hexm=False, char=False):
    #     if not self._RxDataCharMsg:
    #         data = self.formatter._fmtData(self, self._RxDataRaw)
    #         self._RxDataHexMsg  = data['HEXM']
    #         self._RxDataTextMsg = data['TEXT']
    #         self._RxDataCharMsg = data['CHAR']

    #     if   hexd:  return self._RxDataHex
    #     elif hexm:  return self._RxDataHexMsg
    #     elif text:  return self._RxDataTextMsg
    #     elif char:  return self._RxDataCharMsg
    #     else:
    #         return None

    # # @property
    # def RxPayload(self, text=False, hexd=False, hexm=False, char=False):
    #     data = self.formatter._fmtData(self, self._RxDataRaw)
    #     if hexd:
    #         return data['HEXD']
    #     elif hexm:
    #         return data['HEXM']
    #     elif text:
    #         return data['TEXT']
    #     elif char:
    #         return data['CHAR']
    #     return None

    # @property
    # def rawChr(self):
    #     text, char = self.formatter._toText(self)
    #     return char




    # @property
    # def payload(self):
    #     self.formatter._verifyData(self)
    #     return self._rs485RxPayLoad


    # @property
    # def payloadHex(self):
    #     self.formatter._verifyData(self)
    #     hexData, hexMsg = self.formatter._toHex(self._rs485RxPayLoad)
    #     return hexMsg

    # # @property
    # def getPayload(self, rawdata):
    #     self.formatter._extractPayload(self, rawdata)
    #     myDict = self.formatter._payloadToDict(self)
    #     return myDict


    # @property
    def PayloadToDict(self, payload):
        # self.formatter._verifyData(self)
        return self.formatter._payloadToDict(self, payload)
        # return myDict
        # return 'ciao'

    # @property
    # def toRs485(self, payload):
    #     self._prepareRs485Packet(self, payload)
        # self._rs485TxRawData.printDict()
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



