#!/usr/bin/env python3
#
# #####################################################

# updated by ...: Loreto Notarantonio
# Version ......: 14-12-2017 09.44.00



import serial       # sudo pip3.4 install pyserial
import string
import time

from . LnRs232_Class import LnRs232
from . LnRs232_Class import LnClass
from . LnRs485_Formatter import Formatter485

# -----------------------------------------------------------------------
# - con il gioco del complementedByte, gli unici byte che dovrebbero
# - circolare sono i seguenti al di là dello STX ed ETX
# -----------------------------------------------------------------------




#####################################################################
# - MAIN LnRS485 CLASS
#####################################################################
class LnRs485(LnRs232):
    def __init__(self, port, mode='ascii', baudrate=9600, logger=None, myDict=LnClass):

        super().__init__(port=port, mode=mode, baudrate=baudrate, logger=logger, myDict=myDict)

        self.__LnRs485_validBytesHex = [
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

        self._rs485ValidBytes=bytearray([int(i, 16) for i in self.__LnRs485_validBytesHex]) # creiamo un array di integer
        self._sendCounter = 0

        self._STX = 0x02
        self._ETX = 0x03
        self._CRC = True

            # classe per formattare i dati
        self.formatter = Formatter485

        # self._rs485RxPayLoad    = bytearray()    # contiene i dati letti ripuliti da STX, CRC, ETX
        self._fld               =  None            # dict che contiene i nomi dei campi del payload e la loro posizione nel pacchetto



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
                        MODE=self._mode,
                        CPAEC=self._close_port_after_each_call,
                        SERIAL=self._serial,
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
    # - Scrittura dati sulla seriale
    #######################################################################
    def read485(self, timeoutValue=2000, FORMAT=False):
        logger = self._setLogger(package=__name__)

        rawDict      = self._myDict()
        plDict       = self._myDict()
        rawData      = self.read232(timeoutValue = timeoutValue) # return bytearray
        rawDict.data = rawData
        plDict.data  = None

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
    def write485(self, payload, fDEBUG=False):
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
        self.write232(dataToSend)
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
            if byte1 in self._rs485ValidBytes and byte2 in self._rs485ValidBytes:
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
            if self._serial.isOpen():
                logger.info('closing port...')
                self._serial.close()
        else:
            if not self._serial.isOpen():
                logger.info('opening port...')
                self._serial.open()

    def Close(self):
        logger = self._setLogger(package=__name__)
        if self._serial.isOpen():
            logger.info('closing port...')
            self._serial.close()


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
    def PayloadToDict(self, payload):
        # self.formatter._verifyData(self)
        return self.formatter._payloadToDict(self, payload)
        # return myDict
        # return 'ciao'

