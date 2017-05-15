#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:        KeepAlive sul bus RS485
# modified:     by Loreto notarantonio LnVer_2017-05-15_16.24.05
#
# ######################################################################################


import sys
import time


########################################################
# keepAlive()
#   invia un messaggio per verificare che sia presente
########################################################
def EchoTest(gv, serialRelayPort):
    logger  = gv.Ln.SetLogger(package=__name__)
    C       = gv.Ln.LnColor()
    fDEBUG  = gv.input.fDEBUG


    serialRelayPort.ClosePortAfterEachCall(False)
    print(serialRelayPort.__repr__())

        # ===================================================
        # = RS-485 sendMessage
        # ===================================================
    print ('... press ctrl-c to stop the process.')

    ECHO_CMD        = bytes([1]) # comando di ECHO = x01

    sourceAddr      = bytes([0]) # MASTER

    CMD             = gv.Ln.LnDict()
    CMD.dataStr     = 'echo test'
    CMD.commandNO   = int.from_bytes(ECHO_CMD,  'little')
    CMD.destAddr    = 10                                    # Arduino 10 per  keepAlive
    CMD.sourceAddr  = int.from_bytes(sourceAddr, 'little')


    while True:
        print ()
        print ("sending echo test...")
        try:
            dataSent = serialRelayPort.sendDataCMD(CMD, fDEBUG=True)
            time.sleep(3)

        except (KeyboardInterrupt) as key:
            print (__name__, "Keybord interrupt has been pressed")
            sys.exit()


        print ()
        print ("waiting for response...")
        try:
            '''
            data = port.readRawData(EOD=[], hex=True, text=True, char=False, TIMEOUT=1000)
            if data:
                print('data has been received...')
            '''

            payLoad, rawData = serialRelayPort.readData(TIMEOUT=1000, fDEBUG=True)
            if not payLoad:
                print ('payLoad ERROR....')
            print()


        except (KeyboardInterrupt) as key:
            print (__name__, "Keybord interrupt has been pressed")
            sys.exit()

    return 0

