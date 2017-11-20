#!/usr/bin/python3.5
#
# updated by ...: Loreto Notarantonio
# Version ......: 20-11-2017 17.16.08
# -----------------------------------------------
import  sys
from    pathlib import Path
from    time import  strftime
import  argparse

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




#######################################################
# ParseInput
#######################################################
def ParseInput(programVersion=0.1):
    gVar = LnClass()

        # ---------------------------------------------------------
        # -   Identifichiamo il nome progetto dal nome directory
        # -   oppure passiamolo come parametro....
        # ---------------------------------------------------------
    programDir     = Path(sys.argv[0]).resolve().parent
    if programDir.name.lower() in ['bin',  'source']:
        programDir = programDir.parent

    prjName        = programDir.name   # nome della dir del programma

        # --------------------------
        # -   DEFAULT args VALUEs
        # --------------------------
    gVar.defaultLogFile    = Path(programDir , 'log', prjName + strftime('_%Y-%m-%d') + '.log')
    gVar.defaultConfigFile = Path(programDir , 'conf', prjName + '.ini')
    gVar.defaultRootDir    = programDir


        # --------------------------
        # -   MAIN HELP message
        # --------------------------
    mainHelp=""
    myParser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,     # indicates that description and epilog are already correctly formatted and should not be line-wrapped:
        description='Ln-Rs485 protocol',
        usage='',                                          # non voglio lo usage
        epilog=mainHelp,
        conflict_handler='resolve',
    )


        # configurazione Args ..
    myParser.add_argument('--version',
                            action='version',
                            version='{PROG}  Version: {VER}'.format (PROG=prjName, VER=programVersion ),
                            help=myHELP("show program's version number and exit") )


    # - Se abbiamo dei parametri posizionali allora inseriamo il modulo...
    posParameters=1
    if posParameters:
        from . PositionalParameters     import positionalParameters
        posParamName='mainCommand'
        if len(sys.argv) == 1: sys.argv.append('-h')
        positionalParameters(myParser, paramName=posParamName)

    programParameters(myParser, gVar)
    logParameters(myParser, gVar)
    debugParameters(myParser)




        # lancio del parser...
    args = vars(myParser.parse_args())


        # --------------------------------------------
        # - verifica della congruenza di alcuni parametri:
        # - --log=False azzera anche il --log-filename]
        # --------------------------------------------
    # se ho un solo parametro posizionale... eliminialo la LIST
    if posParameters == 1:
        args[posParamName] = args[posParamName][0]

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

    return  args














# ELAPSED
'''
    myParser.add_argument( "--elapsed",
                            required=False,
                            action="store_true",
                            dest="fELAPSED",
                            default=False,
                            help=LnColor.getYellow("""display del tempo necessario al processo..
    [DEFAULT: False]
    """))

    gv.Time.processServices.end = time.time()

    gv.Time.Main.end = time.time()

    if gv.INPUT_PARAM.fELAPSED:
        print ()
        C.printYellow (' read ini file    : {0}'.format(gv.Time.readIniFile.end         - gv.Time.readIniFile.start))
        C.printYellow (' process ini file : {0}'.format(gv.Time.processIniFile.end      - gv.Time.processIniFile.start))
        C.printYellow (' get instances    : {0}'.format(gv.Time.getInstances.end        - gv.Time.getInstances.start))
        C.printYellow (' process services : {0}'.format(gv.Time.processServices.end     - gv.Time.processServices.start))
        print ()
        C.printYellow (' total job tooks  : {0}'.format(gv.Time.Main.end                - gv.Time.Main.start))
        print ()

'''
