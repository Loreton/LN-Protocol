#!/usr/bin/python3.4
# -*- coding: iso-8859-1 -*-
# -*- coding: utf-8 -*-
#
# updated by ...: Loreto Notarantonio
# Version ......: 15-12-2017 15.26.42
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
LnLibPath = Path(sys.argv[0]).resolve().parent / 'bin' / 'LnLib_2017-12-11.zipx'
sys.path.insert(0, str(LnLibPath))


import  LnLib as Ln
import  Source as Prj

def testLnDict():
    gv      = Ln.Dict() #ss gv oggetto dictionary passabile, serve per la 95

        # ==========================================
        # = Preparazione del PAYLOAD  #ss parte definita dai campi fld
        # ==========================================

    relay      = Ln.Dict()      #ss classe - nuovo oggetto relay
    relay.port = '/dev/ttyUSB0' #ss attributo
    relay.mode = 'ascii'        #ss attributo
    relay.baudrate = 9600       #ss attributo

    # relay.printTree(header="relay object", fEXIT=True)



    fld                         = Ln.Dict() #ss altro oggetto
    fld.SRC_ADDR                = 0         #ss attributo
    fld.DEST_ADDR               = 1
    fld.SEQNO_H                 = 2
    fld.SEQNO_L                 = 3
    fld.RCODE                   = 4
    fld.CMD                     = 5
    fld.SUB_CMD                 = 6
    fld.COMMAND_DATA            = 7
    fld.PIN_NO                  = 7
    fld.PIN_ACTION              = 8
    # fld.printDict(header="fields names", fEXIT=True)

    rs485Prot                   = Ln.Dict() #ss altro oggetto
    rs485Prot.MasterAddress     = 1
    rs485Prot.STX               = 0x02
    rs485Prot.ETX               = 0x03
    rs485Prot.mode              = 'ascii'
    rs485Prot.CRC               = True
    rs485Prot.payloadFieldName  = fld
    # rs485Prot.printDict(header="rs485", fEXIT=True)


    mainCmd = {}    #ss altro modo di creare un dictionary
    mainCmd['RELAY_ECHO_CMD'] = 0x01
    mainCmd['SLAVE_ECHO_CMD'] = 0x02

    mainCmd = {"RELAY_ECHO_CMD": 0x01, "SLAVE_ECHO_CMD": 0x02}

        # puntamento ai comandi e sottocomandi
    mainCmd                         = Ln.Dict() #ss
    mainCmd.RELAY_ECHO_CMD          = 0x01  #ss RELAY_ECHO_CMD = keys 0x01 = valore
    mainCmd.SLAVE_ECHO_CMD          = 0x02
    mainCmd.POLLING_CMD             = 0x03
    mainCmd.SET_PINMODE_CMD         = 0x21
    mainCmd.DIGITAL_CMD             = 0x31
    mainCmd.ANALOG_CMD              = 0x32
    mainCmd.PWM_CMD                 = 0x33

    subCmd                         = Ln.Dict() #ss
    subCmd.NO_REPLY                = 0x01     # for echo command
    subCmd.REPLY                   = 0x02     # for echo command
    subCmd.READ_PIN                = 0x04     # for analog/digital commands
    subCmd.WRITE_PIN               = 0x05     # for analog/digital commands
    subCmd.TOGGLE_PIN              = 0x06     # for digital commands
    #subCmd.printDict(header="Global vars", fEXIT=True)



    gv.rs485Prot  = rs485Prot
    gv.mainCmd = mainCmd
    gv.subCmd  = subCmd
    gv.printDict(header="Global vars", fEXIT=True)


################################################################################
# - M A I N
################################################################################
if __name__ == "__main__":
    testLnDict()
    gv        = Ln.Dict()

        # -------------------------------
        # - Lettura parametri di input
        # -------------------------------
    args      = Prj.ParseInput() # ; print (args)
    gv.args   = Ln.Dict(args)
    gv.fDEBUG = gv.args.debug
    if gv.fDEBUG: gv.args.printTree(fPAUSE=True)

        # -------------------------------
        # - Inizializzazione del logger
        # -------------------------------
    logger    = Ln.InitLogger(  toFILE=gv.args.log,
                                logfilename=gv.args.log_filename,
                                toCONSOLE=gv.args.log_console,
                                loglevel=gv.args.loglevel,
                                ARGS=args)


        # ------------------------
        # - Lettura del file.ini
        # ------------------------
    iniFile = Ln.ReadIniFile(gv.args.ini_file, strict=True)
    iniFile.read(resolveEnvVars=False)
    gv.iniFile = Ln.Dict(iniFile.dict)
    gv.args.iniFile = Ln.Dict(iniFile.dict)
    if gv.fDEBUG: gv.iniFile.printTree(header="INI File", fPAUSE=True)

        # ===================================================
        # - Inizio applicazione
        # ===================================================

    Prj.Main(gv)
    gv.Ln.Exit(0, "completed", printStack=False, stackLevel=9, console=True)
    sys.exit()




