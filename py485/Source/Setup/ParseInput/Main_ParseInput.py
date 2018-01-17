#!/usr/bin/python3.5
#
# updated by ...: Loreto Notarantonio
# Version ......: 09-01-2018 07.47.25
# -----------------------------------------------


import  Source as Prj

# -----------------------------------------------------
# mi serve per passarlo come puntatore al ParseInput
# per chiamare la funzione delle command-line options
# La directory option conterrà i file che verranno
# richiamati in base ai parametri di input.
# -----------------------------------------------------
from . import Options as functionsLibPtr


#######################################################
# USER ParseInput
#######################################################
def ParseInput(description='Ln-RS485 protocol', programVersion='V0.1'):
    Ln = Prj.LnLib

    posizARGS = 2
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


    inpArgs = Ln.processInput(
            nPosArgs=posizARGS,
            parmDict=positionalParametersDict,
            funcLibPtr=functionsLibPtr,
            defFuncToCall='programOptions', # function to call only for posizARGS==0
            progrVersion=programVersion,
            prjDescr=description,
            prjDir=None,
            prjName=None)


    return  inpArgs
    Ln.Exit(9999)
