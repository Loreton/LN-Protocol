#!/usr/bin/env python3
#
# modified by Loreto:           2017-03-10_14.50.01
# #####################################################

# updated by ...: Loreto Notarantonio
# Version ......: 23-01-2018 08.37.53

import serial       # sudo pip3.4 install pyserial
import sys
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

read_TIMEOUT  = 0.05
"""Default value for the timeout value in seconds (float)."""



#####################################################################
# - MAIN LnRS485 CLASS
#####################################################################
class LnRs232():
    def __init__(self, port, mode='ascii', baudrate=9600, useLogger=None, myDict=LnClass):

        if useLogger:
            self._setLogger = useLogger
        else:
            self._setLogger = self._internaLogger

        logger = self._setLogger(package=__name__)
        self._myDict = myDict


        if port not in _SERIALPORTS or not _SERIALPORTS[port]:
            try:
                logger.info('opening port...')
                self._serial = _SERIALPORTS[port] = serial.Serial(
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
                logger.error(str(why))
                print ('ERROR:  ', str(why))
                sys.exit()

        else:
            self._serial = _SERIALPORTS[port]
            if self._serial.port is None:
                logger.info('opening already known port...')
                self._serial.open()

                # - chissà se sono importanti....
                self._serial.reset_input_buffer()        # clear input  buffer
                self._serial.reset_output_buffer()       # clear output buffer



        self._mode = mode
        """Slave mode (str), can be MODE_RTU or MODE_ASCII.  Most often set by the constructor (see the class documentation).
        New in version 0.6.
        """

        self._close_port_after_each_call = False
        """If this is :const:'True', the serial port will be closed after each call. """
        if  self._close_port_after_each_call: self._serial.close()

        self._TxDataRaw         =  bytearray()   # raw data in uscita   dalla seriale
        self._TxDataHex         =  ''            # raw data in uscita   dalla seriale
        logger = self._setLogger(package=__name__, exiting=True)



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
            serial-id                  = {SERIAL},>
                """.format(
                        MOD=self.__module__,
                        CLASS=self.__class__.__name__,
                        ID=id(self),
                        MODE=self.mode,
                        CPAEC=self._close_port_after_each_call,
                        SERIAL=self._serial,
            )
                        # ADDRESS=self.address,




    #######################################################################
    # - Lettura dati dalla seriale
    # - Ritorna: una bytearray di integer con i dati ricevuti oppure vuoto
    #######################################################################
    def read232(self, timeoutValue=1000):
        logger = self._setLogger(package=__name__)

        if self._close_port_after_each_call:
            logger.info('opening port...')
            self._serial.open()


        # facciamo partire il timer
        timeStart = time.time()*1000
        # timeEnd   = timeStart+timeoutValue
        # TIMEOUT = True      # flag per indicare se siamo andati in timeout o meno
        logger.info( "starting timer... for {} mSec".format(timeoutValue))


        # loop fino a che non abbiamo ricevuto qualche dato
        _dataBuffer = bytearray()
        while True:
            elapsed = int((time.time()*1000)-timeStart)

                # - read serial
            ch = self._serial.read(1)       # ch e' un type->bytes

            if ch == b'':       # if buffer empty...
                if _dataBuffer: # ... and something was received ...
                    break       # ... exit
                elif elapsed >= timeoutValue:
                    logger.info( "elapsed {0}/{1}".format(elapsed, timeoutValue))
                    break
                else:
                    continue    # nothing has been received ... continue

            chInt = int.from_bytes(ch, 'little')
            _dataBuffer.append(chInt)
            # logger.debug("Received byte: x'{0:02x}'".format(chInt))


        if self._close_port_after_each_call:
            logger.info('closing port...')
            self._serial.close()

        # logger.info( "received {} bytes".format(len(_dataBuffer)))

            # RECEIVED data
        _HexData = ' '.join('{0:02x}'.format(x) for x in _dataBuffer)
        _HexMsg = '     {DESCR:^10}:  <data>{DATA}</data>'.format(DESCR="hex", DATA=_HexData)
        logger.info('received data on serial port: ')
        logger.info(_HexMsg)
        logger = self._setLogger(package=__name__, exiting=True)
        return _dataBuffer







    #######################################################################
    # - Scrittura dati sulla seriale
    #######################################################################
    def write232(self, txData):
        logger = self._setLogger(package=__name__)
        assert type(txData)==bytearray


        if self._close_port_after_each_call:
            logger.info('opening port...')
            self._serial.open()

            # INVIO dati
        _HexData = ' '.join('{0:02x}'.format(x) for x in txData)
        _HexMsg = '{DESCR:^10}:  <data>{DATA}</data>'.format(DESCR="hex", DATA=_HexData)
        logger.info('xmitting data on serial port: ')
        logger.info(_HexMsg)
        self._serial.write(txData)

        if self._close_port_after_each_call:
            logger.info('closing port...')
            self._serial.close()

        logger = self._setLogger(package=__name__, exiting=True)


    _serialRead  = read232
    _serialWrite = write232