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
    port = Prj.Rs485(port=portData.port, baudrate=portData.baudrate, mode=rs485.mode, logger=Ln.SetLogger, myDict=Ln.Dict)
    port.SetSTX(rs485.STX)
    port.SetETX(rs485.ETX)
    port.SetCRC(rs485.CRC)
    port.ClosePortAfterEachCall(False)

    logger.info(port.__repr__())
    # port.Close()
    return port