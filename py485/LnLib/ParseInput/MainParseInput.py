#!/usr/bin/python3.5
#
# updated by ...: Loreto Notarantonio
# Version ......: 26-11-2017 12.40.14
# -----------------------------------------------
import      sys
from        pathlib import Path
from        time    import strftime
import      LnLib as Ln; C=Ln.Color()

#######################################################
# ParseInput
#######################################################
def processInput(gVar, prjRoot):

        # ---------------------------------------------------------
        # -   Identifichiamo il nome progetto dal nome directory
        # ---------------------------------------------------------
    if not gVar.projectDir:
        prjDir = Path(sys.argv[0]).resolve().parent
        if prjDir.name.lower() in ['bin',  'source']:
            prjDir = prjDir.parent
        gVar.projectDir = prjDir

    if not gVar.prjName:
        gVar.prjName = gVar.projectDir.name   # nome della dir del programma


        # -------------------------------------
        # - read positional paramenters
        # - ...and create functionNameToBeCalled as:
        # -   upperCase(pri_sec)
        # -------------------------------------
    posParser      = Ln.createParser(gVar)        # creazione di un parser ad hoc per passarglielo..
    positionalParm = Ln.positionalParameters(posParser, gVar.nPosizARGS, gVar.positionalParametersDict)
    posFuncToCall  = '_'.join(positionalParm).upper()                       # function: PRI_SEC
    if not posFuncToCall:
            posFuncToCall = 'programOptions' # option del programma



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
    # this_mod = sys.modules[__name__]
    # if   hasattr(this_mod,  posFuncToCall):     getattr(this_mod, posFuncToCall)(myParser)
    if hasattr(prjRoot, posFuncToCall):
        getattr(prjRoot,  posFuncToCall)(myParser)
    else:
        errMsg = '[{0}] - Command not yet implemented!'.format(posFuncToCall)
        Ln.Exit(1, errMsg)


        # ----------------------------------
        # - DEFAULT optional parameters
        # - valid for all projects
        # ----------------------------------
    defaultIniFile = str(Path(gVar.projectDir , 'conf', gVar.prjName + '.ini'))
    defaultLogFile = Path(gVar.projectDir , 'log', gVar.prjName + strftime('_%Y-%m-%d') + '.log')

    Ln.iniFileOptions(myParser, defaultIniFile)
    Ln.logOptions(myParser, defaultLogFile)
    Ln.debugOptions(myParser)


        # ===========================================================
        # = lancio del parser... per i restanti parametri opzionali
        # ===========================================================
    args = vars(myParser.parse_args(sys.argv[gVar.nPosizARGS+1:]))


        # ----------------------------------------------
        # - creazione entry per i parametri posizionali
        # ----------------------------------------------
    if gVar.nPosizARGS > 0: args['firstPosParameter']  = positionalParm[0]
    if gVar.nPosizARGS > 1: args['secondPosParameter'] = positionalParm[1]



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

    return args