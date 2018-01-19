#!/usr/bin/env python3
#
# #####################################################

# updated by ...: Loreto Notarantonio
# Version ......: 19-01-2018 15.08.27

import sys

_printableChars = list(range(31,126))

######################################################
# - Formatter485
######################################################
class Formatter:

    ######################################################
    # -
    ######################################################
    @staticmethod
    def _toHex(data):
        assert type(data) == bytearray
        if not data: return None
        hexData = ' '.join("x'{0:02x}'".format(x) for x in data)
        hexData1 = ' '.join("{0:02x}".format(x) for x in data)
        hexMsg = '{DESCR:^10}:  <data>{DATA}</data>'.format(DESCR="hex", DATA=hexData1)
        return hexData, hexMsg




    ######################################################
    # -
    ######################################################
    @staticmethod
    def _xxfmtData___(obj485, data, myDict):
        '''
            Prende in input un bytearray di dati
            li formatta di diversi formati
            e li ritorna.
        '''
        assert type(data) == bytearray
        logger = obj485._setLogger(package=__name__)

        d      = myDict()
        d.raw  = data

        if d.raw:
            _validChars = _printableChars
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
            textMsg = '{DESCR:^10}:  <data>{DATA}</data>'.format(DESCR="text", DATA=''.join(_lineToPrint))

            d.hexd = hexData
            d.hexm = hexMsg
            d.text = textMsg
            d.char = chrMsg
            funcName = sys._getframe(1).f_code.co_name
            for key, val in d.items():
                logger.debug('{}.{:} --> {}'.format(funcName, key, val))

        return d
        # return {'TEXT': textMsg, 'CHAR': chrMsg, 'HEXD': hexData, 'HEXM': hexMsg}



    ######################################################
    # - format rs485 data
    ######################################################
    @staticmethod
    def _fmtData(obj485, data, myDict):
        '''
            Prende in input un bytearray di dati
            return:
                    d.raw
                    d.hex
                    d.hexm
                    d.text
                    d.char
        '''
        assert type(data) == bytearray
        logger = obj485._setLogger(package=__name__)

        d      = myDict()
        d.raw  = data

        if d.raw:
            _validChars = _printableChars
            _validChars.append(10)                  # aggiungiamo il newline in modo che venga displayato

                # PARTE HEX


                # PARTE TEXT or CHAR
            _lineToPrint = []
            for i in d.raw:
                if i in _validChars:                    # Handle only printable ASCII
                    _lineToPrint.append(chr(i))
                else:
                    _lineToPrint.append(" ")

            d.hex   = ' '.join('{0:02x}'.format(x) for x in d.raw)
            d.hexm  = '{DESCR:^10}:  <data>{DATA}</data>'.format(DESCR="hex", DATA=d.hex)
            d.text  = '{DESCR:^10}:  <data>{DATA}</data>'.format(DESCR="text", DATA=''.join(_lineToPrint))
            d.char  = '{DESCR:^10}:  <data> {DATA}</data>'.format(DESCR="char", DATA='  '.join(_lineToPrint))

        else:
            d.hex   = None
            d.hexm  = None
            d.text  = None
            d.char  = None

        # funcName = sys._getframe(1).f_code.co_name
        for key, val in d.items():
            logger.debug('{:<10} --> {}'.format(key, val))

        logger = obj485._setLogger(package=__name__, exiting=True)
        return d





    ######################################################
    # - unpack data
    # - partendo dal rawData:
    # -    1. riconosce STX ed ETX
    # -    2. verifica la correttezza del pacchetto CRC
    # -    3. ricostruisce i byte originali (2bytes --> 1 byte)
    # -    4. mette i dati un un dictionnary
    ######################################################
    @staticmethod
    def _payloadFields(obj485, data, dictType):
        assert type(data) == bytearray
        # logger = obj485._setLogger(package=__name__)

        myDict = dictType()
        if not data: return myDict

        fld = obj485._fld
        # fld.printTree(fPAUSE=True)

        myDict.f01_sourceAddr  = "x'{:02X}'".format(data[fld.SRC_ADDR])
        myDict.f02_destAddr    = "x'{:02X}'".format(data[fld.DEST_ADDR])
        myDict.f03_seqNo       = '{:05}'.format(data[fld.SEQNO_H]*256 + data[fld.SEQNO_L])
        myDict.f05_RCODE       = data[fld.RCODE]
        myDict.f04_CMD         = "x'{:02X}'".format(data[fld.CMD])
        myDict.f06_subCMD      = "x'{:02X}'".format(data[fld.SUB_CMD])
        # myDict.f07_commandData = data[fld.COMMAND_DATA:]
        myDict.f07_commandData = ' '.join("x'{0:02x}'".format(x) for x in data[fld.COMMAND_DATA:])
        # myDict.s07_commandData = Formatter._toHex(data[fld.COMMAND_DATA:])[0]

        return myDict


