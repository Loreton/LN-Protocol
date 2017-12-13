#!/usr/bin/python3.5
#
# Scope:  Programma per ...........
# updated by Loreto: 24-10-2017 09.10.33
# -----------------------------------------------
from    sys import exit as sysExit, _getframe as getframe
import  logging, time
from    pathlib import Path
import  inspect

myLOGGER    = None
fDEBUG    = False
modulesToLog = []

USE_CONTEXT_FILTER = False




# =============================================
# = Logging
#   %(pathname)s    Full pathname of the source file where the logging call was issued(if available).
#   %(filename)s    Filename portion of pathname.
#   %(module)s      Module (name portion of filename).
#   %(funcName)s    Name of function containing the logging call.
#   %(lineno)d      Source line number where the logging call was issued (if available).
# =============================================
def init(toFILE=False, toCONSOLE=False, logfilename=None, ARGS=None):
    global myLOGGER, modulesToLog, fDEBUG


    if ARGS:
        if 'debug' in ARGS:
            fDEBUG = ARGS['debug']


        # ----------------------------------------------------------------
        # - impostazione relativamente complessa ai moduli...
        # - toCONSOLE & toFILE  non dovrebbero mai essere contemporanei
        # - perché bloccati dal ParseInput
        # - toCONSOLE==[] significa tutti i moduli
        # ----------------------------------------------------------------
    if toCONSOLE==[]:
        modulesToLog = ['!ALL!']
        toCONSOLE = True

    elif toCONSOLE:
        modulesToLog = toCONSOLE # copy before modifying it
        toCONSOLE = True

    elif toFILE==[]:
        modulesToLog = ['!ALL!']
        toFILE = True

    elif toFILE:
        modulesToLog = toFILE   # copy before modifying it
        toFILE = True

    else:
        # modulesToLog = []
        myLOGGER = None
        if fDEBUG: print(__name__, 'no logger has been activated')
        return _setNullLogger()

    if fDEBUG: print(__name__, 'modulesToLog..................', modulesToLog)


        # ------------------
        # set up Logger
        # %(levelname)-5.5s limita a 5 prendendo MAX 5 chars
        # logFormatter = logging.Formatter("%(asctime)s - [%(name)-20.20s:%(lineno)4d] - %(levelname)-5.5s - %(message)s", datefmt='%H:%M:%S')
        # logFormatter = logging.Formatter('[%(asctime)s] [%(module)s:%(funcName)s:%(lineno)d] %(levelname)-5.5s - %(message)s','%m-%d %H:%M:%S')
        # ------------------
    # logFormatter = logging.Formatter('[%(asctime)s] [%(name)-25s:%(lineno)4d] %(levelname)-5.5s - %(message)s','%m-%d %H:%M:%S')
    # logFormatter = logging.Formatter('[%(asctime)s] [%(module)-25s:%(lineno)4d] %(levelname)-5.5s - %(message)s','%m-%d %H:%M:%S')

    FMT = """----CHUNK %(lognum)s----
            LEVEL: %(levelname)s
            NAME:%(name)s
            MESSAGE:%(message)s
            ----CHUNK %(lognum)s----"""

    FMT = """
        [%(asctime)s]
        [%(funcName)-20s:%(lineno)4d]
        %(levelname)-5.5s - %(message)s','%m-%d %H:%M:%S'"""

    # logFormatter = logging.Formatter('[%(asctime)s] [%(funcName)-20s:%(lineno)4d] %(levelname)-5.5s - %(message)s','%m-%d %H:%M:%S')


    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)


    # https://docs.python.org/3/library/logging.html#logging.setLogRecordFactory
    # https://stackoverflow.com/questions/47245446/run-function-after-logging-using-the-logging-module-in-python

    if USE_CONTEXT_FILTER:
        # def record_factory(*args, **kwargs):
        #     record = old_factory(*args, **kwargs)
        #     record.custom_attribute = 0xdecafbad
        #     return record

        old_factory = logging.getLogRecordFactory()

        def record_factory(*args, **kwargs):
            global COUNT
            record = old_factory(*args, **kwargs)
            record.lognum = COUNT
            COUNT += 1
            return record

        logging.setLogRecordFactory(record_factory)

        fileFMT    = '[%(asctime)s] [%(GLOBAL_MYVAR)-20s:%(lineno)4d] %(levelname)-5.5s - %(message)s','%m-%d %H:%M:%S'
        consoleFMT = '[%(module)-25s:%(lineno)4d] %(levelname)-5.5s - %(message)s','%m-%d %H:%M:%S'
        consoleFMT = """----CHUNK %(lognum)s----
                LEVEL: %(levelname)s
                NAME:%(name)s
                MESSAGE:%(message)s
                ----CHUNK %(lognum)s----"""
    else:
        fileFMT     = '[%(asctime)s] [%(GLOBAL_MYVAR)-20s:%(lineno)4d] %(levelname)-5.5s - %(message)s','%m-%d %H:%M:%S'
        consoleFMT = '[%(module)-25s:%(lineno)4d] %(levelname)-5.5s - %(message)s','%m-%d %H:%M:%S'

        # log to file
    if toFILE:
        LOG_DIR = Path(logfilename).parent
        try:
            LOG_DIR.mkdir(parents=True) # se esiste non dare errore dalla versione 3.5
        except (FileExistsError):
            pass

        if fDEBUG: print ('using log file:', logfilename)


        fileHandler   = logging.FileHandler('{0}'.format(logfilename))
        fileFormatter = logging.Formatter(fileFMT)
        fileHandler.setFormatter(fileFormatter)
        logger.addHandler(fileHandler)



        # log to the console
    if toCONSOLE:
        consoleHandler   = logging.StreamHandler()
        consoleFormatter = logging.Formatter(consoleFMT)
        consoleHandler.setFormatter(consoleFormatter)
        logger.addHandler(consoleHandler)




        # - logging dei parametri di input
    logger.info('\n'*3)
    if ARGS:
        logger.info("--------- input ARGS ------- ")
        for key, val in ARGS.items():
            logger.info("{KEY:<20} : {VAL}".format(KEY=key, VAL=val))
        logger.info('--------------------------- ')
    logger.info('\n'*3)

    myLOGGER = logger
    return logger


# ====================================================================================
# - dal package passato come parametro cerchiamo di individuare se la fuzione/modulo
# - è tra quelli da fare il log.
# - Il package mi server per verficare se devo loggare il modulo o meno
# ====================================================================================

def SetLogger(package, stackNum=0):
    global GLOBAL_MYVAR
    if not myLOGGER:
        return _setNullLogger()

    funcName        = getframe(stackNum + 1).f_code.co_name
    funcLineNO      = getframe(stackNum).f_lineno
    funcName_prev    = getframe(stackNum).f_code.co_name

    if funcName == '<module>': funcName = '__main__'


        # - tracciamo la singola funzione oppure modulo oppure libreria od altro

    if '!ALL!' in modulesToLog:
        LOG_LEVEL = logging.DEBUG

    else:
        LOG_LEVEL = None # default
        fullPkg = (package + funcName).lower()
        for moduleStr in modulesToLog:
            if moduleStr.lower() in fullPkg:
                LOG_LEVEL = logging.DEBUG


    if False:
        print(__name__, 'package..................', package)
        print(__name__, 'funcName.................', funcName)
        print(__name__, 'funcName_prev............', funcName_prev)
        print(__name__, 'LOG_LEVEL................', LOG_LEVEL)
        print()


    GLOBAL_MYVAR = funcName + '_ciao'

    if not LOG_LEVEL:
        logger = _setNullLogger()
        return logger


    logger = logging.getLogger(package)
    logger.setLevel(LOG_LEVEL)

    # else:
    # caller = inspect.stack()[stackNum]
    # dummy, programFile, lineNumber, funcName, lineCode, rest = caller
    logger.info('\n')
    logger.info('{TARGET}......called by:{CALLER}'.format(TARGET=funcName_prev, CALLER=_GetCaller(stackNum+2)))


    return logger














##############################################################################
# - logger dummy
##############################################################################
def _setNullLogger(package=None):


        ##############################################################################
        # - classe che mi permette di lavorare nel caso il logger non sia richiesto
        ##############################################################################
    class nullLogger():
        def __init__(self, package=None, stackNum=1):
            pass


        def info(self, data):
            pass
            # self._print(data)

        def debug(self, data):
            pass
            # self._print(data)

        def error(self, data):  pass
        def warning(self, data):  pass


        def _print(self, data, stackNum=2):
            TAB = 4
            data = '{0}{1}'.format(TAB*' ',data)
            caller = inspect.stack()[stackNum]
            dummy, programFile, lineNumber, funcName, lineCode, rest = caller
            if funcName == '<module>': funcName = '__main__'
            str = "[{FUNC:<20}:{LINENO}] - {DATA}".format(FUNC=funcName, LINENO=lineNumber, DATA=data)
            print (str)

    return nullLogger()





###############################################
# Ho scoperto che potrei anche usare la call seguente
# ma non avrei il controllo sullo stackNO.
#   fn, lno, func, sinfo = myLOGGER.findCaller(stack_info=False)
#   print (fn, lno, func, sinfo)
###############################################
def _GetCaller(deepLevel=0, funcName=None):
    try:
        caller  = inspect.stack()[deepLevel]
    except Exception as why:
        return '{0}'.format(why)   # potrebbe essere out of stack ma ritorniamo comunque la stringa

    # print ('..........caller', caller)
    programFile = caller[1]
    lineNumber  = caller[2]
    if not funcName: funcName = caller[3]
    lineCode    = caller[4]
    fname       = (Path(programFile).name).split('.')[0]

    if funcName == '<module>':
        data = "[{0}:{1}]".format(fname, lineNumber)
    else:
        # data = "[{0}:{1}]".format(fname, lineNumber)
        # data = "[{0}:{1}]".format(funcName, lineNumber)
        data = "[{0}.{1}:{2}]".format(fname, funcName, lineNumber)


    return data
