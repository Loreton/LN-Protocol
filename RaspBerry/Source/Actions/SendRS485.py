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
def SendRS485(gv, sendPort):
    logger  = gv.Ln.SetLogger(package=__name__)
    C       = gv.Ln.LnColor()

    sendPort.ClosePortAfterEachCall(True)
    print(sendPort.__repr__())



    fDEBUG   = gv.inputParam.fDEBUG
        # ===================================================
        # = RS-485 sendMessage
        # ===================================================
    print ('... press ctrl-c to stop the process.')

    # gv.inputParam.rs485Address = [11, 12]

    sourceAddr  = bytes([0]) # MASTER
    sourceAddr = int.from_bytes(sourceAddr, 'little')
    basedata = 'Loreto.'

    seqNO = 0
    while True:
        for destAddress in gv.inputParam.rs485Address:
            destAddr   = bytes([destAddress])
            destAddr   = int.from_bytes(destAddr, 'little')

            try:
                seqNO += 1
                print(seqNO)
                dataStr  = '{DATA}.{INX:04}'.format(DATA=basedata, INX=seqNO)
                # dataSent = sendPort.writeDataSDD(sourceAddr, destAddr, dataStr, fDEBUG=True)
                dataSent = sendPort.writeDataSDD(sourceAddr, destAddr, basedata, fDEBUG=True)

                time.sleep(10)


            except (KeyboardInterrupt) as key:
                print ("Keybord interrupt has been pressed")
                sys.exit()



    '''
    TYPE = 4
    if TYPE == 1:
            # ===================================================
            # = RS-485 sendMessage
            # ===================================================
        try:
            print ('... press ctrl-c to stop the process.')

            sourceAddr  = bytes([0]) # MASTER
            destAddr    = bytes([gv.inputParam.rs485Address])
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
            destAddr    = bytes([gv.inputParam.rs485Address])
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
            destAddr    = bytes([gv.inputParam.rs485Address])

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


    elif TYPE == 4:
            # ===================================================
            # = RS-485 sendMessage
            # ===================================================
        print ('... press ctrl-c to stop the process.')

        # gv.inputParam.rs485Address = [11, 12]

        sourceAddr  = bytes([0]) # MASTER
        sourceAddr = int.from_bytes(sourceAddr, 'little')
        basedata = 'Loreto.'

        while True:
            index = 0
            for destAddress in gv.inputParam.rs485Address:
                destAddr   = bytes([destAddress])
                destAddr   = int.from_bytes(destAddr, 'little')

                try:
                    index += 1
                    print(index)
                    dataStr  = '{DATA}.{INX:04}'.format(DATA=basedata, INX=index)
                    dataSent = sendPort.writeDataSDD(sourceAddr, destAddr, dataStr, fDEBUG=True)
                    time.sleep(10)


                except (KeyboardInterrupt) as key:
                    print ("Keybord interrupt has been pressed")
                    sys.exit()

    '''
