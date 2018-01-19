#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Master per protocollo Ln-Rs485
#         Invia il comando sul Relay collegato sulla porta seriale
#         Il Relay ritrasmette il comando sul bus Rs485
#
# updated by ...: Loreto Notarantonio
# Version ......: 19-01-2018 12.19.40
#
# ######################################################################################


import sys

import Source as Prj

########################################################
# - monitorRaw()
########################################################
def monitorRaw(LnRs485, inpArgs):
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
    while True:
        try:
                # return bytearray
            data = LnRs485._serialRead(timeoutValue=2000)
            if data:
                fmtData = LnRs485.fmtData(data, Ln.Dict)
                logger.debug('received... {}'.format(fmtData.hexm))
                if gv.args.hex:  print (fmtData.hexm)
                if gv.args.char: print (fmtData.char)
                if gv.args.text: print (fmtData.text)
                print ('\n'*2)


        except (KeyboardInterrupt) as key:
            print (__name__, "Keybord interrupt has been pressed")
            sys.exit()

