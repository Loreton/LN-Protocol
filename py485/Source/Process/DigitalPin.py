#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Master per protocollo Ln-Rs485
#         Invia il comando sul Relay collegato sulla porta seriale
#         Il Relay ritrasmette il comando sul bus Rs485
#
# updated by ...: Loreto Notarantonio
# Version ......: 26-11-2017 16.42.37
#
# ######################################################################################


import sys
import time
import  LnLib as Ln; C = Ln.Color()
import Source as Prj

########################################################
# keepAlive()
#   invia un messaggio per verificare che sia presente
########################################################
def digitalRead(rs485Port, iniData, srcAddress, destAddr, pinNO):
    logger  = Ln.SetLogger(package=__name__)


        # ===================================================
        # = RS-485 sendMessage
        # ===================================================
    C.printColored (color=C.yellowH, text='... press ctrl-c to stop the process.', tab=8)
    iniData.printTree()

    # sourceAddr  = int.from_bytes(iniData.COMMANDS.master, 'little')
    # destAddr    = int.from_bytes(iniData.slave_address, 'little')

    commandData  = bytearray()
    commandData.append( int(iniData.COMMAND.DIGITAL, 16) )    # COMMAND
    commandData.append( int(iniData.SUB_COMMAND.READ_PIN, 16) )    # SubCOMMAND
    commandData.append( pinNO )    # PinNumber

    print (srcAddress, destAddr, commandData  )

    while True:
        print ()
        print ("sending read digital pin...")
        try:
            dataSent = rs485Port.sendDataSDD(sourceAddress=srcAddress, destAddress=destAddr, dataStr=commandData, fDEBUG=True)
            time.sleep(3)

        except (KeyboardInterrupt) as key:
            print (__name__, "Keybord interrupt has been pressed")
            sys.exit()

        sys.exit()

        print ()
        print ("waiting for response...")
        try:
            data = port.readRawData(EOD=[], hex=True, text=True, char=False, TIMEOUT=1000)
            if data:
                print('data has been received...')


            payLoad, rawData = serialRelayPort.readData(TIMEOUT=1000, fDEBUG=True)
            if not payLoad:
                print ('payLoad ERROR....')
            print()


        except (KeyboardInterrupt) as key:
            print (__name__, "Keybord interrupt has been pressed")
            sys.exit()

    return 0

