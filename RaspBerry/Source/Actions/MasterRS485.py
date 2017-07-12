#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per ...........
# modified:  by Loreto notarantonio LnVer_2017-05-19_16.49.45
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
    fDEBUG  = gv.input.fDEBUG


        # ===================================================
        # = Elaborazione del file.ini
        # = ed inizio controllo.
        # ===================================================
    print ('... press ctrl-c to stop the process.')

    CMD = gv.Ln.LnDict()


    sourceAddr     = bytes([0]) # MASTER

    CMD.sourceAddr = int.from_bytes(sourceAddr, 'little')
    gv.ini.printTree(displayField='KV')

    # --------------------------------------------------------------------
    # - analizziamo le section del file e identifichiamo, inizialmente,
    # - come valide solo quelle che hanno un deviceAddress
    # --------------------------------------------------------------------
    for sectionName in gv.ini.keys():
        sectID = gv.ini[sectionName]
        if 'deviceAddress' in sectID:
            print (sectionName)
            for key, val in sectID.items():
                print ('    ', key)
            print()

    '''
    # seqNO = 0
    while True:
        for destAddress in gv.input.rs485Address:
            CMD.destAddr    = destAddress; # print (type(CMD.destAddr), CMD.destAddr )


            gv.Prj.KeepAlive(gv, serialRelayPort, CMD)
            time.sleep(3)
            # gv.Ln.getKeyboardInput('press ENTER to continue...', validKeys='ENTER', exitKey='X', deepLevel=1, keySep="|", fDEBUG=False)
            continue


            try:
                CMD.dataStr     = 'Loreto.'
                CMD.commandNO   = int.from_bytes(ECHO_CMD, 'little')
                dataSent        = serialRelayPort.sendDataCMD(CMD, fDEBUG=True)



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




                    # payLoad, rawData = serialRelayPort.readData(fDEBUG=True)
                    # if not payLoad:
                    #     print ('payLoad ERROR....')
                    # print()


            except (KeyboardInterrupt) as key:
                print ("Keybord interrupt has been pressed")
                sys.exit()
    '''
