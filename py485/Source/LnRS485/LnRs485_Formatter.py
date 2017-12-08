#!/usr/bin/env python3
#
#  by Loreto:  04-12-2017 15.28.54
# #####################################################

# updated by ...: Loreto Notarantonio
# Version ......: 07-12-2017 13.37.38



class LnClass():
    def __init__(self):
        self.rCode  = 0
        self.errMsg = None


######################################################
# - Formatter485
######################################################
class Formatter485:

    ######################################################
    # -
    ######################################################
    @staticmethod
    def _toHex(data):
        assert type(data) == bytearray
        if not data: return None
        hexData = ' '.join('{0:02x}'.format(x) for x in data)
        hexMsg = '{DESCR:^10}:  <data>{DATA}</data>'.format(DESCR="hex", DATA=hexData)
        return hexData, hexMsg

    ######################################################
    # -
    ######################################################
    @staticmethod
    def _toHex2(obj485, payload=False):
        logger = obj485._setLogger(package=__package__)

        data = obj485._rs485RxPayLoad if payload else obj485._rs485RxRawData
        assert type(data) == bytearray
        if not data: return None


        hexData = ' '.join('{0:02x}'.format(x) for x in data)
        hexMsg = '{DESCR:^10}:  <data>{DATA}</data>'.format(DESCR="hex", DATA=hexData)
        return hexData, hexMsg


    ######################################################
    # -
    ######################################################
    @staticmethod
    def _fmtData(obj485, data):
        '''
            Prende in input un bytearray di dati
            li formatta di diversi formati
            e li ritorna.
        '''
        assert type(data) == bytearray
        logger = obj485._setLogger(package=__package__)


        _validChars = obj485._printableChars
        _validChars.append(10)                  # aggiungiamo il newline in modo che venga displayato

        if isinstance(data, bytes):
            data = data.decode('utf-8')

            # PARTE HEX
        hexData = ' '.join('{0:02x}'.format(x) for x in data)
        hexMsg = '{DESCR:^10}:  <data>{DATA}</data>'.format(DESCR="hex", DATA=hexData)


            # PARTE TEXT or CHAR
        _lineToPrint = []
        for i in data:
            if i in _validChars:                    # Handle only printable ASCII
                _lineToPrint.append(chr(i))
            else:
                _lineToPrint.append(" ")


        chrMsg  = '{DESCR:^10}:  <data> {DATA}</data>'.format(DESCR="char", DATA='  '.join(_lineToPrint))
        logger.debug(chrMsg)
        textMsg = '{DESCR:^10}:  <data>{DATA}</data>'.format(DESCR="text", DATA=''.join(_lineToPrint))
        logger.debug(textMsg)


        return {'TEXT': textMsg, 'CHAR': chrMsg, 'HEXD': hexData, 'HEXM': hexMsg}




    ######################################################
    # - unpack data
    # - partendo dal rawData:
    # -    1. riconosce STX ed ETX
    # -    2. verifica la correttezza del pacchetto CRC
    # -    3. ricostruisce i byte originali (2bytes --> 1 byte)
    # -    4. mette i dati un un dictionnary
    ######################################################
    @staticmethod
    def _verifyData(obj485):
        logger = obj485._setLogger(package=__package__)

        if not obj485._rs485RxRawData: return bytearray()

        rawData  = obj485._rs485RxRawData

            # cerchiamo STX
        for index, byte in enumerate(rawData):
            if byte == obj485._STX:
                rawData = rawData[index:]
                break

            # cerchiamo ETX
        for index, byte in enumerate(rawData):
            if byte == obj485._ETX:
                rawData = rawData[:index+1]
                break


        if not rawData or not rawData[0] == obj485._STX or not rawData[-1] == obj485._ETX:
            errMsg = 'STX or ETX missed'
            logger.error(errMsg)
            logger.error(obj485._rs485RxRawData)
            return bytearray()


            # ---------------------------------------------
            # - ricostruzione dei bytes originari
            # - byte = byte1_HighNibble*16 + byte2_HighNibble
            # il trick che segue ci permette di prelevare due bytes alla volta
            # ---------------------------------------------
        _packetData = bytearray()
        xy = iter(rawData[1:-1]) # skip STX and ETX
        for byte1, byte2 in zip(xy, xy):
                # re-build real byte
            if byte1 in obj485._validBytes and byte2 in obj485._validBytes:
                byte1_HighNibble = (byte1 >> 4) & 0x0F
                byte2_HighNibble = (byte2 >> 4) & 0x0F
                realByte = byte1_HighNibble*16 + byte2_HighNibble
                _packetData.append(realByte)

            else:
                errMsg = 'some byte corrupted byte1:{0:02x} byte2:{1:02x}'.format(byte1, byte2)
                logger.error(errMsg)
                return bytearray()




            # -----------------------------------------------------------------------
            # - Una volta ricostruiti i bytes origilali,
            # - calcoliamo il CRC sui dati (ovviamento escluso il byte di CRC stesso)
            # -----------------------------------------------------------------------
        _CRC_calculated  = obj485._getCRC8(_packetData[:-1]) # skipping ETX
        _CRC_received    = _packetData[-1]

        logger.debug("    CRC received  : x{0:02X}".format(_CRC_received))
        logger.debug("    CRC calculated: x{0:02X}".format(_CRC_calculated))

            # ---------------------------------
            # - check CRC (drop STX and ETX)
            # ---------------------------------
        if not _CRC_calculated == _CRC_received:
            errMsg = 'Il valore di CRC non coincide'
            logger.error ()
            logger.error ("    CRC received  : x{0:02X}".format(CRC_received))
            logger.error ("    CRC calculated: x{0:02X}".format(CRC_calculated))
            logger.error ()
            return bytearray()

        obj485._rs485RxPayLoad = _packetData[:-1] # drop CRC





    ######################################################
    # - unpack data
    # - partendo dal rawData:
    # -    1. riconosce STX ed ETX
    # -    2. verifica la correttezza del pacchetto CRC
    # -    3. ricostruisce i byte originali (2bytes --> 1 byte)
    # -    4. mette i dati un un dictionnary
    ######################################################
    @staticmethod
    def _payloadToDict(obj485, data):
        assert type(data) == bytearray
        logger = obj485._setLogger(package=__package__)

        myDict = obj485._myDict()
        if not data: return myDict

        fld = obj485._fld
        # fld.printTree(fPAUSE=True)

        myDict.s01_sourceAddr  = "x'{:02X}'".format(data[fld.SRC_ADDR])
        myDict.s02_destAddr    = "x'{:02X}'".format(data[fld.DEST_ADDR])
        myDict.s03_seqNo       = '{:05}'.format(data[fld.SEQNO_H]*256 + data[fld.SEQNO_L])
        myDict.s05_RCODE       = data[fld.RCODE]
        myDict.s04_CMD         = "x'{:02X}'".format(data[fld.CMD])
        myDict.s06_subCMD      = "x'{:02X}'".format(data[fld.SUB_CMD])
        myDict.s07_commandData = data[fld.COMMAND_DATA:]

        return myDict


