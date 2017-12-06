#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Master per protocollo Ln-Rs485
#         Invia il comando sul Relay collegato sulla porta seriale
#         Il Relay ritrasmette il comando sul bus Rs485
#
# updated by ...: Loreto Notarantonio
# Version ......: 06-12-2017 15.14.30
#
# ######################################################################################


import sys
import time
import  LnLib as Ln; C = Ln.Color()
import Source as Prj

########################################################
# - monitorRS485()
########################################################
def monitorRS485(LnRs485):
    logger  = Ln.SetLogger(package=__name__)


        # ===================================================
        # = RS-485 sendMessage
        # ===================================================
    C.printColored (color=C.yellowH, text=__name__ + '... press ctrl-c to stop the process.', tab=8)



    while True:
        LnRs485.cleanRxData
        try:
                # return bytearray
            LnRs485._serialRead(timeoutValue=2000)
            if LnRs485.rawData:
                # print (LnRs485.rawData)
                # print (LnRs485.rawHex)
                # print (LnRs485.rawChr)
                # print(LnRs485.payload)
                # print(LnRs485.payloadHex)
                # print (xx)
                xx = LnRs485.payloadToDict
                xx.printTree()
                print ('\n'*2)




        except (KeyboardInterrupt) as key:
            print (__name__, "Keybord interrupt has been pressed")
            sys.exit()



########################################################
# - monitorRaw()
########################################################
def monitorRaw(LnRs485, inpArgs):
    logger  = Ln.SetLogger(package=__name__)


        # ===================================================
        # = RS-485 sendMessage
        # ===================================================
    C.printColored (color=C.yellowH, text=__name__ + '... press ctrl-c to stop the process.', tab=8)
    # from string import Template
    while True:
        LnRs485.cleanRxData
        try:
            LnRs485._serialRead(timeoutValue=2000)
            if LnRs485.rawData:
                # print (LnRs485.rawData)
                print (LnRs485.rawText)
                # print (LnRs485.rawHex)
                # print (LnRs485.rawChr)
                # print(LnRs485.payload)
                # print(LnRs485.payloadHex)
                # print (xx)
                # xx = LnRs485.payloadToDict
                # xx.printTree()
                print ('\n'*2)




        except (KeyboardInterrupt) as key:
            print (__name__, "Keybord interrupt has been pressed")
            sys.exit()

