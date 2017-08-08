#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Master per protocollo Ln-Rs485
#         provvede ad inviare tutti i comandi verso un arduino utilizzato come Relay
#         e collegato sulla porta seriale.
#         Il Relay ritrasmette il comando sulla Rs485, cattura la risposta e la
#         inoltra a questo master.
#
#
# by Loreto notarantonio LnVer_2017-07-19_10.09.54
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
    fDEBUG  = gv.inputParam.fDEBUG
    myCMD   = gv.myCMD


        # ===================================================
        # = Elaborazione del file.ini
        # = ed inizio controllo.
        # ===================================================
    print ('... press ctrl-c to stop the process.')

    CMD             = gv.Ln.LnDict()


    # gv.ini.printTree(whatPrint='KV')

    # --------------------------------------------------------------------
    # - analizziamo le section del file e identifichiamo, inizialmente,
    # - come valide solo quelle che hanno un deviceAddress
    # --------------------------------------------------------------------
    for sectionName in gv.ini.keys():
        sectID = gv.ini[sectionName]
        if 'deviceAddress' in sectID:
            dev = gv.Ln.LnDict()
            dev.address = sectID.deviceAddress
            # sectID.printTree(header=sectionName, whatPrint='KV')
            dev.pinNO, dev.pinMode = sectID.pin.split('.')
            if 'OFF' in sectID: dev.OFF = setArrayTime(sectID.OFF)
            if 'ON' in sectID:  dev.ON = setArrayTime(sectID.ON)
            dev.printTree(header=sectionName, whatPrint='KV')

            CMD.dataStr     = 'echo test'
            CMD.commandNO   = int.from_bytes(myCMD.readPin,  'little')
            CMD.sourceAddr  = int.from_bytes(gv.myCMD.masterAddr, 'little')
            CMD.relayAddr   = int.from_bytes(gv.myCMD.relayAddr, 'little')
            CMD.destAddr    = int.from_bytes(gv.myCMD.arduino11, 'little')

            # sourceAddr      = bytes([0]) # MASTER

            # CMD             = gv.Ln.LnDict()
            # CMD.commandNO   = int.from_bytes(gv.CMD.read,  'little')
            # CMD.destAddr    = 10                                    # Arduino 10 per  keepAlive
            # CMD.sourceAddr  = int.from_bytes(sourceAddr, 'little')
            # CMD.dataStr     = 'echo test'


            try:
                # CMD.dataStr     = 'Loreto.'
                # CMD.commandNO   = int.from_bytes(ECHO_CMD, 'little')
                dataSent        = serialRelayPort.sendDataCMD(CMD, fDEBUG=True)



            except (KeyboardInterrupt) as key:
                print ("Keybord interrupt has been pressed")
                sys.exit()



    '''
    # seqNO = 0
    while True:
        for destAddress in gv.inputParam.rs485Address:
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
                    # data = monPort.readRawData(EOD=gv.inputParam.eod_char, hex=gv.inputParam.fHEX, text=gv.inputParam.fLINE, char=gv.inputParam.fCHAR)
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



######################################################
# crea un array di array
######################################################
def setArrayTime(line):
    orario = []

    for ora in line.split(','):
        oraLista = ora.strip().split('.')
        if len(oraLista) == 3:
            orario.append(oraLista)

    return orario