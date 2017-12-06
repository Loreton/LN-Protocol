#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# updated by ...: Loreto Notarantonio
# Version ......: 06-12-2017 16.43.18
#
# ######################################################################################


import os, sys
import LnLib as Ln
import Source as Prj

# from Source.Setup import GlobalVars_Module as projectGlobalVars
# gV = projectGlobalVars

################################################################################
# - M A I N
# - Prevede:
# -  2 - Controllo parametri di input
# -  5 - Chiamata al programma principale del progetto
################################################################################
def Main(gv):
    logger      = Ln.SetLogger(package = __package__)

    iniMain     = gv.iniFile.MAIN
    relay       = gv.iniFile.ARDUINO_RELAY_PORT
    monitor     = gv.iniFile.OTHER_MONITOR_PORT
    rs485Prot   = gv.iniFile.RS485_PROTOCOL
    myCMD       = gv.iniFile.MAIN_COMMAND
    mySubCMD    = gv.iniFile.SUB_COMMAND

    # convert payload fields in integer value
    fld = Ln.Dict()
    for key,val in gv.iniFile.RS485_PAYLOAD_FIELD.items(): fld[key] = int(val)
    gv.payloadFieldName = fld   # save in prjGlobalVars





    for key, val in myCMD.items():      logger.debug('command     {0:<15}: {1}'.format(key, val))
    for key, val in mySubCMD.items():   logger.debug('sub_command {0:<15}: {1}'.format(key, val))


    # gv.args.printTree(header='Args values', fPAUSE=False)
    # relay.printTree(header='RELAY values', fPAUSE=False)

    # myReqCommand = '{}.{}'.format(gv.args.firstPosParameter, gv.args.secondPosParameter)



        # ==========================================
        # = Preparazione del PAYLOAD
        # ==========================================
    payload                 = bytearray(len(fld))
    payload[fld.SRC_ADDR]   = int(rs485Prot.MasterAddress, 16)


        # ==========================================
        # = Apertura porta seriale
        # ==========================================

    if gv.args.firstPosParameter in ['digital']:
        myPort = Prj.openRs485Port(relay, rs485Prot)
        if gv.args.secondPosParameter == 'read':
            Prj.digitalRead(myPort, gv.iniFile, srcAddress=rs485Prot.MasterAddress, destAddr=gv.args.slave_address, pinNO=gv.args.pin_number)

        elif gv.args.secondPosParameter == 'toggle':
            # Prj.digitalToggle(myPort, gv.iniFile, srcAddress=rs485Prot.MasterAddress, destAddr=gv.args.slave_address, pinNO=gv.args.pin_number)
            Prj.digitalToggle(gv, myPort, payload=payload)

        elif gv.args.secondPosParameter == 'write':
            Prj.digitalWrite(myPort, gv.args.slave_address, gv.iniFile)


    elif gv.args.firstPosParameter in ['monitor']:
        if gv.args.port: monitor.port = gv.args.port
        myPort = Prj.openRs485Port(monitor, rs485Prot)

        if gv.args.secondPosParameter == 'rs485':
            Prj.monitorRS485(myPort)

        elif gv.args.secondPosParameter == 'raw':
            Prj.monitorRaw(myPort, inpArgs=gv.args)

    else:
        errMsg = 'comando primario non previsto'
        myPort.Close()
        Ln.Exit(101, errMsg)

    myPort.Close()


    Ln.Exit(0)

        # ===================================================
        # = RS-485
        # ===================================================
    if gv.args.firstPosParameter in ['digital']:
        gv.Prj.MasterRS485(gv, port)
        # logger.info('{0:<15}: {1}'.format('Relay Port',      relay.Port))
        # logger.info('{0:<15}: {1}'.format('Relay Address',   relay.Address))
        # logger.info('{0:<15}: {1}'.format('Relay BaudRate',  relay.BaudRate))

            # ----------------------------------------------------
            # = RS-485 open/initialize port
            # ----------------------------------------------------
        port = Prj.Rs485(port=relay.Port, baudrate=relay.BaudRate, mode=rs485Prot.mode, STX=4, ETX=5, CRC=False, logger=Ln.SetLogger)
        # port.STX = int(rs485Prot.STX, 16)
        # port.ETX = int(rs485Prot.ETX, 16)
        # port.CRC = eval(rs485Prot.CRC)

        # logger.info('{0:<15}: {1}'.format('STX',  port.STX))
        # logger.info('{0:<15}: {1}'.format('STX',  port.ETX))
        # logger.info('{0:<15}: {1}'.format('CRC',  port.CRC))

        port.ClosePortAfterEachCall(False)
        logger.info(port.__repr__())
        port.Close()

    sys.exit()

        # ===================================================
        # = serial port monitor
        # ===================================================

    if not port:
        print("non e' stato possibile selezionare alcuna porta per il comando immesso...")
        sys.exit()

    if gv.args.actionCommand == 'serial.read':
        gv.Prj.Monitor(gv, port)

    elif gv.args.actionCommand == 'read.raw':
        gv.Prj.Monitor(gv, port)

    elif gv.args.actionCommand == 'master.rs485':
        gv.Prj.MasterRS485(gv, port)

    elif gv.args.actionCommand == 'master.echo':
        gv.Prj.EchoTest(gv, port)

    elif gv.args.actionCommand == 'master.polling':
        gv.Prj.Polling(gv, port)

    elif gv.args.actionCommand == 'monitor.rs485':
        gv.Prj.MonitorRS485(gv, port)

    elif gv.args.actionCommand == 'monitor.raw':
        gv.Prj.MonitorRaw(gv, port)

    elif gv.args.actionCommand == 'send.rs485':
        gv.Prj.SendRS485(gv, port)

    elif gv.args.actionCommand == 'send.raw':
        print ('... not yet implemented.\n')


        # ===================================================
        # = serial port send
        # ===================================================
    elif gv.args.actionCommand == 'serial.send':
        if gv.args.fRS485:
            gv.Prj.SendMsg(gv, port, rs485Prot)
        elif gv.args.fRAW:
            print ('... not yet implemented.\n')


    else:
        print(gv.args.actionCommand, 'not available')
        return

