import sys
# import Source as Prj
import LnLib as Ln; C=Ln.Color()
import  argparse

# from LnLib.Common.Exit      import Exit     as LnExit
# from LnLib.Common.LnColor   import LnColor; C=LnColor()
from . Common.MyHelp               import myHELP
from . Common.CreateParser         import createParser
# from . Main_OneTwoParseInput       import positionalParameters
# from . Main_OneTwoParseInput       import createParser


#######################################################
# PROGRAM POSITIONAL parameters
#    passedData                          = LnClass()
#    passedData.posizARGS                = posizARGS
#    passedData.prjName                  = 'LnRS485'
#    passedData.prgVersion               = 'V1.0.0'
#    passedData.positionalParametersDict = {}
#######################################################
# def positionalParameters(positionalParametersDict, nARGS=0, textMsg='commands'):
def positionalParameters(passedData):  # LnClass() type
    global posizARGS
    posizARGS                = passedData.posizARGS
    positionalParametersDict = passedData.positionalParametersDict

    if posizARGS < 1 or posizARGS > 2: return []

    if len(sys.argv) == 1: sys.argv.append('-h')
    cmdList = []
        # ----------------------------------------------
        # - praparazione del display dei parametri...
        # ----------------------------------------------
    if posizARGS == 1:
        cmdList.append(C.getColored(color=C.magentaH, text='\n      Primary MANDATORY Parameters... enter one of them'))
        for key, val in positionalParametersDict.items():
            keyColor = C.getColored(color=C.yellowH, text=key)
            valColor = C.getColored(color=C.yellow, text=val)
            cmdList.append('\n')
            cmdList.append('          {0:<20} : {1}'.format(key, valColor))

    elif posizARGS == 2:
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

    else:
        return []


        # -----------------------------------
        # - creazione di un parser ad hoc
        # -----------------------------------
    paramName = 'priSecCommand'
    myParser = createParser(passedData)
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
