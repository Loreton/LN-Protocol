#!/usr/bin/env python3
#
# modified:  by Loreto notarantonio v2017-03-03_11.34.04
#
# ######################################################################################

# ##########################################################################
# # RS485_setupPort
# ##########################################################################
def SetupPort(LnRs485, conf, address):

    print('setting port {0} to address {1}'.format(conf.usbDevPath, address))
    port = LnRs485.Instrument(conf.usbDevPath, address, conf.mode)  # port name, slave address (in decimal)
    port.serial.baudrate = conf.baudRate
    port.serial.STX      = conf.STX
    port.serial.ETX      = conf.ETX

    return port



# def SetupPort(conf):
#     port0 = serial.Serial(port=usbDevPath,
#             baudrate=conf.baudRate,
#             parity=serial.PARITY_NONE,
#             stopbits=serial.STOPBITS_ONE,
#             bytesize=serial.EIGHTBITS,
#             timeout = 6
#             )

    return port0