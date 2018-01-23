#!/usr/bin/env python3
#
# #####################################################

# updated by ...: Loreto Notarantonio
# Version ......: 23-01-2018 08.33.43



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
    def __init__(self, port, mode='ascii', baudrate=9600, useLogger=None, myDict=LnClass):

        super().__init__(port=port, mode=mode, baudrate=baudrate, useLogger=useLogger, myDict=myDict)

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
        # self.formatter = Formatter485

        # self._rs485RxPayLoad    = bytearray()    # contiene i dati letti ripuliti da STX, CRC, ETX
        self._fld =  None            # dict che contiene i nomi dei campi del payload e la loro posizione nel pacchetto

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
    @property
    def _seqCounter(self):
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

        logger = self._setLogger(package=__name__, exiting=True)


    def SetSTX(self, value):
        logger = self._setLogger(package=__name__)
        if isinstance(value, str):
            value = int(value, 16)
        self._STX = value
        logger.info('setting STX to {}'.format(self._STX))

        logger = self._setLogger(package=__name__, exiting=True)

    def SetETX(self, value):
        logger = self._setLogger(package=__name__)
        if isinstance(value, str):
            value = int(value, 16)
        self._ETX = value
        logger.info('setting ETX to {}'.format(self._ETX))

        logger = self._setLogger(package=__name__, exiting=True)


    def SetCRC(self, bFlag):
        logger = self._setLogger(package=__name__)
        if isinstance(bFlag, bool):
            self._CRC = bFlag
        elif isinstance(bFlag, str):
            self._CRC = eval(bFlag)
        else:
            self._CRC = True
        logger.info('setting CRC to {}'.format(self._CRC))

        logger = self._setLogger(package=__name__, exiting=True)


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
        logger = self._setLogger(package=__name__, exiting=True)

    def Close(self):
        logger = self._setLogger(package=__name__)
        if self._serial.isOpen():
            logger.info('closing port...')
            self._serial.close()
        logger = self._setLogger(package=__name__, exiting=True)




    # =====================================================
    # - _getCRC8
    # =====================================================
    def _getCRC8(self, byteArray_data):
        logger = self._setLogger(package=__name__)
        crcValue = 0
        for byte in byteArray_data:

            # logger.debug('byte: int:{0} hex: {0:02x} - crcValue int:{1} hex: {1:02x}'.format(byte, crcValue))
            b2 = byte
            if (byte < 0):
                b2 = byte + 256
            for i in range(8):
                odd = ((b2^crcValue) & 1) == 1
                crcValue >>= 1
                b2 >>= 1
                if (odd):
                    crcValue ^= 0x8C # this means crc ^= 140

        logger.info('CRC value: int:{0} hex: {0:02x}'.format(crcValue))
        logger = self._setLogger(package=__name__, exiting=True)
        return crcValue






    # ---------------------------------------------
    # - aaaa bbbb
    # -     byte1 = aaaa !aaaa
    # -     byte2 = bbbb !bbbb
    # -     byte = byte1_HNibble * 16 + byte2_HNibble
    # ---------------------------------------------
    def _splitComplementedByte(self, byte):
        assert type(byte) == int
        logger = self._setLogger(package=__name__)

            # first nibble
        c = byte >> 4;
        byteValue = (c << 4) | (c ^ 0x0F)
        highNibble = byteValue

            # second nibble
        c = byte & 0x0F;
        byteValue = (c << 4) | (c ^ 0x0F)
        lowNibble = byteValue

        logger.debug ("byte: {B:02X} converted in: lowNibble: {L:02X} - highNibble: {H:02X}".format(B=byte, L=lowNibble, H=highNibble) )

        logger = self._setLogger(package=__name__, exiting=True)

            # second two bytes
        return highNibble, lowNibble





    #######################################################################
    # - Scrittura dati sulla seriale
    #######################################################################
    def read485(self, timeoutValue=2000):
        ''' return:
                dict232.raw
                dict232.hex
                dict232.hexm
                dict232.text
                dict232.char

            return:
                dict485.raw
                dict485.hex
                dict485.hexm
                dict485.text
                dict485.char
                dict485.fld.f01_xxx
                dict485.fld.f01_yyy
        '''
        logger = self._setLogger(package=__name__)
        rcvdData = self.read232(timeoutValue = timeoutValue)

        # flds = self._fld
        if rcvdData:
            dict232 = self._formatter._fmtData(self, rcvdData, self._myDict)
            payloadArray = self._extractPayload(rcvdData)    # extract payload
            dict485      = self._formatter._fmtData(self, payloadArray, self._myDict) # format payload
            dict485.fld  = self._formatter._payloadFields(self, payloadArray, self._myDict) # create a dictionary with fields

        else:
                # default....
            dict232 = self._myDict()
            dict485 = self._myDict()
            dict232.raw = rcvdData
            dict485.raw = None
            dict485.fld = self._myDict()
            # dict485.rcode = dict485[self._fld.f05_RCODE]

        logger = self._setLogger(package=__name__, exiting=True)
        return dict232, dict485



    #######################################################################
    # - Scrittura dati sulla seriale
    #######################################################################
    def write485(self, payload):
        assert type(payload)==bytearray

        logger = self._setLogger(package=__name__)
        logger.info('payload: {}'.format(self._formatter._toHex(payload)[0]))

        ''' log fino al primo byte di command data '''
        from operator import itemgetter
        for k, v in sorted(self._fld.items(), key=itemgetter(1)):
            logger.info('{:<15}: {:02X}'.format(k, payload[v]))


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

        logger.info('sending data...')
        logger.info('{}'.format(self._formatter._toHex(dataToSend)[1]))

        # INVIO dati
        self.write232(dataToSend)
        logger = self._setLogger(package=__name__, exiting=True)
        return dataToSend
        # data232 = self._formatter._fmtData(self, dataToSend, self._myDict)
        # return data232




    ######################################################
    #
    ######################################################
    def _extractPayload(self, rawData):
        '''
            - unpack data
            - partendo dal rawData:
            -    1. riconosce STX ed ETX
            -    2. verifica la correttezza del pacchetto CRC
            -    3. ricostruisce i byte originali (2bytes --> 1 byte)
            -    4. estrae il payload
            -    5. ritorna payload in un bytearray
        '''
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
            logger = self._setLogger(package=__name__, exiting=True)
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
        logger = self._setLogger(package=__name__, exiting=True)
        return _payloadData[:-1] # drop CRC



    def fmtData(self, data, myDict):
        data485      = self._formatter._fmtData(self, data, myDict) # format payload
        return data485
        # data485      = self._formatter._fmtData(self, payloadArray, self._myDict) # format payload
        # data485.dict = self._formatter._payloadFields(self, payloadArray) # create a dictionary with fields


    def decodePayload485(self, data, myDict):
        payload485      = self._formatter._payloadFields(self, data, myDict) # format payload
        return payload485




