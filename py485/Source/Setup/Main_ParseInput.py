#!/usr/bin/python3.5
#
# updated by ...: Loreto Notarantonio
# Version ......: 03-12-2017 08.33.41
# -----------------------------------------------

import  sys
import  Source as Prj
import  LnLib as Ln; C = Ln.Color()


class LnClass(): pass

#######################################################
# USER ParseInput
# identificare il numero di parametri posizionali
# e creare le funzioni che verranno chiamate automaticamente:
#    nPosizARGS == 0: programOptions()
#    nPosizARGS == 1: posizParam.upper()
#    nPosizARGS == 2: posizParam1.upper()_posizParam2.upper()
# che dovranno essere tutti raggiungibili tramite:
#     Prj.function()
#######################################################
def ParseInput(description='Ln-RS485 protocol', programVersion='V0.1'):

    nPosizARGS = 2
    positionalParametersDict  =  {
    'analog'     : {
            'read':   "read  analog bit",
            'write':  "write analog bit",
            },
    'digital'   : {
            'read':   "read   digital bit",
            'write':  "write  digital bit",
            'toggle': "toggle digital bit",
            },
    'monitor'   : {
            'rs485':   "read RS485-bus traffic",
            'raw':     "read RS485-bus raw traffic",
            },
    }


        # ----------------------------------
        # - dict da passare alle funzioni
        # ----------------------------------
    gVar = LnClass()

    gVar.projectDir               = None
    gVar.prjName                  = None
    gVar.programVersion           = programVersion
    gVar.description              = description

    gVar.nPosizARGS                = nPosizARGS
    gVar.positionalParametersDict = positionalParametersDict

    args = Ln.processInput(gVar, prjRoot=Prj)

    return  args
    Ln.Exit(9999)

