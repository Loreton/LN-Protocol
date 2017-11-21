import sys
# import Source as Prj
import LnLib as Ln
import  argparse

# from LnLib.Common.Exit      import Exit     as LnExit
# from LnLib.Common.LnColor   import LnColor; C=LnColor()
C=Ln.Color()
#######################################################
# PROGRAM POSITIONAL parameters
#######################################################
def positionalParameters(myParser, paramName):
    global posizARGS

    posizARGS = 2
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




        # ----------------------------------------------
        # - praparazione del display dei parametri...
        # ----------------------------------------------
    cmdList = []
    cmdList.append(C.getColored(color=C.magentaH, text='\n      Primary MANDATORY Parameters... enter a couple of them'))
    for key, val in positionalParametersDict.items():
        cmdList.append('\n')
        cmdList.append('      * {0}'.format(key))
        if isinstance(val, dict):
            for key1, val1 in val.items():
                valColor = C.getColored(color=C.yellow, text=val1)
                cmdList.append('          {0:<15} : {1}'.format(key1, valColor))
    cmdList = '\n'.join(cmdList)
    metavarStr  = C.getColored(color=C.cyanH, text='primaryCommand & secondaryCommand\n')
    helpStr = 'comando e sottocomando come elencato di seguito.'



        # ----------------------------------------------
        # - praparazione del display dei parametri...
        # ----------------------------------------------
    myParser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,     # indicates that description and epilog are already correctly formatted and should not be line-wrapped:
        description=C.getColored(color=C.yellow, text="RS485 command"),
        usage='',                                          # non voglio lo usage
        epilog=C.getColored(color=C.yellow, text="default help"),
        conflict_handler='resolve',
    )

        # -------------------------------------------------------
        # - verifichiamo che l'imput dei parametri posizionali sia corretto
        # - con nargs viene tornata una lista con nArgs
        # - deve prendere il comando primario e poi il sottocomando
        # -------------------------------------------------------
    myParser.add_argument(paramName,
                metavar=''.join(cmdList),
                type=str,
                nargs=posizARGS,
                help='')



        # ----------------------------------------------------------
        # - lanciamo il parse dei parametri subito dopo quelli posizionali
        # ----------------------------------------------------------
    mainArgs   = myParser.parse_args(sys.argv[1:posizARGS+1])
    myPosParam = vars(mainArgs)[paramName]

    checkPositionaParam(myParser, myPosParam, positionalParametersDict)
    # ritorno i valori in una list
    return myPosParam

####################################
# # _checkPositionaParam()
####################################
def checkPositionaParam(myParser, posParam, positionalParametersDict):

    primaryCommand   = posParam[0]
    if not (primaryCommand in positionalParametersDict.keys()):
        myParser.print_help()
        C.printColored(color=C.yellow, text=".... Unrecognized command [{0}]. Valid values are:".format(primaryCommand), tab=8)
        for positionalParm in positionalParametersDict.keys():
            C.printColored(color=C.yellow, text=positionalParm, tab=16)
        print()
        exit(1)

    if posizARGS == 2:
        ptr = positionalParametersDict[primaryCommand]
        secondaryCommand = posParam[1]
        if not secondaryCommand in ptr.keys():
            myParser.print_help()
            print()
            C.printColored(color=C.cyan, text=".... Unrecognized subcommand [{0}]. Valid values for '{1}' primary command are:".format(secondaryCommand, primaryCommand), tab=8)
            for key, val in ptr.items():
                C.printColored(color=C.cyan, text='{0:<20}    : {1}'.format(key, val), tab=16)
            print()
            exit(1)
