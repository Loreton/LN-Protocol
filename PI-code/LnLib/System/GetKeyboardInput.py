#!/usr/bin/python -O
# -*- coding: iso-8859-15 -*-
# -O Optimize e non scrive il __debug__
#
# Version 0.01 08/04/2010:  Starting
# ####################################################################################################################
import sys, os
import inspect

from ..LnCommon.LnLogger import SetLogger
from ..LnCommon.LnColor  import LnColor
from ..LnCommon.Exit     import Exit

# ###########################################################################
# * Gestione input da Keyboard.
# * 29-08-2010 - Rimosso LnSys dalla chiamata alla LnSys.exit()
# * 12-02-2012 - Cambiato keys in keyLIST
# * 12-03-2013 - Cambiato keyLIST in validKeys
# * 01-01-2014 - modificato il validKeysLIST.
# ###########################################################################
def getKeyboardInput(msg, validKeys='ENTER', exitKey='X', deepLevel=1, keySep="|", fDEBUG=False):
    logger = SetLogger(package=__name__)
    C       = LnColor()
    exitKeyUPP = exitKey.upper()

    if keySep in validKeys:
        validKeyLIST = validKeys.split(keySep)
    else:
        validKeyLIST = validKeys

    if keySep in exitKeyUPP:
        exitKeyLIST = exitKeyUPP.split(keySep)
    else:
        exitKeyLIST = [exitKeyUPP]

    print()
    if " uscita temporanea" in msg.lower():
        if not 'ENTER' in exitKeyLIST: exitKeyLIST.append('ENTER')
        fDEBUG  =   True

    if fDEBUG:
        funcName = __name__.split('.')[-1]
        C.printCyan(" {0} - exitKeyLIST....: {1}".format(funcName, exitKeyLIST), tab=4)
        C.printCyan(" {0} - validKeyLIST...: {1}".format(funcName, validKeyLIST), tab=4)
        print()
        caller = _calledBy(deepLevel)
        msg = "<{CALLER}> - [{MSG} - ({VALKEY})] ({EXITKEY} to exit) ==> ".format(CALLER=caller, MSG=msg, VALKEY=validKeys, EXITKEY=exitKey)
    else:
        msg = "{0} [{1}] - ({2} to exit) ==> ".format(msg, validKeys, exitKey)

    try:
        while True:
            choice      = input(msg).strip()    # non mi accetta il colore
            choiceUPP   = choice.upper()
            if fDEBUG: C.printCyan("choice: [{0}]".format(choice))

            if choice == '':    # diamo priorità alla exit
                if "ENTER" in exitKeyLIST:
                    sys.exit()
                elif "ENTER" in validKeys:
                    return ''
                else:
                    C.printCyan('\n... please enter something\n')

            elif choiceUPP in exitKeyLIST:
                Exit(9998, "Exiting on user request new.", printStack=True)

            elif choice in validKeyLIST:
                break

            else:
                C.printCyan('\n... try again\n')

    except Exception as why:
        Exit(8, "Error running program [{ME}]\n\n ....{WHY}\n".format(ME=sys.argv[0], WHY=why) )

    return choice

###############################################
#
###############################################
def _calledBy(deepLevel=0):

    try:
        caller = inspect.stack()[deepLevel + 1]

    except Exception as why:
        return '{0}'.format(why)
        return 'Unknown - {0}'.format(why)

    programFile = caller[1]
    lineNumber  = caller[2]
    funcName    = caller[3]
    lineCode    = caller[4]

    fname       = os.path.basename(programFile).split('.')[0]
    str = "[{0}-{1}:{2}]".format(fname, caller[3], int (caller[2]) )
    if funcName == '<module>':
        str = "[{0}:{1}]".format(fname, lineNumber)
    else:
        str = "[{0}.{1}:{2}]".format(fname, funcName, lineNumber)
    return str