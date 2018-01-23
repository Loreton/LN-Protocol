#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Master per protocollo Ln-Rs485
#         Invia il comando sul Relay collegato sulla porta seriale
#         Il Relay ritrasmette il comando sul bus Rs485
#
# updated by ...: Loreto Notarantonio
# Version ......: 23-01-2018 16.58.39
#
# ######################################################################################


import  sys
import  Source as Prj

def digitalRead(serialPort, iniData, srcAddress, destAddr, pinNO):
    pass

########################################################
# - digitalToggle()
########################################################
def digitalToggle(gv, serialPort, payload):
    assert type(payload) == bytearray

    Ln     = Prj.LnLib
    C      = Ln.Color()
    logger = Ln.SetLogger(package=__name__)



        # puntamento ai fieldNames
    _fld     = serialPort._fld

        # puntamento ai comandi e sottocomandi
    _mainCmd = gv.iniFile.MAIN_COMMAND
    _subCmd  = gv.iniFile.SUB_COMMAND


    C.printColored (color=C.yellowH, text='... press ctrl-c to stop the process.', tab=8)

        # ===================================================
        # = RS-485 preparazione del comando
        # ===================================================
    payload[_fld.SEQNO_H], payload[_fld.SEQNO_L] = serialPort._seqCounter
    payload[_fld.RCODE]     = 0 # 0 per la TX

    payload[_fld.DEST_ADDR] = int(gv.args.slave_address)
    payload[_fld.CMD]       = int(_mainCmd.DIGITAL_CMD, 16)     # COMMAND
    payload[_fld.SUB_CMD]   = int(_subCmd.TOGGLE_PIN,   16)     # SubCOMMAND
    payload[_fld.PIN_NO]    = gv.args.pin_number     # pinNO



        # ---------------------------------------------------------------------
        # - Se non lo riceviamo vuol diche che c'è un problema
        # ---------------------------------------------------------------------
        # - invio del messaggio al Relay ....
    Prj.SendToRelay(serialPort, payload)

        # - ... attesa dello stesso come echo
    fDEBUG = False
    while True:
        try:
            logger.info('waiting for response...')
            print('waiting for response...')
            data232, data485 = serialPort.read485(timeoutValue=2000) # return dict.raw dict.hexd dict.hexm dict.text dict.char
            logger.info('received Data: {}'.format(data232.raw))
            print('received Data: {}'.format(data232.raw))
            if data485.raw:
                logger.info(data485.dict, dictTitle='ricezione dati dallo slave: {}'.format(data485.raw[serialPort._fld.SRC_ADDR]))
                print (data485.dict.printTree(header='ricezione dati dallo slave: {}'.format(data485.raw[serialPort._fld.SRC_ADDR]), whatPrint='KV')) # whatPrint='LTKV'
                break


        except (KeyboardInterrupt) as key:
            print (__name__, "Keybord interrupt has been pressed")
            serialPort.Close()
            sys.exit()

    logger = Ln.SetLogger(__name__, exiting=True)
