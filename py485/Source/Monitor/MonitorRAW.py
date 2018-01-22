#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Master per protocollo Ln-Rs485
#         Invia il comando sul Relay collegato sulla porta seriale
#         Il Relay ritrasmette il comando sul bus Rs485
#
# updated by ...: Loreto Notarantonio
# Version ......: 22-01-2018 16.14.51
#
# ######################################################################################


import sys

import Source as Prj

########################################################
# - monitorRaw()
########################################################
def monitorRaw(serialPort, MAX_LOOP=1000000, dHex=True, dText=False, dChar=False):
    # ----- common part into the Prj modules --------
    Ln      = Prj.LnLib
    C       = Ln.Color()
    logger  = Ln.SetLogger(package=__name__)
    gv      = Prj.gv
    # -----------------------------------------------



        # ===================================================
        # = RS-485 sendMessage
        # ===================================================
    C.printColored (color=C.yellowH, text=__name__ + '... press ctrl-c to stop the process.', tab=8)
    # gv.args.printTree(fPAUSE=True)
    while MAX_LOOP>0:
        try:
                # return bytearray
            data = serialPort._serialRead(timeoutValue=2000)
            if data:
                fmtData = serialPort.fmtData(data, Ln.Dict)
                logger.debug('received... {}'.format(fmtData.hexm))
                if dHex:  print (fmtData.hexm)
                if dChar: print (fmtData.char)
                if dText: print (fmtData.text)
                print ('\n'*2)
                MAX_LOOP = 0 # exiting

            MAX_LOOP -= 1


        except (KeyboardInterrupt) as key:
            print (__name__, "Keybord interrupt has been pressed")
            sys.exit()

    logger = Ln.SetLogger(__name__, exiting=True)
