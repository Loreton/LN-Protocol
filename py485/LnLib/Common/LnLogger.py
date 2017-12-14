#!/usr/bin/python3.5
#
# Scope:  Programma per ...........
# updated by Loreto: 24-10-2017 09.10.33
# -----------------------------------------------
import  sys
import  logging, time
from    pathlib import Path
import  inspect

myLOGGER   = None
fDEBUG    = False
# modulesToLog = []



###########################################################
# permette di iniettare campi custom nel log-Record
###########################################################
def setMyLogRecord(myFuncName='nameNotPassed', lineNO=0):
    old_factory = logging.getLogRecordFactory()
    def record_factory(*args, **kwargs):
        record = old_factory(*args, **kwargs)
        record.LnFuncName = myFuncName
        # record.LnLineNO   = lineNO   # non posso altrimenti rimane sempre lo stesso
        return record
    logging.setLogRecordFactory(record_factory)



def prepareLogEnv(toFILE=False, toCONSOLE=False, logfilename=None, ARGS=None):
    ''' ----------------------------------------------------------------
         impostazione relativamente complessa ai moduli...
         toCONSOLE & toFILE  non dovrebbero mai essere contemporanei
         perché bloccati dal ParseInput
         toCONSOLE==[] significa log di tutti i moduli
         toFILE==[]    significa log di tutti i moduli
        ---------------------------------------------------------------- '''
    global modulesToLog, fDEBUG

    _fLOG, _fCONSOLE, _fFILE = True, False, False


    if ARGS:
        if 'debug' in ARGS:
            fDEBUG = ARGS['debug']

    if toCONSOLE==[]:
        modulesToLog = ['!ALL!']
        _fCONSOLE = True

    elif toCONSOLE:
        modulesToLog = toCONSOLE # copy before modifying it
        _fCONSOLE = True

    elif toFILE==[]:
        modulesToLog = ['!ALL!']
        _fFILE = True

    elif toFILE:
        modulesToLog = toFILE   # copy before modifying it
        _fFILE = True

    else:
        modulesToLog = []
        _fLOG = False
        if fDEBUG: print(__name__, 'no logger has been activated')

    if fDEBUG: print(__name__, 'modulesToLog..................', modulesToLog)

    return _fLOG, _fCONSOLE, _fFILE


# =============================================
# = Logging
#   %(pathname)s    Full pathname of the source file where the logging call was issued(if available).
#   %(filename)s    Filename portion of pathname.
#   %(module)s      Module (name portion of filename).
#   %(funcName)s    Name of function containing the logging call.
#   %(lineno)d      Source line number where the logging call was issued (if available).
# =============================================
def init(toFILE=False, toCONSOLE=False, logfilename=None, ARGS=None):
    global myLOGGER

    _fLOG, _fCONSOLE, _fFILE = prepareLogEnv(toFILE=toFILE, toCONSOLE=toCONSOLE, logfilename=logfilename, ARGS=ARGS)
    if not _fLOG:
        myLOGGER = None
        return _setNullLogger()

        # ------------------
        # set up Logger
        # %(levelname)-5.5s limita a 5 prendendo MAX 5 chars
        # logFormatter = logging.Formatter("%(asctime)s - [%(name)-20.20s:%(lineno)4d] - %(levelname)-5.5s - %(message)s", datefmt='%H:%M:%S')
        # logFormatter = logging.Formatter('[%(asctime)s] [%(module)s:%(funcName)s:%(lineno)d] %(levelname)-5.5s - %(message)s','%m-%d %H:%M:%S')
        # ------------------
    fileFMT    = '[%(asctime)s] [%(LnFuncName)-20s:%(lineno)4d] %(levelname)-5.5s - %(message)s'
    consoleFMT = '[%(LnFuncName)-20s:%(lineno)4d] %(levelname)-5.5s - %(message)s'


    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    setMyLogRecord('Ln-Initialize')


        # log to file
    if _fFILE:
        LOG_FILE_NAME = logfilename
        LOG_DIR = Path(logfilename).parent

            # se esiste non dare errore
        try:
            LOG_DIR.mkdir(parents=True)
        except (FileExistsError):
            pass

        if fDEBUG: print ('using log file:', LOG_FILE_NAME)

        fileHandler     = logging.FileHandler('{0}'.format(LOG_FILE_NAME))
        fileFormatter   = logging.Formatter(fmt=fileFMT, datefmt='%m-%d %H:%M:%S')
        fileHandler.setFormatter(fileFormatter)
        logger.addHandler(fileHandler)

        # log to the console
    if _fCONSOLE:
        consoleHandler  = logging.StreamHandler(stream=sys.stdout)
        consoleFormatter= logging.Formatter(fmt=consoleFMT, datefmt='%m-%d %H:%M:%S')
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
    if not myLOGGER:
        return _setNullLogger()

    # comoda ... ma non ho il controllo sullo stackNO.
    # fn, lno, func, sinfo = myLOGGER.findCaller(stack_info=False)
    # print (fn, lno, func, sinfo)

    funcName       = sys._getframe(stackNum+1).f_code.co_name
    funcLineNO     = sys._getframe(stackNum+1).f_lineno
    thisFuncName   = sys._getframe(stackNum).f_code.co_name

    if funcName == '<module>': funcName = '__main__'
    caller = '{}.{}({})'.format(package, funcName, funcLineNO)

    _token = package.split('.')
    _LnFuncName = '{FIRST}.{LAST}.{FUNC}'.format(FIRST=_token[0], LAST=_token[-1], FUNC=funcName)

    if len(_LnFuncName) > 19:
        _LnFuncName = '{LAST}.{FUNC}'.format(LAST=_token[-1], FUNC=funcName)
        _LnFuncName = '{FUNC}'.format(FUNC=funcName)


    if False:
        print(__name__, 'package..................', package)
        print(__name__, 'funcName -2..............', sys._getframe(stackNum-2).f_code.co_name, sys._getframe(stackNum-2).f_lineno)
        print(__name__, 'funcName -1..............', sys._getframe(stackNum-1).f_code.co_name, sys._getframe(stackNum-1).f_lineno)
        print(__name__, 'funcName ................', sys._getframe(stackNum).f_code.co_name, sys._getframe(stackNum).f_lineno)
        print(__name__, 'funcName +1..............', sys._getframe(stackNum+1).f_code.co_name, sys._getframe(stackNum+1).f_lineno)
        print(__name__, 'funcName +2..............', sys._getframe(stackNum+2).f_code.co_name, sys._getframe(stackNum+2).f_lineno)
        try:
            print(__name__, 'funcName +3..............', sys._getframe(stackNum+3).f_code.co_name, sys._getframe(stackNum+3).f_lineno)
        except:
            pass
        print(__name__, 'called by..............', _LnFuncName, funcLineNO)
        print()



        # ---------------------------------
        # - individuiamo se è un modulo
        # - da tracciare o meno
        # ---------------------------------
    if '!ALL!' in modulesToLog:
        LOG_LEVEL = logging.DEBUG

    else:
        LOG_LEVEL = None
        fullPkg = (package + funcName).lower()
        for moduleStr in modulesToLog:
            if moduleStr.lower() in fullPkg:
                LOG_LEVEL = logging.DEBUG



    if LOG_LEVEL:
        logger = logging.getLogger(package)
        logger.setLevel(LOG_LEVEL)

        # - set temporaneo dei nomi per scrivere SetLogger come funzione
        setMyLogRecord(myFuncName=thisFuncName)

        logger.info('\n')
        logger.info('......called by: {CALLER}'.format(CALLER=caller))

        # - set nomi del caller
        setMyLogRecord(myFuncName=_LnFuncName)
    else:
        logger = _setNullLogger()

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




'''

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



# http://stackoverflow.com/questions/16203908/how-to-input-variables-in-logger-formatter
class _ContextFilter(logging.Filter):
    """
    This is a filter which injects contextual information into the log.
    """
    def __init__(self):
        self._line  = None
        self._stack = 5    # default

    def setLineNO(self, number):
        self._line = number

    def setStack(self, number):
        self._stack = number

    def filter(self, record):
        if self._line:
            record.lineno = self._line
        else:
            # record.name   = sys._getframe(stack).f_code.co_name
            record.lineno = sys._getframe(self._stack).f_lineno
        return True




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
            # record.name   = sys._getframe(stack).f_code.co_name
            record.lineno = sys._getframe(self._stack).f_lineno
        return True





def setFilters(logger, stackLevel):
    funcLineNO      = sys._getframe(stackLevel).f_lineno
    thisFuncName   = sys._getframe(stackLevel).f_code.co_name

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
    # logger.info('{TARGET}......called by:{CALLER}'.format(TARGET=thisFuncName, CALLER=_GetCaller(stackNum+2)))

    logger.debug('......called by:{CALLER}'.format(CALLER=_GetCaller(stackLevel+2)))

        # --------------------------------------------------------------------------
        # - azzeriamo il lineNO in modo che le prossime chiamate al logger, che
        # - non passano da questa funzione, prendano il lineNO corretto.
        # --------------------------------------------------------------------------
    LnFilter.setLineNO(None)
    LnFilter.setStack(5)            # ho verificato che con 5 sembra andare bene

    return logger
'''