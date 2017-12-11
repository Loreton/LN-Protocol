#!/usr/bin/python3.4
# -*- coding: iso-8859-1 -*-
# -*- coding: utf-8 -*-
#
# updated by ...: Loreto Notarantonio
# Version ......: 11-12-2017 09.09.38
#                                               by Loreto Notarantonio
# ######################################################################################
import sys; sys.dont_write_bytecode = True
import os
from pathlib import Path


# ----------------------------------------------
# - Inserimento del path corretto della LnLib
# - Le path per LnLib vanno impostate
# - prima di fare gli import
# ----------------------------------------------
LnLibPath = Path(sys.argv[0]).resolve().parent / 'bin' / 'LnLib_2017-12-11.zip'
sys.path.insert(0, str(LnLibPath))


import  LnLib as Ln
import  Source as Prj
from Source.Process.DigitalPinSS import digitalToggle as SSdigitalToggle

################################################################################
# - M A I N
################################################################################
if __name__ == "__main__":
    gv      = Ln.Dict()

        # ==========================================
        # = Preparazione del PAYLOAD
        # ==========================================

    relay      = Ln.Dict()
    relay.port = '/dev/ttyUSB0'
    relay.mode = 'ascii'
    relay.baudrate = 9600



    fld                         = Ln.Dict()
    fld.SRC_ADDR                = 0
    fld.DEST_ADDR               = 1
    fld.SEQNO_H                 = 2
    fld.SEQNO_L                 = 3
    fld.RCODE                   = 4
    fld.CMD                     = 5
    fld.SUB_CMD                 = 6
    fld.COMMAND_DATA            = 7
    fld.PIN_NO                  = 7
    fld.PIN_ACTION              = 8

    rs485Prot                   = Ln.Dict()
    rs485Prot.MasterAddress     = 1
    rs485Prot.STX               = 0x02
    rs485Prot.ETX               = 0x03
    rs485Prot.mode              = 'ascii'
    rs485Prot.CRC               = True
    rs485Prot.payloadFieldName  = fld


        # puntamento ai comandi e sottocomandi
    mainCmd = Ln.Dict()
    mainCmd.RELAY_ECHO_CMD          = 0x01
    mainCmd.SLAVE_ECHO_CMD          = 0x02
    mainCmd.POLLING_CMD             = 0x03
    mainCmd.SET_PINMODE_CMD         = 0x21
    mainCmd.DIGITAL_CMD             = 0x31
    mainCmd.ANALOG_CMD              = 0x32
    mainCmd.PWM_CMD                 = 0x33

    subCmd  = Ln.Dict()
    subCmd.NO_REPLY                = 0x01     # for echo command
    subCmd.REPLY                   = 0x02     # for echo command
    subCmd.READ_PIN                = 0x04     # for analog/digital commands
    subCmd.WRITE_PIN               = 0x05     # for analog/digital commands
    subCmd.TOGGLE_PIN              = 0x06     # for digital commands




    gv.rs485Prot  = rs485Prot
    gv.mainCmd = mainCmd
    gv.subCmd  = subCmd

    myRelay = Prj.openRs485Port(relay, rs485Prot)

    payload                 = bytearray(len(fld))
    payload[fld.SRC_ADDR]   = rs485Prot.MasterAddress



    SSdigitalToggle(gv, myRelay, payload=payload)

    myRelay.Close()


    Ln.Exit(0, "completed", printStack=False, stackLevel=9, console=True)
    sys.exit()




