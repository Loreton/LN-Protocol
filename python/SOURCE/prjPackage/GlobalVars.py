#!/usr/bin/python -O
# -*- coding: iso-8859-1 -*-
# -*- coding: latin-1 -*-
#                                               by Alessandro Fioretti 2013, February
#                                               &  Loreto Notarantonio 2014, July
# ######################################################################################

import sys; sys.dont_write_bytecode = True

import platform
import os
import tempfile
# import cStringIO

class LnClass():
    pass


class GlobalVars():
    # thisDIR             = os.path.dirname(os.path.realpath(__file__))
    scriptDir           = os.path.dirname(os.path.abspath(sys.argv[0]))
    scriptName          = os.path.basename(os.path.abspath(sys.argv[0])).split('.')[0]
    baseDir             = scriptDir if not scriptDir.endswith('/bin') else os.path.dirname(scriptDir)

    fCONSOLE            = True
    fSYSLOG             = False
    fDEBUG              = False
    OpSys               = platform.system()


    # if scriptName == '__main__': scriptName = os.path.basename(scriptDir)
    # sys.path.insert(0, scriptDir)

    tempDir             = tempfile.gettempdir()
    tempDir             = '/tmp'
    logFname            = os.path.abspath(os.path.join(tempDir, scriptName) + '.log')

    REQ                 = LnClass()
    RSP                 = LnClass()


    REQ.conn            = None     # port/connection Handler
    REQ.addr            = 0     # is the Unit Id or slave address
    REQ.func            = 0     # is the Modbus code, such as 3 or 16
    REQ.protErr         = 0     # is the Modbus exception code
    REQ.rdOffset        = 0x0     # is the zero-based offset, so register 4x00001 is offset zero (0)
    REQ.rdCount         = 0     # is the word or bit count for the function
    REQ.rdData          = ()     # is a tuple or list holding words read
    REQ.wrOffset        = 0     # is like 'rdOffset', but used for writes - or for read/write functions
    REQ.wrCount         = 0     # is like 'rdCount', but used for writes - or for read/write functions
    REQ.wrData          = ()     # is a tuple or list holding words to write
    REQ.badCrc          = 0     # (for example) could be added to force a bad CRC to any request created
