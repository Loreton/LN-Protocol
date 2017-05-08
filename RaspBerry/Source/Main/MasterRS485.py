#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per ...........
# modified:  by Loreto notarantonio 2017-03-28 09.59.40
#
# ######################################################################################


import sys
import time

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

    sourceAddr = bytes([0]) # MASTER
    sourceAddr = int.from_bytes(sourceAddr, 'little')
    basedata   = 'Loreto.'

    seqNO = 0
    while True:
        for destAddress in gv.input.rs485Address:
            destAddr   = bytes([destAddress])
            destAddr   = int.from_bytes(destAddr, 'little')

            try:
                seqNO += 1
                print(seqNO)
                dataStr  = '{DATA}.{INX:04}'.format(DATA=basedata, INX=seqNO)
                dataSent = serialRelayPort.writeDataSDD(sourceAddr, destAddr, basedata, fDEBUG=True)
                # time.sleep(10)


            except (KeyboardInterrupt) as key:
                print ("Keybord interrupt has been pressed")
                sys.exit()


                # read response
            try:
                while True:
                    data = serialRelayPort.readRawData(EOD=None, hex=True, text=True, char=True)
                    if data:
                        # print(data)
                        print()
                    else:
                        print ('...nothing')
                    '''
                    payLoad, rowData = monPort.readData(fDEBUG=True)
                    if not payLoad:
                        print ('payLoad ERROR....')
                    print()
                    '''


            except (KeyboardInterrupt) as key:
                print ("Keybord interrupt has been pressed")
                sys.exit()
