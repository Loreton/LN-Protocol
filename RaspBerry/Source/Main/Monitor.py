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
def Monitor(gv, monPort):
    logger  = gv.Ln.SetLogger(package=__name__)
    C       = gv.Ln.LnColor()


    fDEBUG   = gv.input.fDEBUG
    print ('... press ctrl-c to stop the process.\n')

        # ===================================================
        # = RS-485 port monitor
        # ===================================================
    if gv.input.fRS485:
        print ('... RS485 format...')
        try:

            while True:
                payLoad, rowData = monPort.readData(fDEBUG=True)
                if not payLoad:
                    print ('payLoad ERROR....')
                print()


        except (KeyboardInterrupt) as key:
            print ("Keybord interrupt has been pressed")
            sys.exit()




        # ===================================================
        # = R A W
        # ===================================================
    elif gv.input.fRAW:
        print ('... RAW format... until char:', gv.input.eod_char)
        EOD = int('0x0A', 16) # integer
        EOD = int('0x03', 16) # integer
        EOD = None
        monPort.ClosePortAfterEachCall(False) # ho notato che altrimenti perdo qualche byte
        try:
            while True:
                data = monPort.readRawData(EOD=gv.input.eod_char, hex=gv.input.fHEX, text=gv.input.fLINE, char=gv.input.fCHAR)
                if data: print()

        except (KeyboardInterrupt) as key:
            print ("Keybord interrupt has been pressed")
            sys.exit()


