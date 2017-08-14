#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per ...........
# modified:  by Loreto notarantonio 2017-03-28 09.59.40
#
# ######################################################################################


import os, sys


################################################################################
# -
################################################################################
def MonitorRaw(gv, monPort):
    logger  = gv.Ln.SetLogger(package=__name__)
    C       = gv.Ln.LnColor()


    fDEBUG   = gv.inputParam.fDEBUG
    print ('... press ctrl-c to stop the process.\n')
    monPort.ClosePortAfterEachCall(False) # ho notato che altrimenti perdo qualche byte
    print(monPort.__repr__())


    # ===================================================
    # = R A W
    # ===================================================

    print ('... RAW format... until char:', gv.inputParam.eod_char)
    EOD = int('0x0A', 16) # integer
    EOD = int('0x03', 16) # integer
    if not gv.inputParam.eod_char: EOD = []
    try:
        while True:
            data = monPort.readRawData(EOD=EOD, hex=gv.inputParam.fHEX, text=gv.inputParam.fLINE, char=gv.inputParam.fCHAR)
            if data: print()

    except (KeyboardInterrupt) as key:
        print ("Keybord interrupt has been pressed")
        sys.exit()




################################################################################
# -
################################################################################
def MonitorRS485(gv, monPort):
    logger  = gv.Ln.SetLogger(package=__name__)
    C       = gv.Ln.LnColor()


    fDEBUG   = gv.inputParam.fDEBUG
    print ('... press ctrl-c to stop the process.\n')

        # ===================================================
        # = RS-485 port monitor
        # ===================================================
    print ('... RS485 format...')
    try:

        while True:
            payLoad, rawData = monPort.readData(timeoutValue=30000, fDEBUG=True)
            if not payLoad:
                COMMAND_DATA      = 7    # TX - dati necessari al comando per la sua corretta esecuzione/RX - dati di risposta
                # print ('payLoad ERROR....')
                print ('    full data - len: [{0:03}] - '.format(len(rawData)), end="")
                for byte in rawData: print ('{0:02X} '.format(byte), end="")
                print ()
                print ()
                commandData = rawData[COMMAND_DATA*2:]
                print ('    raw data - len: [{0:03}] - '.format(len(commandData)), end="")
                print ('   '*COMMAND_DATA, end="")
                print ('[', end="")
                printableChars = list(range(31,126))
                printableChars.append(13)
                printableChars.append(10)
                for byte in rawData:
                    if byte in printableChars:   # Handle only printable ASCII
                        print(chr(byte), end="")
                    else:
                        print(' ', end="")


            print()


    except (KeyboardInterrupt) as key:
        print ("Keybord interrupt has been pressed")
        sys.exit()

