#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per ...........
# modified:  by Loreto notarantonio 2017-03-28 09.59.40
#
# ######################################################################################


import sys


################################################################################
# -
################################################################################
def MonitorRS485(gv, monPort):
    logger  = gv.Ln.SetLogger(package=__name__)
    C       = gv.Ln.LnColor()


    fDEBUG   = gv.input.fDEBUG
    print ('... press ctrl-c to stop the process.\n')

        # ===================================================
        # = RS-485 port monitor
        # ===================================================
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

