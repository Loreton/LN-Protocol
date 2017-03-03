#!/usr/bin/env python3
#
# modified:  by Loreto notarantonio v2017-03-03_11.34.04
#
# ######################################################################################

# ##########################################################################
# # RS485_setupPort
# ##########################################################################
def SetupPort(LnRs485, conf, address):

    port = LnRs485.Instrument(conf.usbDevPath, address, conf.mode)  # port name, slave address (in decimal)
    port.serial.baudrate = conf.baudRate
    port.serial.STX      = conf.STX
    port.serial.ETX      = conf.ETX

    return port
