#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Master per protocollo Ln-Rs485
#         Invia il comando sul Relay collegato sulla porta seriale
#         Il Relay ritrasmette il comando sul bus Rs485
#
# updated by ...: Loreto Notarantonio
# Version ......: 06-12-2017 17.13.51
#
# ######################################################################################


import sys
import time
import  LnLib as Ln; C = Ln.Color()
import Source as Prj

# gV = Prj.gVars


def digitalRead(LnRs485, iniData, srcAddress, destAddr, pinNO):
    pass

########################################################
# - digitalToggle()
########################################################
def digitalToggle(gv, LnRs485, payload):
    assert type(payload) == bytearray
    logger  = Ln.SetLogger(package=__package__)

    _fld = gv.payloadFieldName

    _mainCmd = gv.iniFile.MAIN_COMMAND
    _subCmd  = gv.iniFile.SUB_COMMAND
    _args    = gv.args




        # ===================================================
        # = RS-485 sendMessage
        # ===================================================
    C.printColored (color=C.yellowH, text='... press ctrl-c to stop the process.', tab=8)
    # iniData.printTree()

    # sourceAddr  = int.from_bytes(iniData.COMMANDS.master, 'little')
    # destAddr    = int.from_bytes(iniData.slave_address, 'little')

    payload[_fld.DEST_ADDR] = int(gv.args.slave_address)
    payload[_fld.CMD]       = int(_mainCmd.DIGITAL_CMD, 16)     # COMMAND
    payload[_fld.SUB_CMD]   = int(_subCmd.TOGGLE_PIN,   16)     # SubCOMMAND
    payload[_fld.PIN_NO]    = _args.pin_number     # pinNO
    high, low               = LnRs485.getSeqCounter()
    payload[_fld.SEQNO_L]   = low
    payload[_fld.SEQNO_H]   = high
    payload[_fld.RCODE]     = 0 # 0 per la TX


    while True:
        print ()
        print ("sending toggle digital pin...")
        try:
            dataSent = LnRs485._rs485Write(payload)
            time.sleep(3)

        except (KeyboardInterrupt) as key:
            print (__name__, "Keybord interrupt has been pressed")
            sys.exit()

        sys.exit()

        print ()
        print ("waiting for response...")
        try:
            data = port.readRawData(EOD=[], hex=True, text=True, char=False, TIMEOUT=1000)
            if data:
                print('data has been received...')


            payLoad, rawData = serialRelayPort.readData(TIMEOUT=1000, fDEBUG=True)
            if not payLoad:
                print ('payLoad ERROR....')
            print()


        except (KeyboardInterrupt) as key:
            print (__name__, "Keybord interrupt has been pressed")
            sys.exit()

    return 0

