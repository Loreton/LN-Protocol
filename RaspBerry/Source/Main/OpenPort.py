#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per ...........
# modified:  by Loreto notarantonio v2017-03-03_11.33.37
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
    logger      = Ln.SetLogger(package = __name__)

    iniMain     = gv.iniFile.MAIN
    relay       = gv.iniFile.ARDUINO_RELAY
    rs485       = gv.iniFile.RS485
    myCMD       = gv.iniFile.COMMANDS
    mySubCMD    = gv.iniFile.SUB_COMMANDS


    '''
    # assegnazione COMANDI presi dal sorgente di ARDUINO LnRs485.h
    LnRs485_COMMANDs = {
                        'RELAY_ECHO'    : bytes([ 1]),
                        'SLAVE_ECHO'    : bytes([ 2]),
                        'SLAVE_POLLING' : bytes([ 3]),
                        'SET_PINMODE'   : bytes([ 4]),
                        'DIGITAL'       : bytes([ 5]),
                        'ANALOG'        : bytes([ 6]),
                        'PWM'           : bytes([ 7]),
                    }

    LnRs485_SubCOMMANDs = {
                            'NO_REPLY'      : bytes([ 1]),
                            'REPLY'         : bytes([ 2]),
                            'READ_PIN'      : bytes([ 4]),
                            'WRITE_PIN'     : bytes([ 5]),
                        };


    fEXECUTE = gv.args.execute
    fDEBUG   = gv.args.debug


    myCMD            = Ln.Dict(LnRs485_COMMANDs)
    mySubCMD         = Ln.Dict(LnRs485_SubCOMMANDs)

    myDEV            = Ln.Dict()
    myDEV.masterAddr = bytes([int(iniMain.Rs485_MasterAddress)])        # Master Address
    myDEV.relayAddr  = bytes([int(iniMain.ArduinoRelayAddress)])       # Arduino Relay Address - di fanno non usato mai in quanto raggiunto tramite la seriale

    '''
    if gv.fDEBUG:
        myCMD.printTree()
        mySubCMD.printTree()
        # myDEV.printTree()

    # logger.info('Master Address: {}'.format(myDEV.masterAddr))
    # logger.info('Relay  Address: {}'.format(myDEV.relayAddr))


    sys.exit()
        # ===================================================
        # = RS-485
        # ===================================================

    if gv.args.mainCommand in ['rs485', 'raw', 'rs485_monitor']:
        LnRs485                             = gv.Ln.LnRs485    # short pointer alla classe
        rs485                               = gv.LnDict()
        rs485.MASTER_ADDRESS                = 0
        rs485.STX                           = int('0x02', 16)
        rs485.ETX                           = int('0x03', 16)
        # rs485.usbDevPath                    = gv.args.usbPort
        # rs485.baudRate                      = 9600
        rs485.mode                          = 'ascii'
        rs485.CRC                           = True

        if fDEBUG:rs485.printTree()


            # ----------------------------------------------------
            # = RS-485 open/initialize port
            # ----------------------------------------------------
        port = LnRs485(port=relay.Port, baudrate=relay.BaudRate, mode=rs485.mode, logger=Ln.SetLogger)
        port.STX = rs485.STX
        port.ETX = rs485.ETX
        port.CRC = rs485.CRC


        port.ClosePortAfterEachCall(False)
        print(port.__repr__())



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

