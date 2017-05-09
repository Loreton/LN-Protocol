#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per ...........
# modified:  by Loreto notarantonio 2017-03-28 09.59.40
#
# ######################################################################################


import sys
import time
class LnClass(): pass

################################################################################
# - serialRelayPort: porta seriale dove si trova un Arduino che rilancia
# -                  il comando su un bus RS485
################################################################################
def MasterRS485(gv, serialRelayPort):
    logger  = gv.Ln.SetLogger(package=__name__)
    C       = gv.Ln.LnColor()
    fDEBUG   = gv.input.fDEBUG


    serialRelayPort.ClosePortAfterEachCall(False)
    print(serialRelayPort.__repr__())

        # ===================================================
        # = RS-485 sendMessage
        # ===================================================
    print ('... press ctrl-c to stop the process.')
    CMD = LnClass()

    sourceAddr  = bytes([0]) # MASTER
    ECHO_CMD    = bytes([1]) # comando di ECHO

    '''
    EOD = None
    try:
        while True:
            data = serialRelayPort.readRawData(EOD=None, hex=False, text=True, char=False)
            if data: print()

    except (KeyboardInterrupt) as key:
        print ("Keybord interrupt has been pressed")
        sys.exit()
    '''




    # seqNO = 0
    while True:
        for destAddress in gv.input.rs485Address:
            destAddr        = bytes([destAddress])
            try:
                CMD.dataStr        = 'Loreto.'
                CMD.sourceAddr  = int.from_bytes(sourceAddr, 'little')
                CMD.destAddr    = int.from_bytes(destAddr, 'little')
                CMD.commandNO   = int.from_bytes(ECHO_CMD, 'little')
                dataSent        = serialRelayPort.writeDataCMD(CMD, fDEBUG=True)



            except (KeyboardInterrupt) as key:
                print ("Keybord interrupt has been pressed")
                sys.exit()




            # print ('\n'*3 ,'waiting for response....')
                # read response
            try:
                timeOut = 100
                while timeOut>0:
                    # data = monPort.readRawData(EOD=gv.input.eod_char, hex=gv.input.fHEX, text=gv.input.fLINE, char=gv.input.fCHAR)
                    # if data: print()

                    data = serialRelayPort.readRawData(EOD=None, hex=True, text=True, char=False)
                    if data:
                        print()
                    else:
                        timeOut -= 1


                    '''

                    payLoad, rowData = serialRelayPort.readData(fDEBUG=True)
                    if not payLoad:
                        print ('payLoad ERROR....')
                    print()
                    '''


            except (KeyboardInterrupt) as key:
                print ("Keybord interrupt has been pressed")
                sys.exit()
