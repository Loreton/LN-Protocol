#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per ...........
# modified:  by Loreto notarantonio 2017-03-28 09.59.46
#
# ######################################################################################


import os, sys
import time
class LnClass(): pass

################################################################################
# -
################################################################################
def SendMsg(gv, sendPort, rs485):
    logger  = gv.Ln.SetLogger(package=__name__)
    C       = gv.Ln.LnColor()


    fDEBUG   = gv.input.fDEBUG
    TYPE = 3

    if TYPE == 1:
            # ===================================================
            # = RS-485 sendMessage
            # ===================================================
        try:
            print ('... press ctrl-c to stop the process.')

            sourceAddr  = bytes([0]) # MASTER
            destAddr    = bytes([gv.input.rs485Address])
            sourceAddr  = int.from_bytes(sourceAddr, 'little')
            destAddr    = int.from_bytes(destAddr, 'little')
            # print ('sourceAddr: x{0:02x}'.format(sourceAddr))
            # print ('destAddr:   x{0:02x}'.format(destAddr))

            basedata = 'Loreto.'
            index = 0

            while True:
                index += 1
                dataStr = '{DATA}.{INX:04}'.format(DATA=basedata, INX=index)

                dataToSend = bytearray()
                dataToSend.append(sourceAddr)
                dataToSend.append(destAddr)
                for x in dataStr:
                    dataToSend.append(ord(x))

                dataSent = sendPort.writeData(dataToSend, fDEBUG=True)
                time.sleep(5)


        except (KeyboardInterrupt) as key:
            print ("Keybord interrupt has been pressed")
            sys.exit()




    elif TYPE == 2:
            # ===================================================
            # = RS-485 sendMessage
            # ===================================================
        try:
            print ('... press ctrl-c to stop the process.')

            sourceAddr  = bytes([0]) # MASTER
            destAddr    = bytes([gv.input.rs485Address])
            basedata = 'Loreto.'

            cmd = LnClass()
            cmd.sourceAddr = int.from_bytes(sourceAddr, 'little')
            cmd.destAddr   = int.from_bytes(destAddr, 'little')

            index = 0
            while True:
                index += 1
                cmd.dataStr = '{DATA}.{INX:04}'.format(DATA=basedata, INX=index)
                dataSent = sendPort.writeDataCMD(cmd, fDEBUG=True)
                time.sleep(5)


        except (KeyboardInterrupt) as key:
            print ("Keybord interrupt has been pressed")
            sys.exit()



    elif TYPE == 3:
            # ===================================================
            # = RS-485 sendMessage
            # ===================================================
        try:
            print ('... press ctrl-c to stop the process.')

            sourceAddr  = bytes([0]) # MASTER
            destAddr    = bytes([gv.input.rs485Address])

            sourceAddr = int.from_bytes(sourceAddr, 'little')
            destAddr   = int.from_bytes(destAddr, 'little')

            basedata = 'Loreto.'
            index = 0
            while True:
                index += 1
                dataStr = '{DATA}.{INX:04}'.format(DATA=basedata, INX=index)
                dataSent = sendPort.writeDataSDD(sourceAddr, destAddr, dataStr, fDEBUG=True)
                time.sleep(5)


        except (KeyboardInterrupt) as key:
            print ("Keybord interrupt has been pressed")
            sys.exit()

