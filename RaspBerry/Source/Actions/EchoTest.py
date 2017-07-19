#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Master per protocollo Ln-Rs485
#         Invia il comando di echo sul Relay collegato sulla porta seriale
#         Il Relay ritrasmette il comando sia sulla Rs485 sia sulla seriale
#         e quindi catturato da questo programma.
#         Siccome destAddr=0 nessuno dovrebbe risponere ma...
#         ...sulle seriali degli Arduino si dovrebbe leggere qualcosa tipo:
#         S[011] - inoRECV from: 10 to  : 0 [00059]   (Request is NOT for me)
#
# modified:     by Loreto notarantonio LnVer_2017-07-19_10.08.13
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
    cPrint  = gv.Ln.LnColor()
    fDEBUG  = gv.inputParam.fDEBUG
    myCMD   = gv.myCMD


        # ===================================================
        # = RS-485 sendMessage
        # ===================================================
    cPrint.YellowH ('... press ctrl-c to stop the process.')


    CMD             = gv.Ln.LnDict()
    CMD.dataStr     = 'echo test'
    CMD.commandNO   = int.from_bytes(myCMD.echo,  'little')
    CMD.sourceAddr  = int.from_bytes(gv.myCMD.masterAddr, 'little')
    CMD.destAddr    = int.from_bytes(gv.myCMD.relayAddr, 'little')


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

