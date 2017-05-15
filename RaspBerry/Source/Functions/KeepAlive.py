#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:        KeepAlive sul bus RS485
# modified:     by Loreto notarantonio LnVer_2017-05-15_11.54.19
#
# ######################################################################################


import sys



########################################################
# keepAlive()
#   invia un messaggio per verificare che sia presente
########################################################
def KeepAlive(gv, port, CMD):

    gECHO_CMD = bytes([1]) # comando di ECHO

    try:
        CMD.dataStr     = 'keepAlive'
        CMD.commandNO   = int.from_bytes(gECHO_CMD,  'little')
        CMD.destAddr    = 10                                    # Arduino 10 per  keepAlive
        dataSent        = port.sendDataCMD(CMD, fDEBUG=True)


    except (KeyboardInterrupt) as key:
        print (__name__, "Keybord interrupt has been pressed")
        sys.exit()


    try:
        print ("waiting for response...")
        '''
        data = port.readRawData(EOD=[], hex=True, text=True, char=False, TIMEOUT=1000)
        if data:
            print('data has been received...')
        '''

        payLoad, rawData = port.readData(TIMEOUT=1000, fDEBUG=True)
        if not payLoad:
            print ('payLoad ERROR....')
        print()


    except (KeyboardInterrupt) as key:
        print (__name__, "Keybord interrupt has been pressed")
        sys.exit()

    return 0

