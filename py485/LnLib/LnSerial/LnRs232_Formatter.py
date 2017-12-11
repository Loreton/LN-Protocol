#!/usr/bin/env python3
#
# #####################################################

# updated by ...: Loreto Notarantonio
# Version ......: 11-12-2017 16.35.38


######################################################
# - Formatter485
######################################################
class Formatter232:

    ######################################################
    # -
    ######################################################
    @staticmethod
    def _fmtData(obj232, data):
        '''
            Prende in input un bytearray di dati
            li formatta di diversi formati
            e li ritorna.
        '''
        assert type(data) == bytearray
        logger = obj232._setLogger(package=__package__)


        _validChars = obj232._printableChars
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


