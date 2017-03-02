#!/usr/bin/env python3
# -*- coding: iso-8859-1 -*-
#
# Scope:  ............
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import sys, os; sys.dont_write_bytecode = True
import serial
import time

import logging
import logging.handlers as Handlers
#---------------------------------------------------------------------------#
# This will send the error messages in the specified namespace to a file.
# The available namespaces in pymodbus are as follows:
#---------------------------------------------------------------------------#
# * pymodbus.*          - The root namespace
# * pymodbus.server.*   - all logging messages involving the modbus server
# * pymodbus.client.*   - all logging messages involving the client
# * pymodbus.protocol.* - all logging messages inside the protocol layer
#---------------------------------------------------------------------------#
logging.basicConfig()
log = logging.getLogger('pymodbus.server')
log = logging.getLogger()
log.setLevel(logging.DEBUG)


class LnClass(): pass

import  PrjPackage as Ln
# from    prjPackage.LnMinimalModbus            import *
import  PrjPackage.LnRs485  as rs485


# gv                  = GlobalVars          # shortCut alle GlobalVars
gv                          = Ln.GlobalVars          # shortCut alle GlobalVars
gv.Ln                       = Ln                  # Funzioni
gv.prot                     = LnClass()
gv.prot.MASTER_ADDRESS      = 0
gv.prot.STX                 = 0x02
gv.prot.ETX                 = 0x03
gv.rcvedMSG                 = LnClass()
# xx = GlobalVars.LnClass()


BYTE_STX            = 0
BYTE_MsgNO_LOW      = 1
BYTE_MsgNO_HIGH     = 2
BYTE_DestADDR       = 3
BYTE_SourceADDR     = 4
BYTE_StartOfMsg     = 5




__author__   = 'loreto Notarantonio'
__email__    = 'nloreto@gmail.com'
__url__      = 'http://minimalmodbus.sourceforge.net/'
__license__  = 'Apache License, Version 2.0'

__version__  = '0.1'
__status__   = 'Beta'
__revision__ = '$Rev: 200 $'
__date__     = '$Date: 2015-03-28 $'



if sys.version > '3':    import binascii

# Allow long also in Python3
# http://python3porting.com/noconv.html
if sys.version > '3':    long = int




##############################
## Modbus instrument object ##
##############################


def startSlave(usbDevPath):
    slave01 = rs485.Instrument(usbDevPath, 1, rs485.MODE_ASCII)  # port name, slave address (in decimal)
    # slave01.serial.baudrate = 19200
    slave01.serial.baudrate = 9600
    slave01.serial.STX      = gv.prot
    slave01.serial.STX      = gv.prot.STX
    slave01.serial.ETX      = gv.prot.ETX
    data = slave01.readData(fDEBUG=False)

    return data




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


messageNumber = 0
# ##########################################################################
# # VW_sendMSG()
# #     destAddr = destination devAddress
# #     msg      = messaggio da inviare (bytearray())
# ##########################################################################
def VW_sendMSG(gv, destAddr, msg):
    import struct
    global messageNumber

    if isinstance(msg, str):
        # print ('is str')
        baData = bytearray(map(ord, msg))
        # oppure:
            # data = bytearray()
            # data.extend(map(ord, msg))
    elif isinstance(msg, list):
        print ('is list - NOT implemented.')
        sys.exit()
    elif isinstance(msg, bytes):
        print ('is bytes - NOT implemented.')
        sys.exit()
    elif isinstance(msg, bytearray):
        # print ('is bytearray')
        baData = msg
    else:
        print (type(msg), len(msg), ' - NOT implemented.')
        sys.exit()

    dataLen = len(baData)

    #@TODO
        # big-endian
        # --- https://docs.python.org/3.3/library/struct.html
        # --- Use sys.byteorder to check the endianness of your system.
        # --- struct.pack_into('>H', y, 0, 2);
    messageNumber += 1                              # Numero del messaggio che stiamo inviando 2 bytes
    msgNO = struct.pack('>H', messageNumber);       # convertiamo un numero (H=2bytes) (>=big-endian) in bytes[]


    data = bytearray()                              # creazione dell'Array da inviare
    data.append(gv.prot.STX)                        # STX
    data.extend(msgNO)                              # numero SEQ del Messaggio
    data.append(destAddr)                           # destAddress
    data.append(gv.prot.MASTER_ADDRESS)             # sourceAddress
    data.extend(baData)                             # Dati da inviare
    data.append(gv.prot.ETX)                        # ETX



    # print("\n{0:<10}".format('Sending:'), end='' )
    # print (' '.join('{:02x}'.format(c) for c in data))
    # print( )
    printHexMsg(data, prefix='Sending:')


    gv.VW.tx.put(data)

        # WAIT for completing SEND
    while not gv.VW.tx.ready():
        time.sleep(0.1)



def printHexMsg(data, prefix=''):

    if data:
        print("\n{0:<10}".format(prefix), end='' )
        print (' '.join('{:02X}'.format(c) for c in data))
        # print( )

        TextOfMsg = ' '.join('{:02X}'.format(c) for c in data[BYTE_StartOfMsg:-1])

        print("      STX           : {0:02X}".format(data[0]))
        print("      MSG_NO        : {0:02X} {1:02X}".format(data[BYTE_MsgNO_LOW], data[BYTE_MsgNO_HIGH]))
        print("      from --> to   : {0:02X} {1:02X}".format(data[BYTE_SourceADDR], data[BYTE_DestADDR]))
        print("      Messaggio     : {0}".format(TextOfMsg))
        print("      ETX           : {0:02X}".format(data[-1]))

        print()



# ##########################################################################
# # VW_getMSG()
# # se attivato subi dopo un invio, rilegge il messaggio inviato da se stesso.
# ##########################################################################
def VW_getMSG_OK(gv, Timeout):

    gv.VW.rx.cancel()

    start = time.time()
    currTime = time.time()-start

    while currTime < Timeout:

        currTime = time.time()-start
        while gv.VW.rx.ready():
            print("\nReceived {0:3.2f}:".format(currTime), end='')
            for c in gv.VW.rx.get():
                print("{0:02X} ".format(c), end='')    # python3

            print()

        # time.sleep(0.1)

    return

# ##########################################################################
# # VW_getMSG()
# # se attivato subi dopo un invio, rilegge il messaggio inviato da se stesso.
# ##########################################################################
def checkMsgValidity(gv, data):

    gv.rcvedMSG.STX         = data[BYTE_STX]
    gv.rcvedMSG.msgNO       = data[BYTE_MsgNO_HIGH:BYTE_MsgNO_LOW]
    gv.rcvedMSG.destAddr    = data[BYTE_DestADDR]
    gv.rcvedMSG.srcAddr     = data[BYTE_SourceADDR]
    gv.rcvedMSG.data        = data[BYTE_StartOfMsg:-1]
    gv.rcvedMSG.ETX         = data[-1]

    if gv.rcvedMSG.STX !=  gv.prot.STX:
        print('Il byte di STX non è valido {0:02X} '.format(data[0]))
        data = ''

    elif gv.rcvedMSG.ETX !=  gv.prot.ETX:
        print('Il byte di ETX non è valido {0:02X} '.format(data[-1]))
        data = ''

    elif gv.rcvedMSG.srcAddr ==  gv.prot.MASTER_ADDRESS:
        print('ECHO received - Ricevuto messaggio inviato da me stesso.')
        data = ''

    elif gv.rcvedMSG.destAddr !=  gv.prot.MASTER_ADDRESS:
        print('Destination Address is not Master Address {0:02X} '.format(gv.rcvedMSG.destAddr))
        data = ''

    else:
        pass
        # fullMSG     = ' '.join('{:02X}'.format(c) for c in data)
        # TextOfMsg   = ' '.join('{:02X}'.format(c) for c in data[MSG_START:-1])

    return data

# ##########################################################################
# # VW_getMSG()
# # se attivato subi dopo un invio, rilegge il messaggio inviato da se stesso.
# ##########################################################################
def VW_getMSG(gv, Timeout):


    start = time.time()
    currTime = time.time()-start



    while currTime < Timeout:

        data = bytearray()
        currTime = time.time()-start
        while gv.VW.rx.ready():
            print("\nReceived {0:3.2f}:".format(currTime), end='')
            while gv.VW.rx.ready():
                for c in gv.VW.rx.get():
                    data.append(c)
                    # print("{0:02X} ".format(c), end='')    # python3


            if checkMsgValidity(gv, data):
                printHexMsg(data, prefix='')

    return


# ##########################################################################
# # RS485_sendMSG()
# ##########################################################################
def RS485_sendMSG(gv, slaveADDR):
    data = bytearray()
    data.append(slaveADDR)   # Address
    data.append(0x11)
    data.append(0x12)
    data = Master.writeData(data, fDEBUG=True)
    return

import time

# ##########################################################################
# # setupVirtualWire()
# ##########################################################################
def setupVirtualWire(gv, stop=False):
    import pigpio
    # import vw
    import vw_Loreto as vw
    # import vw_Loreto2 as vw

    if stop:
        gv.VW.rx.cancel()
        gv.VW.tx.cancel()
        gv.VW.pi.stop()

    else:
        RX_pin  = 19        # GPIO19 - pin 35
        TX_pin  = 26        # GPIO26 - pin 37
        BPS     = 2000

        gv.VW = LnClass()
        gv.VW.pi = pigpio.pi() # Connect to local Pi.

        gv.VW.rx = vw.rx(gv.VW.pi, RX_pin, BPS) # Specify Pi, rx gpio, and baud.
        gv.VW.tx = vw.tx(gv.VW.pi, TX_pin, BPS) # Specify Pi, tx gpio, and baud.


#########################################
# # pollingVirtualWire()
#########################################
def pollingVirtualWire(gv):
    tx = gv.VW.tx
    msg = 0
    start = time.time()

    while not tx.ready(): time.sleep(0.1)

    # time.sleep(0.2)
    # tx.put([48, 49, 65, ((msg>>6)&0x3F)+32, (msg&0x3F)+32])
    # while not tx.ready(): time.sleep(0.1)
    # time.sleep(0.2)

    tx.put("Hello World #{}!".format(msg))
    while not tx.ready(): time.sleep(0.1)

    '''
    while rx.ready():
     # print("".join(chr (c) for c in rx.get()))
     for c in rx.get():
        # print("{0:02X}".format(c)),          # python2
        print("{0:02X} ".format(c), end='')    # python3

     print()

    '''


def itIsOK(gv):
    start = time.time()
    msg = 0
    while (time.time()-start) < 300:

        msg += 1

        while not gv.VW.tx.ready():
            time.sleep(3)
            time.sleep(0.1)

        strToSend = "Hello World #{}!".format(msg)
        print("\nsending:", strToSend )
        gv.VW.tx.put(strToSend)

        while gv.VW.rx.ready():
             # print("".join(chr (c) for c in rx.get()))
            print("\nReceived:", end='')
            for c in gv.VW.rx.get():
                print("{0:02X} ".format(c), end='')    # python3
                # print("{0:02X}".format(c)),          # python2

        print()

# #######################################################
# #
# #######################################################
def itIsOK_Base(gv):
    start = time.time()
    msg = 0
    while (time.time()-start) < 300:

        msg += 1

        while not gv.VW.tx.ready():
            time.sleep(3)
            time.sleep(0.1)

        strToSend = "Hello World #{}!".format(msg)
        print("\nsending:", strToSend )
        gv.VW.tx.put(strToSend)

        while gv.VW.rx.ready():
             # print("".join(chr (c) for c in rx.get()))
            print("\nReceived:", end='')
            for c in gv.VW.rx.get():
                print("{0:02X} ".format(c), end='')    # python3
                # print("{0:02X}".format(c)),          # python2

        print()

#TODO: Sto lavorando a questa funzione. Devo scoprire la lunghezza massima dei dati che posso inviare.
# #######################################################
# #
# #######################################################
def itIsOK_Base1(gv, Timeout):
    start = time.time()
    msg = 0

    while (time.time()-start) < Timeout:

        msg += 1

        while not gv.VW.tx.ready():
            time.sleep(3)
            time.sleep(0.1)

        strToSend = "Hello World #{}!".format(msg)
        print("\nsending:", strToSend )
        gv.VW.tx.put(strToSend)

        while gv.VW.rx.ready():
             # print("".join(chr (c) for c in rx.get()))
            print("\nReceived:", end='')
            for c in gv.VW.rx.get():
                print("{0:02X} ".format(c), end='')    # python3
                # print("{0:02X}".format(c)),          # python2

        print()


# #######################################################
# #
# #######################################################
def itIsOK_Base2(gv, Timeout):
    msg = 0

    msg += 1

    while not gv.VW.tx.ready():
        time.sleep(3)

    msgToSend = "Loreto Loreto Loreto Loreto "  # NON funziona
    msgToSend = "1234567890123456"                        # FUNZIONA dino a 16 caratteri dopo di che non riceviamo più
    msgToSend = "1234567890"                        # FUNZIONA dino a 16 caratteri dopo di che non riceviamo più
    VW_sendMSG(gv, destAddr=0xFF, msg=msgToSend)

    VW_getMSG(gv, Timeout)

    '''
    start = time.time()
    currTime = time.time()-start

    while currTime < Timeout:

        currTime = time.time()-start
        while gv.VW.rx.ready():
            print("\nReceived {0:3.2f}:".format(currTime), end='')
            for c in gv.VW.rx.get():
                print("{0:02X} ".format(c), end='')    # python3

            print()

        # time.sleep(0.1)
    '''

# #######################################################
# #
# #######################################################
def Test01(gv, Timeout):

    msgToSend = [1,2,3,4,5,6,7,8]
    msgToSend = bytes(10)
    msgToSend = bytearray(10)
    msgToSend = "Hello World !"
    VW_sendMSG(gv, destAddr=0xFF, msg=msgToSend)

    start = time.time()
    msg = 0

    while (time.time()-start) < Timeout:

        while gv.VW.rx.ready():
             # print("".join(chr (c) for c in rx.get()))
            print("\nReceived:", end='')
            for c in gv.VW.rx.get():
                print("{0:02X} ".format(c), end='')    # python3
                # print("{0:02X}".format(c)),          # python2
            print()

        Timeout -= 1
        time.sleep(.1)

    print()



################################################################################
# - M A I N
#
#   MASTER di LN-Protocol
#   Provvede a dialogare su due fronti:
#       1 - RS-485 (quindi fornire il device dove si trova l'RS485 USB converter
#       1 - VirtualWire - quindi modulo Wireless
################################################################################
if __name__ == "__main__":
    gv.Lnf = Ln.preparePATHs(False)
    # Ln.testVirtualWire()
    # sys.exit()

#TODO: Perde alcuni pacchetti in ricezione. NON affidabile

        # ---------------------------------------------
        # - Indirizzi degli SLAVE da controllare
        # ---------------------------------------------
    slaveADRESS = [1, 2]

    if len(sys.argv) != 2:
        print ("immettere:")
        print ("    USBdev (per la parte RS485):   ttyUSBx")
        sys.exit()

        # Verifica della presenza del device
    usbDevPath = Ln.isUsbDevice(sys.argv[1])
    if not Ln.isUsbDevice(usbDevPath):
        print('{0} - is not a valid USB device'.format(sys.argv[1]))
        sys.exit()


        # ------------------------------
        # - Inizializzazione
        # ------------------------------
    try:
        Master = RS485_setupMaster(usbDevPath)
        setupVirtualWire(gv)

    except (KeyboardInterrupt) as key:
        print ("Keybord interrupt has been pressed")
        sys.exit()

    while True:

        try:
            # itIsOK_Base(gv)
            # itIsOK_Base1(gv, 300)
            itIsOK_Base2(gv, 10)
            # Test01(gv, 300)
            # sys.exit()

        except (KeyboardInterrupt) as key:
            print (key)
            # choice      = input().strip()
            # if choice.upper() == 'X': break
            break
