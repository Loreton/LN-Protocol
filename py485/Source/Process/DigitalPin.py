#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Master per protocollo Ln-Rs485
#         Invia il comando sul Relay collegato sulla porta seriale
#         Il Relay ritrasmette il comando sul bus Rs485
#
# updated by ...: Loreto Notarantonio
# Version ......: 18-01-2018 15.52.18
#
# ######################################################################################


import  sys
import  Source as Prj

def digitalRead(LnRs485, iniData, srcAddress, destAddr, pinNO):
    pass

########################################################
# - digitalToggle()
########################################################
def digitalToggle(gv, LnRs485, payload):
    assert type(payload) == bytearray

    Ln     = Prj.LnLib
    C      = Ln.Color()
    logger = Ln.SetLogger(package=__name__)



        # puntamento ai fieldNames
    _fld     = LnRs485._fld

        # puntamento ai comandi e sottocomandi
    _mainCmd = gv.iniFile.MAIN_COMMAND
    _subCmd  = gv.iniFile.SUB_COMMAND


    C.printColored (color=C.yellowH, text='... press ctrl-c to stop the process.', tab=8)

    PIN_NO      = 7
    PIN_ACTION  = 8

        # ===================================================
        # = RS-485 preparazione del comando
        # ===================================================
    payload[_fld.SEQNO_H], payload[_fld.SEQNO_L] = LnRs485._seqCounter
    payload[_fld.RCODE]     = 0 # 0 per la TX

    payload[_fld.DEST_ADDR] = int(gv.args.slave_address)
    payload[_fld.CMD]       = int(_mainCmd.DIGITAL_CMD, 16)     # COMMAND
    payload[_fld.SUB_CMD]   = int(_subCmd.TOGGLE_PIN,   16)     # SubCOMMAND
    payload[PIN_NO]         = gv.args.pin_number     # pinNO



        # ---------------------------------------------------------------------
        # - Se non lo riceviamo vuol diche che c'è un problema
        # ---------------------------------------------------------------------
        # - invio del messaggio al Relay ....
    Prj.SendToRelay(LnRs485, payload)

        # - ... attesa dello stesso come echo
    fDEBUG = False
    while True:
        try:
            data232, payload = LnRs485.read485(timeoutValue=2000) # return bytearray
            if data232.raw:
                if fDEBUG: print (data232.hexm)

            if payload.raw:
                if fDEBUG: print (payload.hexm)
                print (payload.dict.printTree(header='ricezione dati dallo slave: {}'.format(payload.raw[LnRs485._fld.SRC_ADDR]), whatPrint='KV')) # whatPrint='LTKV'
                print ('\n'*2)
                break


        except (KeyboardInterrupt) as key:
            print (__name__, "Keybord interrupt has been pressed")
            LnRs485.Close()
            sys.exit()