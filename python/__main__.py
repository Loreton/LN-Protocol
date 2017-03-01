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
# logging.basicConfig()
# log = logging.getLogger('pymodbus.server')
# log = logging.getLogger()
# log.setLevel(logging.DEBUG)

# class LnClass(): pass


# import  prjPackage as Ln
# from    prjPackage.LnMinimalModbus            import *
# import  prjPackage.LnRs485  as rs485


# gv                  = GlobalVars          # shortCut alle GlobalVars
# gv                          = Ln.GlobalVars          # shortCut alle GlobalVars
# gv.Ln                       = Ln                  # Funzioni
# gv.prot                     = LnClass()
# gv.prot.MASTER_ADDRESS      = 0
# gv.prot.STX                 = 0x02
# gv.prot.ETX                 = 0x03
# gv.rcvedMSG                 = LnClass()
# xx = GlobalVars.LnClass()


# BYTE_STX            = 0
# BYTE_MsgNO_LOW      = 1
# BYTE_MsgNO_HIGH     = 2
# BYTE_DestADDR       = 3
# BYTE_SourceADDR     = 4
# BYTE_StartOfMsg     = 5


__author__   = 'loreto Notarantonio'
__email__    = 'nloreto@gmail.com'
__url__      = 'http://minimalmodbus.sourceforge.net/'
__license__  = 'Apache License, Version 2.0'

__version__  = '0.1'
__status__   = 'Beta'
__revision__ = '$Rev: 200 $'
__date__     = '$Date: 2015-03-28 $'



# if sys.version > '3':    import binascii

# Allow long also in Python3
# http://python3porting.com/noconv.html
# if sys.version > '3':    long = int



################################################################################
# - inseriamo la lista delle dir dove possiamo trovare le LnFunctions
# - vale anche per quando siamo all'interno del .zip
################################################################################
def preparePATHs(fDEBUG):
    thisModule                      = os.path.abspath(os.path.realpath(__file__))
    thisModuleDIR                   = os.path.dirname(thisModule)
    thisModuleName, thisModuleExt   = os.path.basename(thisModule).split('.')

    print(thisModuleDIR, thisModuleName, thisModuleExt)
    pathsLevels = [ '.', '../', '../../', '../../../', '../../../../' ]

    if thisModuleExt == 'zip':
        level = 3
        zipFnameList = ['LnFunctions.zip', 'LnFunctions_2015-10-16.zip']
    else:
        level = 2
        zipFnameList = ''
        zipFnameList = ['LnFunctions_2015-10-16.zip']

    for i in reversed(range(level)):
        for zipName in zipFnameList:
            path = os.path.abspath(os.path.join(thisModuleDIR, pathsLevels[i], zipName))
            if os.path.isfile(path):
                sys.path.insert(0, path)

        path = os.path.abspath(os.path.join(thisModuleDIR, pathsLevels[i]))
        sys.path.insert(0, path)


    if fDEBUG:
        for path in sys.path:
            print ('......', path)

    import LnFunctions       as Ln          # All'interno dello zip deve esserci la dir LnFunction

    return Ln


################################################################################
# - M A I N
# - Imposta le variabili per fare l'import delle funzioni
# - Preleva alcuni parametri di input
# - Legge il file.ini
# - Chiama il vero main applicativo
################################################################################
import PrjPackage   as Prj
if __name__ == "__main__":
    thisModule  = os.path.abspath(os.path.realpath(__file__))
    gv          = Prj.setup.globalVariables(Prj, mainModule=thisModule, projectName='LN-Protocol', fDEBUG=False)
    calledBy    = gv.LN.sys.calledBy


    gv.MAIN.DEBUG    = True
        # ---------------------------------------------------------
        # - SetUp del log
        # ---------------------------------------------------------
    logConfigFileName = os.path.join(gv.MAIN.mainConfigDIR, 'LoggerConfig.ini')
    if gv.MAIN.DEBUG: print ("    {0:<32}: {1}".format('Reading LOG configuration file', logConfigFileName))
    # logger      = gv.LN.logger.setLogger(gv, logFile=logConfigFileName, pkgName='LN-Protocol')
    # logger      = gv.LN.logger.setLogger(gv, pkgName=__name__)
    gv.MAIN.logFileName = Prj.setup.setLogger(gv, logFile=logConfigFileName, pkgName='LN-Protocol')
    logger              = Prj.setup.setLogger(gv, pkgName=__name__)
    if gv.MAIN.DEBUG:   print ("    {0:<32}: {1}".format('using LOG file', gv.MAIN.logFileName))

    gv.MAIN.DEBUG    = False








################################################################################
# - M A I N
#
#   MASTER di LN-Protocol
#   Provvede a dialogare su due fronti:
#       1 - RS-485 (quindi fornire il device dove si trova l'RS485 USB converter
#       1 - VirtualWire - quindi modulo Wireless
################################################################################
if __name__ == "__main__x":
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
