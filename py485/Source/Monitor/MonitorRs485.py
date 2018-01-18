#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Master per protocollo Ln-Rs485
#         Invia il comando sul Relay collegato sulla porta seriale
#         Il Relay ritrasmette il comando sul bus Rs485
#
# updated by ...: Loreto Notarantonio
# Version ......: 18-01-2018 15.54.24
#
# ######################################################################################


import sys

import Source as Prj

########################################################
# - monitorRS485()
########################################################
def monitorRS485(LnRs485):
    # ----- common part into the Prj modules --------
    Ln      = Prj.LnLib
    # gv      = Prj.gv
    C       = Ln.Color()
    # logger  = Ln.SetLogger(package=__name__)
    # -----------------------------------------------



        # ===================================================
        # = RS-485 sendMessage
        # ===================================================
    C.printColored (color=C.yellowH, text=__name__ + '... press ctrl-c to stop the process.', tab=8)


    while True:
        # LnRs485.cleanRxData
        try:
                # return bytearray
            rawData = LnRs485._serialRead(timeoutValue=2000)
            if rawData:
                fullData = LnRs485.VerifyRs485Data(rawData)
                payload = fullData.payload
                raw     = fullData.raw
                if payload.data:
                    # print (payload.data)
                    # print (payload.hexd)
                    # print (payload.hexm)
                    # print (payload.char)
                    # print (payload.text)
                    xx = LnRs485.PayloadToDict(payload.data)
                    xx.printTree(header='ricezione dati dallo slave: {}'.format(payload.data[LnRs485._fld.SRC_ADDR]))
                    print ('\n'*2)




        except (KeyboardInterrupt) as key:
            print (__name__, "Keybord interrupt has been pressed")
            sys.exit()



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

