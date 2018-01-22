#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Master per protocollo Ln-Rs485
#         Invia il comando sul Relay collegato sulla porta seriale
#         Il Relay ritrasmette il comando sul bus Rs485
#
# updated by ...: Loreto Notarantonio
# Version ......: 19-01-2018 16.03.40
#
# ######################################################################################


import sys

import Source as Prj

########################################################
# - monitorRS485()
########################################################
def monitorRS485(LnSerial):
    Ln      = Prj.LnLib
    C       = Ln.Color()
    logger  = Ln.SetLogger(package=__name__)
    gv = Prj.gv

        # ===================================================
        # = RS-485 sendMessage
        # ===================================================
    C.printColored (color=C.yellowH, text=__name__ + '... press ctrl-c to stop the process.', tab=8)


    while True:
        # LnSerial.cleanRxData
        try:
                # return bytearray
            dict232, dict485 = LnSerial.read485(timeoutValue=2000)
                # - ricevuto il messaggio di waiting for command da parte del Relay
            if dict485.raw and dict485.fld.f05_RCODE==6:
                logger.info(dict485.fld, dictTitle='RS485 received data')
                print ('\n'*2)
                continue

            # if data:
            # if data:
                # fmtData = LnSerial.fmtData(data, Ln.Dict)
                # if gv.args.hex:  print (fmtData.hexm)
                # if gv.args.char: print (fmtData.char)
                # if gv.args.text: print (fmtData.text)

            #     logger.debug('received... {}'.format(fmtData.hexm))
                # fullData = LnSerial.decodePayload485(data, Ln.Dict)
                # logger.info(gv.args, dictTitle='command line parameters...')
                # logger.info(fullData, dictTitle="rs485 payload")
                # payload = fullData.payload
                # raw     = fullData.raw
                # if payload.data:
                    # print (payload.data)
                    # print (payload.hexd)
                    # print (payload.hexm)
                    # print (payload.char)
                    # print (payload.text)
                    # xx = LnSerial.PayloadToDict(payload.data)
                    # xx.printTree(header='ricezione dati dallo slave: {}'.format(payload.data[LnSerial._fld.SRC_ADDR]))




        except (KeyboardInterrupt) as key:
            print (__name__, "Keybord interrupt has been pressed")
            sys.exit()

    logger = Ln.SetLogger(__name__, exiting=True)


