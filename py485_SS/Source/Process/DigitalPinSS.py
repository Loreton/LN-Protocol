#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Master per protocollo Ln-Rs485
#         Invia il comando sul Relay collegato sulla porta seriale
#         Il Relay ritrasmette il comando sul bus Rs485
#
# updated by ...: Loreto Notarantonio
# Version ......: 11-12-2017 09.06.43
#
# ######################################################################################


import  sys
import  time
import  LnLib as Ln; C = Ln.Color()
import  Source as Prj




########################################################
# - digitalToggle()
########################################################
def digitalToggle(gv, LnRs485, payload):
    assert type(payload) == bytearray
    logger  = Ln.SetLogger(package=__package__)

        # puntamento ai fieldNames
    _fld     = gv.rs485Prot.payloadFieldName

    _mainCmd = gv.mainCmd
    _subCmd = gv.subCmd


    C.printColored (color=C.yellowH, text='... press ctrl-c to stop the process.', tab=8)


        # ===================================================
        # = RS-485 preparazione del comando
        # ===================================================
    payload[_fld.SEQNO_H], payload[_fld.SEQNO_L] = LnRs485.getSeqCounter()
    payload[_fld.RCODE]                          = 0 # 0 per la TX

    payload[_fld.DEST_ADDR]                      = 11
    payload[_fld.CMD]                            = _mainCmd.DIGITAL_CMD     # COMMAND
    payload[_fld.SUB_CMD]                        = _subCmd.TOGGLE_PIN     # SubCOMMAND
    payload[_fld.PIN_NO]                         = 13     # pinNO



        # ---------------------------------------------------------------------
        # - invio del messaggio al Relay ed attesa dello stesso come echo
        # - Se non lo riceviamo vuol diche che c'è un problema
        # ---------------------------------------------------------------------
    Prj.SendToRelay(LnRs485, payload)

        # ---------------------------------------------------------------------
        # - Attesa risposta...
        # ---------------------------------------------------------------------
    fDEBUG = False
    while True:
        try:
            raw, payload = LnRs485._rs485Read(timeoutValue=2000, FORMAT=True) # return bytearray
            if raw.data:
                if fDEBUG: print (raw.hexm)
            if payload.data:
                if fDEBUG: print (payload.hexm)
                print (payload.dict.printTree(header='ricezione dati dallo slave: {}'.format(payload.data[LnRs485._fld.SRC_ADDR]), whatPrint='KV')) # whatPrint='LTKV'
                print ('\n'*2)
                break


        except (KeyboardInterrupt) as key:
            print (__name__, "Keybord interrupt has been pressed")
            LnRs485.Close()
            sys.exit()