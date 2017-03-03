#!/usr/bin/env python3
#


# ##########################################################################
# # RS485_setupMaster(usbDevPath)
# ##########################################################################
def RS485_setupMaster(usbDevPath):

    rs485.CLOSE_PORT_AFTER_EACH_CALL = True

    Master = rs485.Instrument(usbDevPath, 0, rs485.MODE_ASCII)  # port name, slave address (in decimal)
    # Master.serial.baudrate = 19200
    Master.serial.baudrate = 9600
    Master.serial.STX      = gv.prot
    Master.serial.STX      = gv.prot.STX
    Master.serial.ETX      = gv.prot.ETX

    return Master


