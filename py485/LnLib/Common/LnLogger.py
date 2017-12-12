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

USE_CONTEXT_FILTER = True
GLOBAL_MYVAR = 'LnFunction'

##############################################
# - http://stackoverflow.com/questions/16203908/how-to-input-variables-in-logger-formatter
# - https://opensource.com/article/17/9/python-logging
##############################################
class ContextFilter(logging.Filter):
    """
    This is a filter which injects contextual information into the log.
    """
    # def __init__(self):
    #     self._line  = None
    #     self._stack = 5    # default

    # def setLineNO(self, number):
    #     self._line = number

    # def setStack(self, number):
    #     self._stack = number

    def filter(self, record):
        # global GLOBAL_MYVAR
        # if self._line:
        #     record.lineno = self._line
        # else:
        #     # record.name   = getframe(stack).f_code.co_name
        #     record.lineno = getframe(self._stack).f_lineno

        record.MYVAR = GLOBAL_MYVAR

        return True




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

    logFormatter = logging.Formatter('[%(asctime)s] [%(funcName)-20s:%(lineno)4d] %(levelname)-5.5s - %(message)s','%m-%d %H:%M:%S')


    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)




        # log to file
    if toFILE:
        LOG_DIR = Path(logfilename).parent
        try:
            LOG_DIR.mkdir(parents=True) # se esiste non dare errore dalla versione 3.5
        except (FileExistsError):
            pass

        if fDEBUG: print ('using log file:', logfilename)


        fileHandler = logging.FileHandler('{0}'.format(logfilename))

        if USE_CONTEXT_FILTER:
            logFormatter = logging.Formatter('[%(asctime)s] [%(GLOBAL_MYVAR)-20s:%(lineno)4d] %(levelname)-5.5s - %(message)s','%m-%d %H:%M:%S')
            # fileHandler.addFilter(LnFilter)              # - aggiungiamolo al logger attuale
        else:
            consoleFormatter = logging.Formatter('[%(module)-25s:%(lineno)4d] %(levelname)-5.5s - %(message)s','%m-%d %H:%M:%S')

        fileHandler.setFormatter(logFormatter)
        logger.addHandler(fileHandler)



        # log to the console
    if toCONSOLE:
        consoleHandler = logging.StreamHandler()

        if USE_CONTEXT_FILTER:
            consoleFormatter = logging.Formatter('[%(GLOBAL_MYVAR)-25s:%(lineno)4d] %(levelname)-5.5s - %(message)s','%m-%d %H:%M:%S')
            # consoleHandler.addFilter(LnFilter)              # - aggiungiamolo al logger attuale
        else:
            consoleFormatter = logging.Formatter('[%(module)-25s:%(lineno)4d] %(levelname)-5.5s - %(message)s','%m-%d %H:%M:%S')

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
# InitLogger = init

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

    if USE_CONTEXT_FILTER:
        LnFilter = ContextFilter()           # - creiamo il contextFilter
        logger.addFilter(LnFilter)              # - aggiungiamolo al logger attuale

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




'''


# http://stackoverflow.com/questions/16203908/how-to-input-variables-in-logger-formatter
class _ContextFilter(logging.Filter):
    """
    This is a filter which injects contextual information into the log.
    """
    def __init__(self):
        self._line  = None
        self._stack = 5    # default
        self._myFuncname = funcName    # nome della funzione personalizzato

    def setLineNO(self, number):
        self._line = number

    def setFuncName(self, name):
        self._myFuncname = name

    def setStack(self, number):
        self._stack = number


    def filter(self, record):
        record.LnFuncName = self._myFuncname
        if self._line:
            record.lineno = self._line
        else:
            # record.name   = getframe(stack).f_code.co_name
            record.lineno = getframe(self._stack).f_lineno
        return True





def setFilters(logger, stackLevel):
    funcLineNO      = getframe(stackLevel).f_lineno
    funcName_prev   = getframe(stackLevel).f_code.co_name

        # -----------------------------------------------------------------------------------------
        # - Per quanto riguarda il setLogger, devo intervenire sul numero di riga della funzione
        # - altrimenti scriverebbe quello della presente funzione.
        # - Per fare questo utilizzo l'aggiunta di un filtro passandogli il lineNO corretto
        # - per poi ripristinarlo al default
        # -----------------------------------------------------------------------------------------




        # - creiamo il contextFilter
    LnFilter    = _ContextFilter('Loreto.Func')

        # - aggiungiamolo al logger attuale
    logger.addFilter(LnFilter)

        # - modifichiamo la riga della funzione chiamante
    LnFilter.setLineNO(funcLineNO)

        # ----------------------------------------------------------------------------------
        # - inseriamo la riga con riferimento al chiamante di questa fuznione
        # - nel "...called by" inseriamo il caller-1
        # ----------------------------------------------------------------------------------
    # scriviamo la riga
    logger.info('\n')
    # logger.info('{TARGET}......called by:{CALLER}'.format(TARGET=funcName_prev, CALLER=_GetCaller(stackNum+2)))

    logger.debug('......called by:{CALLER}'.format(CALLER=_GetCaller(stackLevel+2)))

        # --------------------------------------------------------------------------
        # - azzeriamo il lineNO in modo che le prossime chiamate al logger, che
        # - non passano da questa funzione, prendano il lineNO corretto.
        # --------------------------------------------------------------------------
    LnFilter.setLineNO(None)
    LnFilter.setStack(5)            # ho verificato che con 5 sembra andare bene

    return logger
'''