#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# updated by ...: Loreto Notarantonio
# Version ......: 26-11-2017 18.04.00
#
# ######################################################################################


import os, sys
import LnLib as Ln
import Source as Prj


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
    monitor     = gv.iniFile.RS485_MONITOR_PORT
    rs485       = gv.iniFile.RS485_PROTOCOL
    myCMD       = gv.iniFile.COMMAND
    mySubCMD    = gv.iniFile.SUB_COMMAND


    for key, val in myCMD.items():      logger.debug('command     {0:<15}: {1}'.format(key, val))
    for key, val in mySubCMD.items():   logger.debug('sub_command {0:<15}: {1}'.format(key, val))


    # gv.args.printTree(header='Args values', fPAUSE=False)
    # relay.printTree(header='RELAY values', fPAUSE=False)

    myReqCommand = '{}.{}'.format(gv.args.firstPosParameter, gv.args.secondPosParameter)
        # ==========================================
        # = Apertura porta seriale
        # ==========================================
    myPort = Prj.openRs485Port(relay, rs485)

    if myReqCommand == 'digital.read':
        Prj.digitalRead(myPort, gv.iniFile, srcAddress=rs485.MasterAddress, destAddr=gv.args.slave_address, pinNO=gv.args.pin_number)

    elif myReqCommand == 'digital.write':
        Prj.digitalWrite(myPort, gv.args.slave_address, gv.iniFile)

    elif myReqCommand == 'monitor.rs485':
        Prj.monitorRS485(myPort)

    elif myReqCommand == 'monitor.raw':
        Prj.monitorRaw(myPort)

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
        port = Prj.Rs485(port=relay.Port, baudrate=relay.BaudRate, mode=rs485.mode, STX=4, ETX=5, CRC=False, logger=Ln.SetLogger)
        # port.STX = int(rs485.STX, 16)
        # port.ETX = int(rs485.ETX, 16)
        # port.CRC = eval(rs485.CRC)

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
            gv.Prj.SendMsg(gv, port, rs485)
        elif gv.args.fRAW:
            print ('... not yet implemented.\n')


    else:
        print(gv.args.actionCommand, 'not available')
        return

