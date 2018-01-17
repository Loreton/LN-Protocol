#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Master per protocollo Ln-Rs485
#         Invia il comando sul Relay collegato sulla porta seriale
#         Il Relay ritrasmette il comando sul bus Rs485
#
# updated by ...: Loreto Notarantonio
# Version ......: 09-01-2018 12.09.54
#
# ######################################################################################


import    Source as Prj


########################################################
# - SendToRelay()
########################################################
def SendToRelay(LnRs485, payload):
    assert type(payload) == bytearray
    # ----- common part into the Prj modules --------
    # import    Source as Prj
    # global Ln
    Ln     = Prj.LnLib
    # C      = Ln.Color()
    # logger  = Ln.SetLogger(package=__package__)
    # -----



        # ---------------------------------------------------------------------
        # - invio del messaggio al Relay ed attesa dello stesso come echo
        # - Se non lo riceviamo vuol diche che c'è un problema
        # ---------------------------------------------------------------------
    LOOP = 10
    while LOOP:
        try:
                # - invio messaggio (torna il dict dei dati nella seriale232)
            txData = LnRs485.write485(payload)

                # - attesa echo
            data = LnRs485.read232(timeoutValue=2000) # return dict.raw dict.hexd dict.hexm dict.text dict.char
            if data.raw == txData.raw:
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
