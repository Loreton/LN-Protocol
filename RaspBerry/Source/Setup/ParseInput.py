#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import sys
import os
import argparse
import collections
# mi serve per poi cercare i metodi dentro
this_mod = sys.modules[__name__]


#############################################################
# - parseInput()
#############################################################
def ParseInput(gVars, args, programVersion=None):
    global C,  gv
    gv = gVars

    C = gv.Ln.LnColor()
    if not programVersion: programVersion = 'unknown'

     # definizioni per mantenere insalterato l'ordine
    positionalActionsDict  =  {
        'edit': {
            'conf'    : "edit configuration file"
            },

        # 'serial': {
        #     'raw'        : "read RAW data from serial Port and display it",
        #     'rs485'      : "read/send data from USB data formatted LnRs485-bus",
        #     'read'       : "read data from serial Port and display it",
        #     'send'       : "send data from serial Port",
        #     },

        'send': {
            'raw'        : "send RAW data from serial Port and display it",
            'rs485'      : "send LnRs485 formatted data from USB data",
            },

        'monitor': {
            'raw'        : "read RAW data from serial Port and display it",
            'rs485'      : "read LnRs485 formatted data from USB data",
            },

        'master': {
            'raw'        : "read RAW data from serial Port and display it",
            'rs485'      : "diventa master per un bus rs485 appoggiandosi ad un arduino-relay rs485 ",
            'echo'       : "invia dati su arduino-relay il quale fa echo del messaggio verso pi e lo inoltra nel bus RS485 ",
            },

        # 'virtualwire': {
        #     'monitor'      : ".....",
        #     },
        }



        # se non ci sono parametri... forziamo l'help
    if len(sys.argv) == 1: sys.argv.append('-h')

    mainArgs   = prepareArgParse(positionalActionsDict, programVersion)
    InputPARAM = commonParsing(mainArgs.mainCommand)

    InputPARAM.mainCommand    = mainArgs.mainCommand
    InputPARAM.actionCommand = '.'.join(mainArgs.mainCommand)

        # ---------------------------------
        # setting della parte di logging
        # logMODULE  contiene la lista dei moduli da tracciare
        # logCONSOLE True/False
        # LOGGER     True/False
        # ---------------------------------
    InputPARAM.LOGGER  = False
        # - copiamo i moduli in logMODULE
    if not InputPARAM.logCONSOLE == False: # potrebbe essere [] oppure ['xxx', 'yyyy']
        InputPARAM.logMODULE    = InputPARAM.logCONSOLE[:]
        InputPARAM.LOGGER       = True
        InputPARAM.logCONSOLE   = True

    elif not InputPARAM.logMODULE == False: # potrebbe essere [] oppure ['xxx', 'yyyy']
        InputPARAM.LOGGER       = True
        InputPARAM.logCONSOLE   = False


    print ()



        # -----------------------------------------------------
        # - convert  InputPARAM (argparse.Namespace) in dict
        # -----------------------------------------------------
    myDict = {}
    for key, val in vars(InputPARAM).items():
        myDict[key] = val

            # -----------------------------------------
            # - Controlli
            # -----------------------------------------
    if InputPARAM.fDisplayParam:
        C.printYellow('.'*10 + __name__ + '.'*10, tab=4)
        dictID = vars(InputPARAM)
        for key, val in sorted(dictID.items()):
            TYPE = '(' + str(type(val)).split("'")[1] + ')'
            C.printCyan('{0:<20} : {1:<6} - {2}'.format(key, TYPE, val), tab = 8)


        C.printYellow('.'*10 + __name__ + '.'*10, tab=4)
        print ()

    # sys.exit()
    return myDict



#############################################################
# - prepareArgParse()
#############################################################
def prepareArgParse(positionalActionsDict, programVersion):
    mainHelp    = "default help"
    description = "ServerDiscovery"

    totalCMDLIST = []
    for key, val in positionalActionsDict.items():
        totalCMDLIST.append('\n')
        totalCMDLIST.append('      * {0}'.format(key))
        if isinstance(val, dict):
            for key1, val1 in val.items():
                totalCMDLIST.append('          {0:<15} : {1}'.format(key1, val1))
    cmdLIST = '\n'.join(totalCMDLIST)

    mainHelp="""
        Immettere uno dei seguenti valori/comandi/action:
        (con il parametro -h se si desidera lo specifico help)
                {CMDLIST}\n""".format(CMDLIST=cmdLIST)

    myParser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,     # indicates that description and epilog are already correctly formatted and should not be line-wrapped:
        description=C.getYellow(description),
        usage='',                                          # non voglio lo usage
        epilog=C.getYellow(mainHelp),
        conflict_handler='resolve',
        prefix_chars='-+/',
    )


    myParser.add_argument('--version',
                            action='version',
                            version='{PROG} Version: {VER}'.format(PROG='JBossCMK', VER=programVersion))
                            # version='%(prog)s {VER}'.format(VER=programVersion))


        # -------------------------------------------------------
        # - con nargs viene tornata una lista con nArgs
        # - deve prendere il comando primario e poi il sottocomando
        # -------------------------------------------------------
    # -- mantenimao separati
    # myParser.add_argument('mainCommand',   metavar='mainCommand',   type=str, nargs=1)
    # myParser.add_argument('actionCommand', metavar='actionCommand', type=str, nargs=1)

    # .... oppure uniti.
    # myParser.add_argument('mainCommand',   metavar='mainCommand',   type=checkMainCommand, nargs=1)
    myParser.add_argument('mainCommand',
                metavar=C.getCyanH('primaryCommand & secondaryCommand') + C.getYellow(mainHelp),
                type=str,
                nargs=2,
                help='comando e sottocomando come elencato di seguito.'
                # help='comando e sottocomando come elencato di seguito.' + C.getYellow(mainHelp)
                )

        # ----------------------------------------------------------
        # - lanciamo il parse dei parametri subito dopo quelli posizionali
        # ----------------------------------------------------------
    posizARGS = 2
    mainArgs = myParser.parse_args(sys.argv[1:posizARGS+1])
    primaryCommand   = mainArgs.mainCommand[0]
    secondaryCommand = mainArgs.mainCommand[1]
    # print (type(mainArgs.mainCommand), mainArgs.mainCommand)

        # print dell'HELP per il primaryCommand errato
    if not (primaryCommand in positionalActionsDict.keys()):
        myParser.print_help()
        C.printYellow(".... Unrecognized command [{0}]. Valid values are:".format(primaryCommand), tab=8)
        for positionalParm in positionalActionsDict.keys():
            C.printYellow (positionalParm, tab=16)
        exit(1)

        # print dell'HELP in base al primaryComand passato
    ptr = positionalActionsDict[primaryCommand]
    if not secondaryCommand in ptr.keys():
        print()
        C.printCyan(".... Unrecognized subcommand [{0}]. Valid values for [{1}] command are:".format(secondaryCommand, primaryCommand), tab=8)
        for key, val in ptr.items():
            C.printCyanH ('{0:<20}    : {1}'.format(key, val), tab=16)
        exit(1)

    # print (subCommand)

    return mainArgs


###################################################
# - commonParsing
###################################################
def commonParsing(positionalParm, DESCR='CIAO DESCR'):
    mainCommand, secondaryCommand = positionalParm
    usageMsg = "\n          {COLOR}   {ACTION} {COLRESET}[options]".format(COLOR=C.YEL, ACTION=mainCommand, COLRESET=C.RESET)
    myParser = argparse.ArgumentParser( description='{0} Command'.format(mainCommand),
                                        add_help=True, usage=usageMsg,
                                        # formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                        formatter_class=argparse.RawTextHelpFormatter,
                                        # formatter_class=argparse.RawDescriptionHelpFormatter,
                                        prefix_chars='-+/',
                                        )



        # use dispatch pattern to invoke method with same name
        # ritorna un nameSpace
    funcToCall = '_'.join(positionalParm)  # non so se conviene
    if hasattr(this_mod,  mainCommand.upper()):
        getattr(this_mod, mainCommand.upper())(myParser, secondaryCommand)
    else:
        C.printCyan ("[{MOD} - {CMD}] - Command not yet implemented!".format(MOD=__name__, CMD=mainCommand))
        sys.exit(1)


        # ------------------------------------------------
        # - skip first/action parameter
        # ------------------------------------------------
    args = myParser.parse_args(sys.argv[len(positionalParm)+1:])
    # print (args.compareWithSource)

    return args







# ---------------------------
# - _debugOptions
# ---------------------------
def _debugOptions(myParser, required=False):
    '''
        parser.add_argument('--three',          nargs=3)
        parser.add_argument('--optional',       nargs='?')
        parser.add_argument('--all',            nargs='*')
        parser.add_argument('--one-or-more',    nargs='+')
    '''
    mandatory = C.getMagentaH('is MANDATORY - ') if required else C.getCyanH('is OPTIONAL - ')

    logGroup = myParser.add_mutually_exclusive_group(required=False)  # True indica obbligatorietà di uno del gruppo

        # log debug su file
    DEFAULT = False
    logGroup.add_argument( "--log",
                            required=required,
                            # action="store_true",
                            dest="logMODULE",
                            default=DEFAULT,
                            nargs='*',
                            help=mandatory + C.getYellow("""attivazione log.
            E' possibile indicare una o più stringhe
            per identificare le funzioni che si vogliono inserire nel log.
            Possono essere anche porzioni di funcName separate da ' ' Es: pippo uto ciao
            DEFAULT = {DEF}
    """.format(DEF=DEFAULT)))

        # log debug su console
    logGroup.add_argument( "--log-console",
                            required=required,
                            dest="logCONSOLE",
                            # action="store_true",
                            # choices=['info', 'debug'],
                            default=DEFAULT,
                            nargs='*',
                            help=mandatory + C.getYellow("""attivazione log sulla console.
            E' possibile indicare una o più stringhe
            per identificare le funzioni che si vogliono inserire nel log.
            Possono essere anche porzioni di funcName separate da ' ' Es: pippo uto ciao
            DEFAULT = {DEF}
    """.format(DEF=DEFAULT)))



    myParser.add_argument( "-D", "--debug",
                            required=required,
                            action="store_true",
                            dest="fDEBUG",
                            default=DEFAULT,
                            help=mandatory + C.getYellow("""enter in DEBUG mode..
    [DEFAULT: {DEF}]
    """.format(DEF=DEFAULT)))

    myParser.add_argument( "--elapsed",
                            required=required,
                            action="store_true",
                            dest="fELAPSED",
                            default=DEFAULT,
                            help=mandatory + C.getYellow("""display del tempo necessario al processo..
    [DEFAULT: {DEF}]
    """.format(DEF=DEFAULT)))


    myParser.add_argument( "--parameters",
                            required=required,
                            action="store_true",
                            dest="fDisplayParam",
                            default=DEFAULT,
                            help=mandatory + C.getYellow("""display del tempo necessario al processo..
    [DEFAULT: {DEF}]
    """.format(DEF=DEFAULT)))







# ---------------------------
# - A C T I O N s
# ---------------------------
def EDIT(myParser, action):
    _debugOptions(myParser)

    myEditor = (os.environ.get('EDITOR'))
    if not myEditor:
        if 'editor' in gv.ini.MAIN:
            myEditor = gv.ini.MAIN.editor
        else:
            myEditor = 'wordpad.exe'

    if action == 'conf':
        command = [
                    myEditor,
                    gv.Prj.iniFileName
                    ]

        print ('running command:', command)
        rCode = os.system(' '.join(command))

        C.printCyan('[{MOD} - configuration file can be edited [RCODE: {RCODE}]'.format(MOD=__name__, RCODE=rCode), tab=4)
        sys.exit()

    else:
        C.printCyan('[{MOD} - Action [{ACTION}] non prevista per il comando di edit...'.format(MOD=__name__, ACTION=action), tab=4)

    myParser.print_help()


# ---------------------------
# - A C T I O N s
# ---------------------------
def RS485(myParser, action):
    from . import ParseInput_RS485 as rs485

    rs485.SetGlobals(C, gv.Ln)
    rs485.ExecuteOptions(myParser, required=False)

    # print ('....', action.lower())
    if action.lower() in ['monitor']:
        rs485.SerialPort(myParser, required=True)


    elif action.lower() in ['send']:
        rs485.SerialPort(myParser, required=True)
        rs485.Rs485Address(myParser, required=True)
        pass


    else:
        print("""
            Action: [{0}] non prevista.
            valori previsti sono:
            """.format(action)
            )
        sys.exit()

    _debugOptions(myParser)


# ---------------------------
# - A C T I O N s
# ---------------------------
def SERIAL(myParser, action):
    from . import ParseInput_RS485 as rs485

    rs485.SetGlobals(C, gv.Ln)
    rs485.ExecuteOptions(myParser, required=False)

    if action.lower() in ['read']:
        rs485.SerialPort(myParser, required=True)
        rs485.DataProtocol(myParser, required=True)
        rs485.DisplayDataFormat(myParser, required=False)


    elif action.lower() in ['send']:
        rs485.SerialPort(myParser, required=True)
        rs485.DataProtocol(myParser, required=True)
        rs485.Rs485Address(myParser, required=True)



    else:
        print("""
            Action: [{0}] non prevista.
            valori previsti sono:
            """.format(action)
            )
        sys.exit()

    _debugOptions(myParser)




# ---------------------------
# - A C T I O N s
# ---------------------------
def MASTER(myParser, action):
    from . import ParseInput_RS485 as rs485

    rs485.SetGlobals(C, gv.Ln)
    rs485.ExecuteOptions(myParser, required=False)

    if action.lower() in ['rs485']:
        rs485.SerialPort(myParser, required=True)
        # rs485.Rs485Address(myParser, required=True)

    elif action.lower() in ['echo']:
        rs485.SerialPort(myParser, required=True)

    else:
        print("""
            Action: [{0}] non prevista.
            valori previsti sono:
            """.format(action)
            )
        sys.exit()

    _debugOptions(myParser)


# ---------------------------
# - A C T I O N s
# ---------------------------
def SEND(myParser, action):
    from . import ParseInput_RS485 as rs485

    rs485.SetGlobals(C, gv.Ln)
    rs485.ExecuteOptions(myParser, required=False)

    if action.lower() in ['raw']:
        rs485.SerialPort(myParser, required=True)


    elif action.lower() in ['rs485']:
        rs485.SerialPort(myParser, required=True)
        rs485.Rs485Address(myParser, required=True)

    else:
        print("""
            Action: [{0}] non prevista.
            valori previsti sono:
            """.format(action)
            )
        sys.exit()

    _debugOptions(myParser)



# ---------------------------
# - A C T I O N s
# ---------------------------
def MONITOR(myParser, action):
    from . import ParseInput_RS485 as rs485

    rs485.SetGlobals(C, gv.Ln)
    rs485.ExecuteOptions(myParser, required=False)

    if action.lower() in ['raw']:
        rs485.SerialPort(myParser, required=True)
        rs485.DisplayDataFormat(myParser, required=False)


    elif action.lower() in ['rs485']:
        rs485.SerialPort(myParser, required=True)
        # rs485.DisplayDataFormat(myParser, required=False)



    else:
        print("""
            Action: [{0}] non prevista.
            valori previsti sono:
            """.format(action)
            )
        sys.exit()

    _debugOptions(myParser)



