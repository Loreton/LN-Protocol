#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Polling per protocollo Ln-Rs485
#         Invia il comando di echo sul Relay collegato sulla porta seriale
#         Il Relay ritrasmette il comando sia sulla Rs485 sia sulla seriale
#         e quindi catturato da questo programma.
#         Siccome destAddr=0 nessuno dovrebbe risponere ma...
#         ...sulle seriali degli Arduino si dovrebbe leggere qualcosa tipo:
#         S[011] - inoRECV from: 10 to  : 0 [00059]   (Request is NOT for me)
#
# modified:     by Loreto notarantonio LnVer_2017-08-14_12.46.58
#
# ######################################################################################


import sys
import time


########################################################
# keepAlive()
#   invia un messaggio per verificare che sia presente
########################################################
def Polling(gv, serialRelayPort):
    logger  = gv.Ln.SetLogger(package=__name__)
    cPrint  = gv.Ln.LnColor()
    fDEBUG  = gv.inputParam.fDEBUG


        # ===================================================
        # = RS-485 sendMessage
        # ===================================================
    cPrint.YellowH ('... press ctrl-c to stop the process.')


    CMD             = gv.Ln.LnDict()
    CMD.dataStr     = 'polling test'
    CMD.command     = int.from_bytes(gv.myCMD.polling,  'little')
    CMD.subCommand   = 0x01
    CMD.sourceAddr  = int.from_bytes(gv.myDEV.master, 'little')
    CMD.xmitRcode   = 0

    while True:
        for dev, address in gv.myDEV.items():
            if dev in ('master', 'relay'): continue
            # print ('...................', dev, address)
            CMD.destAddr    = int.from_bytes(address, 'little')

            print ()
            cPrint.Yellow("sending polling test to {DEV} - Addr: 0x{ADDR:02X}".format(DEV=dev, ADDR=CMD.destAddr))

            try:
                dataSent = serialRelayPort.sendDataCMD(CMD, fDEBUG=True)

            except (KeyboardInterrupt) as key:
                print (__name__, "Keybord interrupt has been pressed")
                sys.exit()


            print ()
            cPrint.Cyan("waiting for response...")
            time.sleep(5)


            try:
                '''
                data = serialRelayPort.readRawData(EOD=[], hex=True, text=True, char=False, timeoutValue=5000)
                if data:
                    print('data has been received...')
                '''

                myData, rawData = serialRelayPort.readData(timeoutValue=1000, fDEBUG=True)
                if not myData:
                    hexData = ' '.join('{0:02X}'.format(x) for x in rawData)
                    cPrint.RedH ('ERROR....')
                    cPrint.RedH (hexData)
                print()


            except (KeyboardInterrupt) as key:
                cPrint.Yellow (__name__, "Keybord interrupt has been pressed")
                sys.exit()
        """
        """
        time.sleep(5)



