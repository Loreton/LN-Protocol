#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# updated by ...: Loreto Notarantonio
# Version ......: 24-01-2018 12.12.18
#
# ######################################################################################


import os, sys
import Source as Prj
import time
# import LnLib as Ln

# from Source.Setup import GlobalVars_Module as projectGlobalVars
# gV = projectGlobalVars

################################################################################
# - M A I N
# - Prevede:
# -  2 - Controllo parametri di input
# -  5 - Chiamata al programma principale del progetto
################################################################################
def Main(gv):
    # ----- common part into the Prj modules --------
    global Ln
    Ln     = Prj.LnLib
    logger = Ln.SetLogger(__name__)
    # print (logger)
    logger.info('ciao sono io 01')
    logger.info('ciao sono io 02')
    logger.info('ciao sono io 03')
    # Ln.Exit(9999)
    # -----------------------------------------------

    iniMain     = gv.iniFile.MAIN
    relay       = gv.iniFile.ARDUINO_RELAY_PORT
    monitor     = gv.iniFile.RS485_BUS_MONITORING_PORT
    rs485Prot   = gv.iniFile.RS485_PROTOCOL
    myCMD       = gv.iniFile.MAIN_COMMAND
    mySubCMD    = gv.iniFile.SUB_COMMAND

    # convert payload fields in integer value
    fld = Ln.Dict()
    for key,val in gv.iniFile.RS485_PAYLOAD_FIELD.items(): fld[key] = int(val)
    rs485Prot.payloadFieldName = fld



    for key, val in myCMD.items():      logger.debug('command     {0:<15}: {1}'.format(key, val))
    for key, val in mySubCMD.items():   logger.debug('sub_command {0:<15}: {1}'.format(key, val))

        # ==========================================
        # = Preparazione del PAYLOAD
        # ==========================================
    payload                 = bytearray(len(fld))
    payload[fld.SRC_ADDR]   = int(rs485Prot.MasterAddress, 16)



        # ==========================================
        # = Apertura porta seriale
        # = e process del comando
        # ==========================================
    if gv.args.firstPosParameter in ['digital']:
        myPort = Prj.openRs485Port(relay, rs485Prot)

        if gv.args.secondPosParameter == 'read':
            Prj.digitalRead(myPort, gv.iniFile, srcAddress=rs485Prot.MasterAddress, destAddr=gv.args.slave_address, pinNO=gv.args.pin_number)
        elif gv.args.secondPosParameter == 'toggle':
            # Prj.digitalToggle(myPort, gv.iniFile, srcAddress=rs485Prot.MasterAddress, destAddr=gv.args.slave_address, pinNO=gv.args.pin_number)
            Prj.digitalToggle(gv, myPort, payload=payload)
            print ('\n'*4)
            # time.sleep(1)
            # Prj.digitalToggle(gv, myPort, payload=payload)
            # print ('\n'*4)
            # time.sleep(1)
            # Prj.digitalToggle(gv, myPort, payload=payload)

        elif gv.args.secondPosParameter == 'write':
            Prj.digitalWrite(myPort, gv.args.slave_address, gv.iniFile)


    elif gv.args.firstPosParameter in ['monitor']:

        if gv.args.port:
            monitor.port = gv.args.port

        myPort = Prj.openRs485Port(monitor, rs485Prot)

        if gv.args.secondPosParameter == 'rs485':
            Prj.monitorRS485(myPort)

        elif gv.args.secondPosParameter == 'raw':
            Prj.monitorRaw(myPort, dHex=gv.args.hex, dText=gv.args.text, dChar=gv.args.char)

    else:
        errMsg = 'comando primario non previsto'
        myPort.Close()
        Ln.Exit(101, errMsg)

    myPort.Close()

    logger = Ln.SetLogger(__name__, exiting=True)

    # Ln.Exit(0)
