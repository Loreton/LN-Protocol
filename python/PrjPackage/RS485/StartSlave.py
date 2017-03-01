#!/usr/bin/env python3
#


##############################
##
##############################
def RS485_startSlave(usbDevPath):
    slave01 = rs485.Instrument(usbDevPath, 1, rs485.MODE_ASCII)  # port name, slave address (in decimal)
    # slave01.serial.baudrate = 19200
    slave01.serial.baudrate = 9600
    slave01.serial.STX      = gv.prot
    slave01.serial.STX      = gv.prot.STX
    slave01.serial.ETX      = gv.prot.ETX
    data = slave01.readData(fDEBUG=False)

    return data
