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


    fEXECUTE = gv.INPUT_PARAM.fEXECUTE
    fDEBUG   = gv.INPUT_PARAM.fDEBUG



        # ===================================================
        # = RS-485
        # ===================================================
    if gv.INPUT_PARAM.actionCommand.startswith('rs485.'):
        LnRs485                             = gv.Ln.LnRs485    # short pointer alla classe
        rs485                               = gv.LnDict()
        # rs485.Class                         = gv.Ln.LnRs485    # short pointer alla classe
        rs485.MASTER_ADDRESS                = 0
        rs485.STX                           = int('0x02', 16)
        rs485.ETX                           = int('0x03', 16)
        rs485.usbDevPath                    = gv.INPUT_PARAM.usbPort
        rs485.baudRate                      = 9600
        rs485.mode                          = 'ascii'
        rs485.CRC                           = True
        rs485.close_port_after_each_call    = True

        if fDEBUG:rs485.printTree()

            # ----------------------------------------------------
            # = RS-485 open/initialize port
            # ----------------------------------------------------
        port = LnRs485(port=rs485.usbDevPath, baudrate=rs485.baudRate, mode=rs485.mode, logger=gv.Ln.SetLogger)  # port name, slave address (in decimal)
        port.STX                        = rs485.STX
        port.ETX                        = rs485.ETX
        port.CRC                        = rs485.CRC
        port.close_port_after_each_call = rs485.close_port_after_each_call

        print(port.__repr__())

        # ===================================================
        # = RS-485 port monitor
        # ===================================================
    if gv.INPUT_PARAM.actionCommand == 'rs485.monitor':
        print( '--- monitoring device: {0}'.format(rs485.usbDevPath))
        gv.Prj.Monitor(gv, port)


    elif gv.INPUT_PARAM.actionCommand == 'rs485.send':
        gv.Prj.SendMsg(gv, port, rs485)

    else:
        print(gv.INPUT_PARAM.actionCommand, 'not available')
        return

