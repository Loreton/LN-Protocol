#!/usr/bin/python3.5
#
# updated by ...: Loreto Notarantonio
# Version ......: 21-11-2017 17.04.03
# -----------------------------------------------
import  sys
from    pathlib import Path
from    time import  strftime
import  argparse


import LnLib as Ln; C=Ln.Color()


# from LnLib.Common.LnColor import LnColor; C=LnColor()

# import Source as Prj

class LnClass(): pass

from . ProgramParameters     import programParameters
# from . import Common as pCommon
# import ParseInput as LnParse
# sys.exit()

from . Common.DebugParameters      import debugParameters
from . Common.LogParameters        import logParameters
from . Common.MyHelp               import myHELP
from . OneTwoPositionalParameters  import positionalParameters
from . Common.CreateParser         import createParser

#######################################################
# ParseInput
#######################################################
def ParseInput(programVersion=0.1):

        # ---------------------------------------------------------
        # -   Identifichiamo il nome progetto dal nome directory
        # -   oppure passiamolo come parametro....
        # ---------------------------------------------------------
    programDir     = Path(sys.argv[0]).resolve().parent
    if programDir.name.lower() in ['bin',  'source']:
        programDir = programDir.parent

    prjName        = programDir.name   # nome della dir del programma

        # --------------------------
        # -   var di comodo da passare
        # --------------------------
    gVar = LnClass()
    gVar.defaultLogFile           = Path(programDir , 'log', prjName + strftime('_%Y-%m-%d') + '.log')
    gVar.defaultConfigFile        = Path(programDir , 'conf', prjName + '.ini')
    gVar.defaultRootDir           = programDir
    gVar.posizARGS                = 2
    gVar.prjName                  = prjName
    gVar.programVersion           = 'V1.0.0'
    gVar.description              = 'Ln-RS485 protocol'
    gVar.positionalParametersDict = {}

    # - Se abbiamo dei parametri posizionali allora inseriamo il modulo...
    if gVar.posizARGS == 1:
        gVar.positionalParametersDict  =  {
            'rs485_usb'     : "send/receive  Ln-RS485 protocol via USB_RS485_pen",
            'rs485_relay'   : "send/receive  Ln-RS485 protocol via Arduino Relay",
            'rs485_monitor' : "monitoring    Ln-RS485 protocol via USB_RS485_pen",
            'raw'           : "send/receive  Ln-RS485 protocol on USB port",
        }


    elif gVar.posizARGS == 2:
        gVar.positionalParametersDict  =  {
            'analog'     : {
                    'read':   "read analog bit",
                    'write':  "write analog bit",
                    },
            'digital'   : {
                    'read':   "read analog bit",
                    'write':  "write analog bit",
                    },
        }


    # myPosParam = positionalParameters(positionalParametersDict, nARGS=posizARGS, textMsg="RS485 command")
    positionalParm = positionalParameters(gVar)
    print (positionalParm)
    funcToCall = '_'.join(positionalParm).upper()                       # function: PRI_SEC
    if not funcToCall:
        funcToCall = 'programParameters'
    print (funcToCall)

    funcToCall = 'programParameters'


        # -----------------------------------
        # - creazione di un parser ad hoc
        # -----------------------------------
    myParser = createParser(gVar)




        # use dispatch pattern to invoke method with same name
        # ritorna un nameSpace
    this_mod = sys.modules[__name__]
    if hasattr(this_mod,  funcToCall):
        print ('................... FOUND')
        # getattr(this_mod, funcToCall)(myParser, positionalParm)
        print(gVar.defaultConfigFile)
        getattr(this_mod, funcToCall)(myParser, gVar)
    else:
        errMsg = '[{0}] - Command not yet implemented!'.format(funcToCall)
        # C.printColored(color=C.cyan, text=errMsg)
        # Ln.Exit(1, errMsg)





    # sys.exit()

    programParameters(myParser, gVar)
    logParameters(myParser, gVar)
    debugParameters(myParser)




        # lancio del parser...
    # args = vars(myParser.parse_args())
    print (sys.argv[gVar.posizARGS+1:])
    args = vars(myParser.parse_args(sys.argv[gVar.posizARGS+1:]))


    # se ho un solo parametro posizionale... eliminialo la LIST
    if gVar.posizARGS > 0: args['firstPosParameter']  = positionalParm[0]
    if gVar.posizARGS > 1: args['secondPosParameter'] = positionalParm[1]



        # --------------------------------------------
        # - verifica della congruenza di alcuni parametri:
        # - --log=False azzera anche il --log-filename]
        # --------------------------------------------
    if args['log'] == False: args['log_filename'] = None


        # -----------------------
        # - print dei parametri
        # -----------------------
    if args['parameters']:
        print()
        for key, val in args.items():
            if 'options ____' in key:
                continue
            # keyColor = C.getColored(color=C.yellowH, text=key)
            # valColor = C.getColored(color=C.yellow, text=val)
            print('     {0:<20}: {1}'.format(key, val))
        print()
        choice = input('press Enter to continue... (q|x to exit): ')
        if choice.lower() in ('x', 'q'): sys.exit()

    Ln.Exit(9999)
    return  args


