#!/usr/bin/python -O
# -*- coding: iso-8859-15 -*-
# -O Optimize e non scrive il __debug__
#
# Version 0.01 08/04/2010:  Starting
# ####################################################################################################################
import sys, os
import logging


# ---- Note riguardo lo STACK Trace ----
# ---- http://blog.dscpl.com.au/2015/03/generating-full-stack-traces-for.html
import inspect
    # ========================================================
    # - SetUp del log
    # ========================================================
def setLogger(gv, logFile=None, pkgName=None):

        # ------------------------------------------------
        # - del packageHier cerchiamo di prendere
        # - solo gli ultimi due qualificatori.
        # ------------------------------------------------
    print ('\n'*3)
    print(pkgName)
    pkgName = ''

    if not pkgName:
        level = 0
        caller      = inspect.stack()[level]
        programFile = caller[1]     # full name
        lineNumber  = caller[2]
        funcName    = caller[3]
        lineCode    = caller[4]

        fname       = os.path.basename(programFile).split('.')[0]
        str = "[%s-%s:%d]" % (fname, caller[3], int (caller[2]) )
        str = "[%s.%s:%s]" % (fname, funcName, lineNumber)

    print ('{0:<10}: {1}'.format('caller', caller))
    print ('{0:<10}: {1}'.format('fname', fname))
    print (str)
    print ('\n'*3)


    # sys.exit()

    packageHier = pkgName.split('.')
    loggerName  = ('.'.join(packageHier[-2:]))

    if logFile:
        try:
            logging.config.fileConfig(logFile, disable_existing_loggers=False)
        except Exception as why:
            gv.LN.sys.exit(gv, 2001, "{} - ERROR in file: {}".format(str(why), logFile), console=True)

        logger = logging.getLogger(loggerName)
        savedLevel = logger.getEffectiveLevel()
        logger.setLevel(logging.INFO)
        for i in range(1,10):   logger.info(' ')
        for i in range(1,5):    logger.info('-'*40 + 'Start LOGging' + '-'*20)
        logger.setLevel(savedLevel)
        logFileName = logging.getLoggerClass().root.handlers[0].baseFilename
        return logFileName

    logger = logging.getLogger(loggerName)
    return logger
