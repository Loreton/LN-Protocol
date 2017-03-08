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
        LnRs485                   = gv.Prj.LnRs485   # short pointer alla classe
        rs485                     = gv.LnDict()
        rs485.MASTER_ADDRESS      = 0
        rs485.STX                 = 0x02
        rs485.ETX                 = 0x03
        rs485.usbDevPath          = gv.INPUT_PARAM.usbPort
        rs485.baudRate            = 9600
        rs485.mode                = 'ascii'

        if fDEBUG:rs485.printTree()

        # rs485.Class.CLOSE_PORT_AFTER_EACH_CALL = True




        # ===================================================
        # = RS-485 port monitor
        # ===================================================
    if gv.INPUT_PARAM.actionCommand == 'rs485.monitor':
            # ------------------------------
            # - Inizializzazione
            # ------------------------------
        try:
            # port = gv.Prj.LnRs485.Instrument(rs485.usbDevPath, 0, rs485.mode)  # port name, slave address (in decimal)
            # monitorPort = gv.Prj.rs485.SetupPort(gv.Prj.LnRs485, rs485, 5)
            address = 5
            print('setting port {0} to address {1}'.format(rs485.usbDevPath, address))
            port = LnRs485.Instrument(rs485.usbDevPath, address, rs485.mode, logger=gv.Ln.SetLogger)  # port name, slave address (in decimal)
            port.serial.baudrate = rs485.baudRate
            port.serial.STX      = rs485.STX
            port.serial.ETX      = rs485.ETX

            print ('... press ctrl-c to stop the process.')
            while True:
                data = monitorPort.readData(fDEBUG=True)
                print ('...', data)

        except (KeyboardInterrupt) as key:
            print ("Keybord interrupt has been pressed")
            sys.exit()


    elif gv.INPUT_PARAM.actionCommand == 'rs485.send':
            # ------------------------------
            # - Inizializzazione
            # ------------------------------
        try:
            address = 5
            print('setting port {0} to address {1}'.format(rs485.usbDevPath, address))
            port = LnRs485.Instrument(rs485.usbDevPath, address, rs485.mode, logger=gv.Ln.SetLogger)  # port name, slave address (in decimal)
            port.serial.baudrate = rs485.baudRate
            port.serial.STX      = rs485.STX
            port.serial.ETX      = rs485.ETX
            # sendingPort = gv.Prj.rs485.SetupPort(gv.Prj.LnRs485, rs485, 5)
            print ('... press ctrl-c to stop the process.')
            index = 0
            basedata = 'Loreto.'
            while True:
                index += 1
                data = '[{0}.{1:04}]'.format(basedata, index)
                line = '[{0}:{1:04}] - {2}'.format(rs485.usbDevPath, index, data)
                print (line)
                port.writeData('Loreto', fDEBUG=True)
                time.sleep(5)


        except (KeyboardInterrupt) as key:
            print ("Keybord interrupt has been pressed")
            sys.exit()


    else:
        print(gv.INPUT_PARAM.actionCommand, 'not available')
        return

