#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Master per protocollo Ln-Rs485
#         Invia il comando sul Relay collegato sulla porta seriale
#         Il Relay ritrasmette il comando sul bus Rs485
#
# updated by ...: Loreto Notarantonio
# Version ......: 10-12-2017 21.22.22
#
# ######################################################################################


import  LnLib as Ln; C = Ln.Color()


########################################################
# - SendToRelay()
########################################################
def SendToRelay(LnRs485, payload):
    assert type(payload) == bytearray
    logger  = Ln.SetLogger(package=__package__)

        # ---------------------------------------------------------------------
        # - invio del messaggio al Relay ed attesa dello stesso come echo
        # - Se non lo riceviamo vuol diche che c'è un problema
        # ---------------------------------------------------------------------
    LOOP = 10
    while LOOP:
        try:
                # - invio messaggio
            dataSent = LnRs485._rs485Write(payload, fDEBUG=False)
                # - attesa echo
            rawData = LnRs485._serialRead(timeoutValue=2000) # return bytearray
            if rawData == dataSent:
                print ('    echo has been received from Arduino Relay...')
                break
            else:
                LOOP -= 1


        except (KeyboardInterrupt) as key:
            print (__name__, "Keybord interrupt has been pressed")
            LnRs485.Close()
            Ln.Exit(0)

    if LOOP < 1:
        Ln.Exit(1, "    Il relay non risponde...")
