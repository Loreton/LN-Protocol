#!/usr/bin/python3.5
#
# updated by ...: Loreto Notarantonio
# Version ......: 23-11-2017 17.07.37
# -----------------------------------------------
import  sys
from    pathlib import Path
from    time    import strftime

import Source as Prj


import  LnLib as Ln; C = Ln.Color()


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



    nPosizARGS = 0
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
                'read':   "read  analog bit",
                'write':  "write analog bit",
                },
        'digital'   : {
                'read':   "read  digital bit",
                'write':  "write digital bit",
                },
        'monitor'   : {
                'read':   "read RS485-bus traffic",
                },
    }

    else:
        nPosizARGS = 0
        positionalParametersDict  =  {}



        # ----------------------------------
        # - dict da passare alle funzioni
        # ----------------------------------
    gVar = LnClass()

    # gVar.projectDir               = programDir
    # nPosizARGS                = nPosizARGS
    gVar.prjName                  = prjName
    gVar.programVersion           = 'V1.0.0'
    gVar.description              = 'Ln-RS485 protocol'
    # gVar.positionalParametersDict = positionalParametersDict


        # -------------------------------------
        # - read positional paramenters
        # - ...and create functionNameToBeCalled as:
        # -   upperCase(pri_sec)
        # -------------------------------------
    posParser      = Ln.createParser(gVar)        # creazione di un parser ad hoc per passarglielo..
    positionalParm = Ln.positionalParameters(posParser, nPosizARGS, positionalParametersDict)
    posFuncToCall  = '_'.join(positionalParm).upper()                       # function: PRI_SEC
    if   not posFuncToCall: posFuncToCall = 'programOptions' # option del programma



    # ====================================================
    # = OPTIONAL PARAMETERs
    # ====================================================
        # -----------------------------------
        # - for the optional parameters
        # - create ad-hoc PARSER
        # -----------------------------------
    myParser = Ln.createParser(gVar)



        # ----------------------------------------------------------
        # - search functionNameToBeCalled
        # - in current module
        # - and in Prj package
        # ----------------------------------------------------------
    this_mod = sys.modules[__name__]
    if   hasattr(this_mod,  posFuncToCall):     getattr(this_mod, posFuncToCall)(myParser)
    elif hasattr(Prj,       posFuncToCall):     getattr(Prj,      posFuncToCall)(myParser)
    else:
        errMsg = '[{0}] - Command not yet implemented!'.format(posFuncToCall)
        Ln.Exit(1, errMsg)


        # ----------------------------------
        # - DEFAULT optional parameters
        # - valid for all projects
        # ----------------------------------
    defaultIniFile = str(Path(programDir , 'conf', prjName + '.ini'))
    defaultLogFile = Path(programDir , 'log', prjName + strftime('_%Y-%m-%d') + '.log')

    Ln.iniFileOptions(myParser, defaultIniFile)
    Ln.logOptions(myParser, defaultLogFile)
    Ln.debugOptions(myParser)


        # ===========================================================
        # = lancio del parser... per i restanti parametri opzionali
        # ===========================================================
    args = vars(myParser.parse_args(sys.argv[nPosizARGS+1:]))


        # ----------------------------------------------
        # - creazione entry per i parametri posizionali
        # ----------------------------------------------
    if nPosizARGS > 0: args['firstPosParameter']  = positionalParm[0]
    if nPosizARGS > 1: args['secondPosParameter'] = positionalParm[1]



        # --------------------------------------------
        # - verifica della congruenza di alcuni parametri:
        # - --log=False azzera anche il --log-filename]
        # --------------------------------------------
    if args['log'] == False: args['log_filename'] = None


        # ----------------------------------------
        # - cancellazione delle option di comodo
        # -    containing -->   'options '
        # ----------------------------------------
    keysToBeDeleted = []
    for key, val in args.items():
        if 'options ' in key:
            keysToBeDeleted.append(key)

    for key in keysToBeDeleted:
        if args['debug']: print ('.... deleting ', key)
        del args[key]


        # ----------------------------------------
        # - ... e print dei parametri
        # ----------------------------------------
    if args['parameters']:
        print()
        for key, val in args.items():
            print('     {0:<20}: {1}'.format(key, val))
        print()
        choice = input('press Enter to continue... (q|x to exit): ')
        if choice.lower() in ('x', 'q'): sys.exit()

    return  args
    Ln.Exit(9999)


