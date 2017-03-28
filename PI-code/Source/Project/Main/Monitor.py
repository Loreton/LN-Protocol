#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per ...........
# modified:  by Loreto notarantonio v2017-03-03_11.33.37
#
# ######################################################################################


import os, sys

import time


################################################################################
# - M A I N
# - Prevede:
# -  2 - Controllo parametri di input
# -  5 - Chiamata al programma principale del progetto
################################################################################
def Monitor(gv):
    logger  = gv.Ln.SetLogger(package=__name__)
    C       = gv.Ln.LnColor()


    fEXECUTE = gv.INPUT_PARAM.fEXECUTE
    fDEBUG   = gv.INPUT_PARAM.fDEBUG


        # ===================================================
        # = RS-485
        # ===================================================
    LnRs485                             = gv.Prj.LnRs485.LnRs485_Instrument   # short pointer alla classe
    # LnRs485                             = gv.Prj.LnRs485.LnRs485   # short pointer alla classe
    rs485                               = gv.LnDict()
    rs485.MASTER_ADDRESS                = 0
    rs485.STX                           = int('0x02', 16)
    rs485.ETX                           = int('0x03', 16)
    rs485.usbDevPath                    = gv.INPUT_PARAM.usbPort
    rs485.baudRate                      = 9600
    rs485.mode                          = 'ascii'
    rs485.CRC                           = True
    rs485.close_port_after_each_call    = True

    if fDEBUG:rs485.printTree()

        # rs485.Class.CLOSE_PORT_AFTER_EACH_CALL = True


        # ===================================================
        # = RS-485 port monitor
        # ===================================================
    try:
        address = 5
        print('setting port {0} to address {1}'.format(rs485.usbDevPath, address))
        port = LnRs485(port=rs485.usbDevPath, slaveaddress=address, baudrate=rs485.baudRate, mode=rs485.mode, logger=gv.Ln.SetLogger)  # port name, slave address (in decimal)
        port.STX                        = rs485.STX
        port.ETX                        = rs485.ETX
        port.CRC                        = rs485.CRC
        port.close_port_after_each_call = rs485.close_port_after_each_call

        print(port.__repr__())

        print ('... press ctrl-c to stop the process.')

        while True:
            print( '--- monitoring: {0}'.format(rs485.usbDevPath))
            payLoad, rowData = port.readData()
            # print ('rowData (Hex):   {0}'.format(' '.join('{0:02x}'.format(x) for x in rowData)))
            msg = '{TITLE:<15}: ({LEN}) {DATA}'.format(TITLE='raw data', LEN=len(rowData), DATA=' '.join('{:02X}'.format(x) for x in rowData))
            print (msg)

            if payLoad:
                print ('fields       :   SA DA data')
                print ('payLoad (Hex):   {0}'.format(' '.join('{0:02x}'.format(x) for x in payLoad)))
                # print ('payLoad (chr):     {0}'.format(' '.join('{0:>2}'.format(chr(x)) for x in payLoad)))
            else:
                print ('payLoad ERROR....')
            print()


    except (KeyboardInterrupt) as key:
        print ("Keybord interrupt has been pressed")
        sys.exit()



