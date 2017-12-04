#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Master per protocollo Ln-Rs485
#         Invia il comando sul Relay collegato sulla porta seriale
#         Il Relay ritrasmette il comando sul bus Rs485
#
# updated by ...: Loreto Notarantonio
# Version ......: 04-12-2017 17.19.12
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
        try:
                # return bytearray
            LnRs485._serialRead(timeoutValue=2000)
            if LnRs485.rawData:
                # print (LnRs485.rawData)
                # print (LnRs485.rawHex)
                # print (LnRs485.rawChr)
                # xx = LnRs485.payload
                # print (xx)
                xx = LnRs485.toDict
                xx.printTree()




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
        try:
            data = LnRs485.readRawData(timeoutValue=500)
            if data:
                dataDict = Ln.Dict(data)
                if inpArgs.text: print(data['text_data'])
                if inpArgs.char: print(data['char_data'])
                if inpArgs.hex:  print(data['hex_data'])
                    # template = Template(data['TEXT'])
                    # out = template.substitute(startData=C.yellowH, endData=C.RESET)
                    # print(out)


        except (KeyboardInterrupt) as key:
            print (__name__, "Keybord interrupt has been pressed")
            sys.exit()

