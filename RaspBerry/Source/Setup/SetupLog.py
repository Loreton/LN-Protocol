#!/opt/python3.4/bin/python3.4

#!/usr/bin/python3.4
import getpass
import os, sys

__author__  = 'Loreto Notarantonio'
__version__ = 'LnVer_2017-08-14_11.39.41'

# #########################################################
# - SetUp del log
# #########################################################
def SetupLog(gv):
    # gv.PrintTree()
    if gv.inputParam.LOGGER:
        cPrint       = gv.Ln.LnColor()

        logFileName         = '/tmp/{PREFIX}_{USER}.log'.format(PREFIX=gv.env.prefix, USER=getpass.getuser())
        logConfigFileName   = os.path.normpath('{CONFDIR}/LoggerConfig.ini'.format(CONFDIR=gv.env.mainConfigDIR))

        if gv.fDEBUG:
            cPrint.Yellow('.'*10 + __name__ + '.'*10, tab=4)
            cPrint.Cyan('logFileName       {0}'.format(os.path.abspath(logFileName)), tab=8)
            cPrint.Cyan('logConfigFileName {0}'.format(logConfigFileName), tab=8)
            cPrint.Yellow('.'*10 + __name__ + '.'*10, tab=4)
            print ()
            # sys.exit()


        if os.path.isfile(logConfigFileName):
            gv.Ln.InitLogger(   iniLogFile=logConfigFileName,
                                logFileName=logFileName,
                                package=gv.env.name,
                                LOGGER=gv.inputParam.LOGGER,
                                logCONSOLE=gv.inputParam.logCONSOLE,
                                logMODULE=gv.inputParam.logMODULE,
                                packageQualifiers=8
                            )

            logger = gv.Ln.SetLogger(package="Main")
        else:
            errMsg = 'il file {0} non esiste..'.format(logConfigFileName)
            gv.Ln.Exit(1, errMsg)
    else:
        logger = gv.Ln.SetLogger(package="Main")


    return logger



