#!/usr/bin/env python3
#
# #####################################################

# updated by ...: Loreto Notarantonio
# Version ......: 26-01-2018 15.55.25



import serial       # sudo pip3.4 install pyserial
import string
import time

from . LnRs232_Class import LnRs232
from . LnRs232_Class import LnClass
# from . LnRs485_Formatter import Formatter485

# -----------------------------------------------------------------------
# - con il gioco del complementedByte, gli unici byte che dovrebbero
# - circolare sono i seguenti al di là dello STX ed ETX
# -----------------------------------------------------------------------


from . Data_Formatter import Formatter

#####################################################################
# - MAIN LnRS485 CLASS
#####################################################################
class LnRs485(LnRs232):
    def __init__(self,
                    port,
                    mode='ascii',
                    baudrate=9600,
                    STX = 0x02,
                    ETX = 0x03,
                    CRC = True,
                    setLogger=None,
                    myDict=LnClass):

        super().__init__(port=port, mode=mode, baudrate=baudrate, setLogger=setLogger, myDict=myDict)


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

        self._STX = int(STX, 16)
        self._ETX = int(ETX, 16)
        self._CRC = CRC

        self._fld               =  None            # dict che contiene i nomi dei campi del payload e la loro posizione nel pacchetto

            # classe per formattare i dati
        self._formatter = Formatter


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



    #######################################################################
    # # PUBLIC methods
    #######################################################################
    # @property
    def seqCounter(self):
        self._sendCounter += 1
        yy = self._sendCounter.to_bytes(2, byteorder='big')
        return yy

    def SetPayloadFieldName(self, mydict):
        logger = self._setLogger(package=__name__)
        logger = self._logger

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


    def ClosePortAfterEachCall(self, bFlag):
        logger = self._logger

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
        logger = self._logger

        if self._serial.isOpen():
            logger.info('closing port...')
            self._serial.close()
        else:
            logger.info('port was alreay closed...')





    # =====================================================
    # - __getCRC8
    # =====================================================
    def __getCRC8(self, byteArray_data):
        logger = self._logger


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
    def __splitComplementedByte(self, byte):
        # logger = self._logger --- meglio di no

            # first nibble
        c = byte >> 4;
        byteValue = (c << 4) | (c ^ 0x0F)
        highNibble = byteValue


            # second nibble
        c = byte & 0x0F;
        byteValue = (c << 4) | (c ^ 0x0F)
        lowNibble = byteValue

        # logger.info ("byte x{BYTE:02X} converted to: HIGH: x{HI:02X} - LOW: x{LO:02X}".format(BYTE=byte, HI=highNibble, LO=lowNibble))

            # second two bytes
        return highNibble, lowNibble





    #######################################################################
    # - Scrittura dati sulla seriale
    #######################################################################
    def read485(self, timeoutValue=2000):

        data485 = self._myDict()
        data485 = self._myDict()
        data232 = self._myDict()
        data232.raw = bytearray() # empty
        data485.raw = bytearray() # empty

            # - bytearray of received data....
        rcvd232Data  = self.read232(timeoutValue = timeoutValue)

        if rcvd232Data:
            data232      = self._formatter._fmtData(self, rcvd232Data, self._myDict) # format payload
            payloadArray = self.__extractPayload(rcvd232Data)    # extract payload
            data485      = self._formatter._fmtData(self, payloadArray, self._myDict) # format payload
            data485.dict = self._formatter._payloadFields(self, payloadArray, self._myDict) # create a dictionary with fields


            # - return dict.raw dict.hexd dict.hexm dict.text dict.char
        return data232, data485



    #######################################################################
    # - Scrittura dati sulla seriale
    #######################################################################
    def write485(self, payload):
        '''
        return dict.raw dict.hex dict.hexm dict.text dict.char
        '''
        assert type(payload)==bytearray

        logger = self._setLogger(package=__name__)


        logger.info('payload: {}'.format(self._formatter._toHex(payload)[0]))

            # - prepariamo il bytearray per i dati da inviare
        dataToSend=bytearray()

            # - STX nell'array
        dataToSend.append(self._STX)

            # - Data nell'array
        for thisByte in payload:
            byte1, byte2 = self.__splitComplementedByte(thisByte)
            dataToSend.append(byte1)
            dataToSend.append(byte2)

            # - CRC nell'array
        if self._CRC:
            CRC_value    = self.__getCRC8(payload)
            byte1, byte2 = self.__splitComplementedByte(CRC_value)
            dataToSend.append(byte1)
            dataToSend.append(byte2)

            # - ETX
        dataToSend.append(self._ETX)

        logger.info('dataToSend: {}'.format(self._formatter._toHex(dataToSend)[0]))

        # INVIO dati
        self.write232(dataToSend)
        data232 = self._formatter._fmtData(self, dataToSend, self._myDict)
        return data232




    ######################################################
    # - unpack data
    # - partendo dal rawData:
    # -    1. riconosce STX ed ETX
    # -    2. verifica la correttezza del pacchetto CRC
    # -    3. ricostruisce i byte originali (2bytes --> 1 byte)
    # -    4. estrae il payload
    # -    5. ritorna payload in un bytearray
    ######################################################
    def __extractPayload(self, rawData):
        '''
            - unpack data (partendo dal rawData):
            -    1. riconosce STX ed ETX
            -    2. verifica la correttezza del pacchetto CRC
            -    3. ricostruisce i byte originali (2bytes --> 1 byte)
            -    4. estrae il payload
            -    5. ritorna payload in un bytearray
        '''
        assert type(rawData) == bytearray
        logger = self._logger

        logger.info('analizing rawData: {}'.format(' '.join('{0:02x}'.format(x) for x in rawData)))
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
        _CRC_calculated  = self.__getCRC8(_payloadData[:-1]) # skipping ETX
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


