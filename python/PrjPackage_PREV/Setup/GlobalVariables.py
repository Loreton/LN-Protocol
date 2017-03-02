#!/usr/bin/python
# -*- coding: latin-1 -*-
# -*- coding: iso-8859-1 -*-
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import sys; sys.dont_write_bytecode = True

import platform
import os
import tempfile
import socket
# import argparse

import logging.config       # altrimenti si ottiene l'errore: 'module' object has no attribute 'config'

class LnClass(): pass
gv = LnClass()

# ####################################################################
# #
# ####################################################################
# def globalVariables(Prj, Ln, projectName=None):
def globalVariables(Prj, mainModule, projectName=None, fDEBUG=False):
    global gv

    gv.MAIN = LnClass()
    gv.Prj  = Prj

    preparePaths(mainModule, fDEBUG=fDEBUG)




    gv.projectName = projectName
    calledBy       = gv.LN.sys.calledBy

        # Classi che servono per il printDictionary
    # gv.myDictTYPES          = [LnClass, argparse.Namespace]
    gv.myDictTYPES          = [LnClass]



        # Calcolo dello scriptDir
    gv.MAIN.scriptDir = os.path.dirname(os.path.abspath(sys.argv[0]))

    if gv.MAIN.scriptDir.split(os.sep)[-1].lower() in ['source', 'bin']:
        gv.MAIN.projectDir = os.path.abspath(gv.MAIN.scriptDir + os.sep + '..')
    else:
        gv.MAIN.projectDir = gv.MAIN.scriptDir

    sys.path.insert(0, gv.MAIN.scriptDir)
    if projectName:
        gv.MAIN.scriptName = projectName
    else:
        gv.MAIN.scriptName = os.path.basename(os.path.abspath(sys.argv[0])).split('.')[0]
        if gv.MAIN.scriptName == '__main__':
            gv.MAIN.scriptName = os.path.basename(gv.MAIN.projectDir)


    gv.MAIN.OpSys                = platform.system()
    gv.MAIN.fullHostName         = socket.gethostname() if socket.gethostname().find('.')>=0 else socket.gethostbyaddr(socket.gethostname())[0]
    gv.MAIN.shortHostName        = gv.MAIN.fullHostName.split('.')[0]

    gv.MAIN.OK                   = 0
    gv.MAIN.WARNING              = 1
    gv.MAIN.ERROR                = 2
    gv.MAIN.CRITICAL             = 3
    gv.MAIN.UNKNOWN              = 4

    gv.MAIN.fCONSOLE             = False
    gv.MAIN.fSYSLOG              = False
    gv.MAIN.fDEBUG               = False
    gv.MAIN.tempDir              = tempfile.gettempdir()
    gv.MAIN.tempDir              = '/tmp'
    gv.MAIN.logFname             = "vedere il file LoggerConfig.ini"

    gv.MAIN.mainConfigDIR        = os.path.abspath(os.path.join(gv.MAIN.projectDir, 'conf' ))
    gv.MAIN.iniMainConfigFile    = os.path.join(gv.MAIN.mainConfigDIR, gv.MAIN.scriptName+'.ini')



        # Conterrà i valori dei parametri di input
    # gv.InpParam             = LnClass()
        # Conterrà i valori dei parametri del file INI
    gv.INI                  = LnClass()
    gv.INI_RAW              = LnClass()

    REQ                     = LnClass()
    RSP                     = LnClass()


    REQ.conn                = None              # port/connection Handler
    REQ.addr                = 0                 # is the Unit Id or slave address
    REQ.func                = 0                 # is the Modbus code, such as 3 or 16
    REQ.protErr             = 0                 # is the Modbus exception code
    REQ.rdOffset            = 0x0               # is the zero-based offset, so register 4x00001 is offset zero (0)
    REQ.rdCount             = 0                 # is the word or bit count for the function
    REQ.rdData              = ()                # is a tuple or list holding words read
    REQ.wrOffset            = 0                 # is like 'rdOffset', but used for writes - or for read/write functions
    REQ.wrCount             = 0                 # is like 'rdCount', but used for writes - or for read/write functions
    REQ.wrData              = ()                # is a tuple or list holding words to write
    REQ.badCrc              = 0                 # (for example) could be added to force a bad CRC to any request created

    gv.REQ  = REQ
    gv.RSP  = RSP
    # gv.MAIN = MAIN

    if fDEBUG:
        gv.LN.dict.printDictionaryTree(gv, gv, header="Global Vars [%s]" % calledBy(0), console=True, exit=True, retCols='TV', lTAB=' '*4, listInLine=2)



    return gv



################################################################################
# - inseriamo la lista delle dir dove possiamo trovare le LnFunctions
# - vale anche per quando siamo all'interno del .zip
################################################################################
def preparePaths(mainModule, fDEBUG=False):
    global gv
    # mainModule                      = os.path.abspath(os.path.realpath(__file__))
    mainModuleDIR                   = os.path.dirname(mainModule)
    mainModuleName, mainModuleExt   = os.path.basename(mainModule).split('.')

    # print(mainModuleDIR, mainModuleName, mainModuleExt)

    # MAIN.exit()
    pathsLevels = [ '.', '../', '../../', '../../../', '../../../../' ]

    zipFnameList = ['LnFunctions_29-10-2015.zip']
    deepLevel = 3

    for i in reversed(range(deepLevel)):
        for zipName in zipFnameList:
            path = os.path.abspath(os.path.join(mainModuleDIR, pathsLevels[i], zipName))
            if os.path.isfile(path):
                sys.path.insert(0, path)

        path = os.path.abspath(os.path.join(mainModuleDIR, pathsLevels[i]))
        sys.path.insert(0, path)


    if fDEBUG:
        for path in sys.path:
            print ('......', path)

    import LnFunctions       as Ln          # All'interno dello zip deve esserci la dir LnFunction

    gv.MAIN.mainModuleDIR    = mainModuleDIR
    gv.MAIN.mainModuleName   = mainModuleName
    gv.MAIN.mainModuleExt    = mainModuleExt
    gv.LN                   = Ln

    return