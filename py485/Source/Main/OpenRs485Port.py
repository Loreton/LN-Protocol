#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per ...........
# modified:  by Loreto notarantonio v2017-03-03_11.33.37
#
# ######################################################################################

import LnLib    as Ln
import Source   as Prj
################################################################################
# - Open RS485 port
################################################################################
def openRs485Port(portData, rs485):
    logger = Ln.SetLogger(package = __package__)

    for key, val in portData.items():   logger.debug('portData    {0:<15}: {1}'.format(key, val))
    for key, val in rs485.items():      logger.debug('rs485       {0:<15}: {1}'.format(key, val))

        # ----------------------------------------------------
        # = RS-485 open/initialize port
        # ----------------------------------------------------
    port = Prj.Rs485(port=portData.Port, baudrate=portData.BaudRate, mode=rs485.mode, logger=Ln.SetLogger)
    port.STX = int(rs485.STX, 16)
    port.ETX = int(rs485.ETX, 16)
    port.CRC = eval(rs485.CRC)

    logger.info('{0:<15}: {1}'.format('STX',  port.STX))
    logger.info('{0:<15}: {1}'.format('STX',  port.ETX))
    logger.info('{0:<15}: {1}'.format('CRC',  port.CRC))

    port.ClosePortAfterEachCall(False)
    logger.info(port.__repr__())
    # port.Close()
    return port