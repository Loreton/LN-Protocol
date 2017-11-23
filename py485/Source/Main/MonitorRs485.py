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
# modified:     by Loreto notarantonio LnVer_2017-08-15_09.56.13
#
# ######################################################################################


import sys
import time
import LnLib as Ln
import Source as Prj


########################################################
# keepAlive()
#   invia un messaggio per verificare che sia presente
########################################################
def monitorRS485(gv, serialRelayPort):
    logger  = Ln.SetLogger(package=__name__)
    cPrint  = Ln.LnColor()


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

    # JUST_MONITOR = True
    # if JUST_MONITOR:
    #     while True:
    #         rcvdData, rawData = serialRelayPort.readData(timeoutValue=30000, fDEBUG=True)
    #         if not rcvdData:
    #             gv.Prj.displayRawData(rawData)

    #     print()
    # sys.exit()



    timeOutValue = 30000
    LOOP_ON_DEV = True
    while True:
            '''
        for dev, address in gv.myDEV.items():
            if dev in ('master', 'relay'): continue
            CMD.destAddr    = int.from_bytes(address, 'little')
            '''

            validAddresses = [11,12,13,14,15]
            # address = 0
            dev = "Slave"
            address = gv.Ln.getKeyboardInput("Please Enter address...", validKeys='11,12,13,14,15', exitKey='X', deepLevel=1, keySep=",", fDEBUG=False)
            # while not address in validAddresses:
            #     address = input("\n\n\n\nPlease Enter address...{}".format(validAddresses))
            # address = int(address)
            # print (address)

            # print ('...................', dev, address)
            CMD.destAddr    = int(address)

            print ()
            cPrint.Yellow("sending polling test to {DEV} - Addr: 0x{ADDR:02X}".format(DEV=dev, ADDR=CMD.destAddr))

            try:
                dataSent = serialRelayPort.sendDataCMD(CMD, fDEBUG=True)

            except (KeyboardInterrupt) as key:
                print (__name__, "Keybord interrupt has been pressed")
                sys.exit()


            print ()

            # time.sleep(5)


            cPrint.Cyan("waiting for response...")
            try:
                rcvdData, rawData = serialRelayPort.readData(timeoutValue=timeOutValue, fDEBUG=True)
                if not rcvdData:
                    gv.Prj.displayRawData(rawData)


            except (KeyboardInterrupt) as key:
                cPrint.Yellow (__name__, "Keybord interrupt has been pressed")
                sys.exit()

            # time.sleep(5)


            # gv.Ln.getKeyboardInput("Press Enter to continue...", validKeys='ENTER', exitKey='X', deepLevel=1, keySep="|", fDEBUG=False)
            # choice = input("\n\n\n\nPress Enter to continue...")





