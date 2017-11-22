#!/usr/bin/python3.5
#
# updated by ...: Loreto Notarantonio
# Version ......: 22-11-2017 11.19.40
# -----------------------------------------------
import  sys
from    pathlib import Path
from    time    import strftime


# from Source.ParseInput.NoPositionalParameters import noPositionalParameters
from . NoPositionalParameters import noPositionalParameters
from . DigitalWrite           import digitalWrite as DIGITAL_WRITE

import  LnLib as Ln; C = Ln.Color(); pInp = Ln.ParseInput


class LnClass(): pass

#######################################################
# ParseInput
#######################################################
def ParseInput(programVersion=0.1):

        # ---------------------------------------------------------
        # -   Identifichiamo il nome progetto dal nome directory
        # ---------------------------------------------------------
    programDir     = Path(sys.argv[0]).resolve().parent
    if programDir.name.lower() in ['bin',  'source']:
        programDir = programDir.parent
    prjName        = programDir.name   # nome della dir del programma

    defaultLogFile = Path(programDir , 'log', prjName + strftime('_%Y-%m-%d') + '.log')


    nPosizARGS = 2
    if nPosizARGS == 1:
        positionalParametersDict  =  {
            'rs485_usb'     : "send/receive  Ln-RS485 protocol via USB_RS485_pen",
            'rs485_relay'   : "send/receive  Ln-RS485 protocol via Arduino Relay",
            'rs485_monitor' : "monitoring    Ln-RS485 protocol via USB_RS485_pen",
            'raw'           : "send/receive  Ln-RS485 protocol on USB port",
        }


    elif nPosizARGS == 2:
        positionalParametersDict  =  {
            'analog'     : {
                    'read':   "read analog bit",
                    'write':  "write analog bit",
                    },
            'digital'   : {
                    'read':   "read analog bit",
                    'write':  "write analog bit",
                    },
        }

    else:
        nPosizARGS = 0
        positionalParametersDict  =  {}


        # ----------------------------------
        # - dict da passare alle funzioni
        # ----------------------------------
    gVar = LnClass()

    gVar.defaultConfigFile        = str(Path(programDir , 'conf', prjName + '.ini'))
    gVar.projectDir               = programDir
    gVar.posizARGS                = nPosizARGS
    gVar.prjName                  = prjName
    gVar.programVersion           = 'V1.0.0'
    gVar.description              = 'Ln-RS485 protocol'
    gVar.positionalParametersDict = positionalParametersDict


        # -------------------------------------
        # - lettura dei parametri posizionali
        # -------------------------------------
    posParser      = pInp.createParser(gVar)        # creazione di un parser ad hoc per passarglielo..
    positionalParm = pInp.positionalParameters(gVar, posParser)
    posFuncToCall  = '_'.join(positionalParm).upper()                       # function: PRI_SEC

    if not posFuncToCall:  # non abbiamo positional parameters
        posFuncToCall = 'noPositionalParameters'



    # ====================================================
    # = OPTIONAL PARAMETERs
    # ====================================================

        # -----------------------------------
        # - for the optional parameters
        # - create ad-hoc PARSER
        # -----------------------------------
    myParser = pInp.createParser(gVar)


        # ----------------------------------------------------------
        # - adding optional parameters
        # - calling the functionName dinalmically crated.
        # - use dispatch pattern to invoke method with same name
        # ----------------------------------------------------------
    this_mod = sys.modules[__name__]
    if hasattr(this_mod,  posFuncToCall):
        getattr(this_mod, posFuncToCall)(gVar, myParser)
    else:
        errMsg = '[{0}] - Command not yet implemented!'.format(posFuncToCall)
        Ln.Exit(1, errMsg)


        # ----------------------------------
        # - DEFAULT optional parameters
        # - valid for all projects
        # ----------------------------------
    pInp.logParameters(defaultLogFile, myParser)
    pInp.debugParameters(myParser)





        # ----------------------------------------------------------
        # - lancio del parser... per i restanti parametri opzionali
        # ----------------------------------------------------------
    args = vars(myParser.parse_args(sys.argv[gVar.posizARGS+1:]))


        # ----------------------------------------------
        # - creazione entry per i parametri posizionali
        # ----------------------------------------------
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
            if 'options ' in key:  continue
            # if '__________' in key:  continue
            print('     {0:<20}: {1}'.format(key, val))
        print()
        choice = input('press Enter to continue... (q|x to exit): ')
        if choice.lower() in ('x', 'q'): sys.exit()

    Ln.Exit(9999)
    return  args


