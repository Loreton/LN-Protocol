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


    fDEBUG   = gv.INPUT_PARAM.fDEBUG

        # ===================================================
        # = RS-485 port monitor
        # ===================================================
    try:
        print ('... press ctrl-c to stop the process.\n')

        while True:
            payLoad, rowData = monPort.readData(fDEBUG=True)
            if not payLoad:
                print ('payLoad ERROR....')
            print()


    except (KeyboardInterrupt) as key:
        print ("Keybord interrupt has been pressed")
        sys.exit()



