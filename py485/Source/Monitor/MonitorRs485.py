#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Master per protocollo Ln-Rs485
#         Invia il comando sul Relay collegato sulla porta seriale
#         Il Relay ritrasmette il comando sul bus Rs485
#
# updated by ...: Loreto Notarantonio
# Version ......: 26-11-2017 18.17.43
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
def monitorRS485(rs485Port):
    logger  = Ln.SetLogger(package=__name__)


        # ===================================================
        # = RS-485 sendMessage
        # ===================================================
    C.printColored (color=C.yellowH, text=__name__ + '... press ctrl-c to stop the process.', tab=8)



    while True:
        try:
            payLoad, rawData = rs485Port.readData(fDEBUG=True)

        except (KeyboardInterrupt) as key:
            print (__name__, "Keybord interrupt has been pressed")
            sys.exit()

def monitorRaw(rs485Port):
    logger  = Ln.SetLogger(package=__name__)


        # ===================================================
        # = RS-485 sendMessage
        # ===================================================
    C.printColored (color=C.yellowH, text='... press ctrl-c to stop the process.', tab=8)



    while True:
        try:
            data = rs485Port.readRawData(EOD=[], hex=True, text=False, char=False)
            if data: print()
            print()

        except (KeyboardInterrupt) as key:
            print (__name__, "Keybord interrupt has been pressed")
            sys.exit()

