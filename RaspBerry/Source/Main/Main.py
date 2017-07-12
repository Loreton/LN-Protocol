#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per ...........
# modified:  by Loreto notarantonio v2017-03-03_11.33.37
#
# ######################################################################################


import os, sys
import datetime
this_mod = sys.modules[__name__]
import time




# ssh -o "NumberOfPasswordPrompts=1" -o "StrictHostKeyChecking=no" -i /cygdrive/c/Users/f602250/.ssh/id_rsa -l f602250 esil600.ac.bankit.it 'bash -s' < j:/GIT-REPO/Python3/ServerScan/conf/LnDiscovery.sh

################################################################################
# - M A I N
# - Prevede:
# -  2 - Controllo parametri di input
# -  5 - Chiamata al programma principale del progetto
################################################################################
def Main(gv, action):
    logger  = gv.Ln.SetLogger(package=__name__)
    C       = gv.Ln.LnColor()


    fEXECUTE = gv.input.fEXECUTE
    fDEBUG   = gv.input.fDEBUG



    print ('.{}.'.format(gv.input.actionCommand))
        # ===================================================
        # = RS-485
        # ===================================================
    cmd, subcmd = gv.input.actionCommand.split('.')
    if subcmd in ['rs485', 'raw', 'echo']:
        LnRs485                             = gv.Ln.LnRs485    # short pointer alla classe
        rs485                               = gv.LnDict()
        rs485.MASTER_ADDRESS                = 0
        rs485.STX                           = int('0x02', 16)
        rs485.ETX                           = int('0x03', 16)
        rs485.usbDevPath                    = gv.input.usbPort
        rs485.baudRate                      = 9600
        rs485.mode                          = 'ascii'
        rs485.CRC                           = True

        if fDEBUG:rs485.printTree()


            # ----------------------------------------------------
            # = RS-485 open/initialize port
            # ----------------------------------------------------
        port = LnRs485(port=rs485.usbDevPath, baudrate=rs485.baudRate, mode=rs485.mode, logger=gv.Ln.SetLogger)
        port.STX = rs485.STX
        port.ETX = rs485.ETX
        port.CRC = rs485.CRC


    port.ClosePortAfterEachCall(False)
    print(port.__repr__())


        # ===================================================
        # = serial port monitor
        # ===================================================
    if gv.input.actionCommand == 'serial.read':
        gv.Prj.Monitor(gv, port)

    elif gv.input.actionCommand == 'read.raw':
        gv.Prj.Monitor(gv, port)

    elif gv.input.actionCommand == 'master.rs485':
        gv.Prj.MasterRS485(gv, port)

    elif gv.input.actionCommand == 'master.echo':
        gv.Prj.EchoTest(gv, port)

    elif gv.input.actionCommand == 'monitor.rs485':
        gv.Prj.MonitorRS485(gv, port)

    elif gv.input.actionCommand == 'monitor.raw':
        gv.Prj.MonitorRaw(gv, port)

    elif gv.input.actionCommand == 'send.rs485':
        gv.Prj.SendRS485(gv, port)

    elif gv.input.actionCommand == 'send.raw':
        print ('... not yet implemented.\n')


        # ===================================================
        # = serial port send
        # ===================================================
    elif gv.input.actionCommand == 'serial.send':
        if gv.input.fRS485:
            gv.Prj.SendMsg(gv, port, rs485)
        elif gv.input.fRAW:
            print ('... not yet implemented.\n')


    else:
        print(gv.input.actionCommand, 'not available')
        return

