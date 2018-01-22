#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per ...........
# modified:  by Loreto notarantonio v2017-03-03_11.33.37
#
# ######################################################################################

import    Source as Prj
################################################################################
# - Open RS485 port
################################################################################
def openRs485Port(portData, rs485):
    # ----- common part into the Prj modules --------
    # import    Source as Prj
    global Ln
    Ln     = Prj.LnLib
    # C      = Ln.Color()
    # logger = Ln.SetLogger(__package__)
    # -----
    logger = Ln.SetLogger(package = __package__)

    for key, val in portData.items():   logger.debug('portData    {0:<15}: {1}'.format(key, val))
    for key, val in rs485.items():      logger.debug('rs485       {0:<15}: {1}'.format(key, val))

        # ----------------------------------------------------
        # = RS-485 open/initialize port
        # ----------------------------------------------------
    port = Ln.Rs485(port=portData.port, baudrate=portData.baudrate, mode=rs485.mode, useLogger=Ln.SetLogger, myDict=Ln.Dict)
    port.SetSTX(rs485.STX)
    port.SetETX(rs485.ETX)
    port.SetCRC(rs485.CRC)
    port.ClosePortAfterEachCall(False)
        # carichiamo i nomi dei campi del payload
    port.SetPayloadFieldName(rs485.payloadFieldName)


    # rs485.printTree()
    logger.info(port.__repr__())
    logger = Ln.SetLogger(__name__, exiting=True)
    return port