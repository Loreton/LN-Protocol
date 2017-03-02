#!/usr/bin/python3.4
# -*- coding: iso-8859-15 -*-
#
#!/usr/bin/python -O
# -O Optimize e non scrive il __debug__
#
# ####################################################################################################################
import sys

from ..LnCommon.LnLogger import SetLogger
from ..LnCommon.LnColor  import LnColor
# from ..LnCommon.Exit     import Exit

##########################################################
# - timeout solo dalla Versione 3.3
#   searchLoc = [this_mod, gv.Ln, gv.Prj]:
##########################################################
def GetFunctionPtr(funcName, searchLoc):
    logger  = SetLogger(package=__name__)
    C       = LnColor()

    logger.debug('searching fo funcName: {0}:'.format(funcName))
    funcToCall = None
    for where in searchLoc:
        try:
            funcToCall = getattr(where, funcName)
            logger.debug('found: {0}:'.format(funcToCall))
        except:
            pass

    if not funcToCall:
        for where in [globals, locals]:
            try:
                # result = globals()[funcName](**parameters)
                funcToCall = where()[funcName]
                logger.debug('found: {0}:'.format(funcToCall))
            except:
                pass

    if not funcToCall:
        logger.error('[{0}] - Function not found!'.format(funcName))

    return funcToCall