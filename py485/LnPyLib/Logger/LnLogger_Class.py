import sys, os
# from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
import logging
from logging import handlers  # se non lo inserisco da errore sull'handlers
from pathlib import Path
import inspect


class LnClass(): pass

'''
# https://stackoverflow.com/questions/20372669/python-use-the-same-class-instance-in-multiple-modules
def singleton_with_args(*args, **kwargs):
    def wrapper(cls):
        return cls(*args, **kwargs)
    return wrapper


# https://stackoverflow.com/questions/39492471/how-to-extend-the-logger-logging-class
# https://stackoverflow.com/questions/19615876/showing-the-right-funcname-when-wrapping-logger-functionality-in-a-custom-class
@singleton_with_args(0)
'''
class LnLogger(logging.getLoggerClass()):
    ''' LnLogger class '''

        # ----------------------------------------------------------------------------
        # - variabili che saranno condivise da tutti i chiamanti.
        # - inserisco i pointer ed i valori basilari per condividere la classe
        # ----------------------------------------------------------------------------
    loggerNames    = set() # univoco MA... non mantiene l'ordine di iserimento
    Pointers   = LnClass()

    def __init__(   self,
                    name='LnLoggerClass',
                    toFILE=False,
                    toCONSOLE=False,
                    logfilename=None,
                    defaultLogLevel='info',
                    rotationType='time',
                    backupCount=5,
                    maxBytes=20000,
                    when="m",       # m=minutes
                    interval=60,
                    funcname='M+F',
                    ):


        ''' internal variables '''
        self._logEnabled        = False
        self._logLevel             = logging.INFO

        self._name              = name
        self._to_file           = False
        self._to_console        = False
        self._filename          = None
        self._modulesToLog      = []

        self._rotation_type     = rotationType
        self._backup_count      = backupCount
        self._max_bytes         = maxBytes
        self._when_rotate       = when
        self._rotation_interval = interval

        self._file_format       = '[%(asctime)s] [%(LnFuncName)-30s:%(lineno)4d] %(levelname)-5.5s - %(message)s'
        self._console_format    = '[%(LnFuncName)-30s:%(lineno)4d] %(levelname)-5.5s - %(message)s'
        # self._file_format       = '[%(asctime)s] [%(module)-20s:%(lineno)4d] %(levelname)-5.5s - %(message)s'
        # self._console_format    = '[%(module)-20s:%(lineno)4d] %(levelname)-5.5s - %(message)s'
        self._date_time_format  = '%m-%d %H:%M:%S'

        self._realLogger        = logging.getLogger(self._name)
        self._nullLogger        = nullLogger()
        self._LnFilter          = ContextFilter(defaultStack=6, autoReset=True)
        if funcname =='M+F':
            self._LnFilter.setModuleFuncName(True)

        if name not in self.loggerNames:
            self.loggerNames.add(name)
            self._realLogger.setLevel(self._logLevel)
            self._realLogger.addFilter(self._LnFilter)

        self._LnFilter.setFuncName('initializing')

        ''' setting LogLevel '''
        assert type(defaultLogLevel) == str
        if   defaultLogLevel.lower() == 'debug':    self._logLevel = logging.DEBUG
        elif defaultLogLevel.lower() == 'warning':  self._logLevel = logging.WARNING



        ''' setting file/console/logEnable/modulesToLog '''
        self._prepareFileLog(toFILE, logfilename)

        ''' put Console to override file settings '''
        self._prepareConsoleLog(toCONSOLE)

        ''' prepare logfile if required '''
        self._myLogger = self._realLogger
        if self._to_file or self._to_console:
            self._logEnabled = True
        else:
            self._logEnabled = False
            # self._myLogger = self._nullLogger


            # ---------------------------------------------
            # - inseriamo alcuni puntatori per permettere
            # - agli altri di accedere alla stessa istanza
            # - di logger
            # ---------------------------------------------
        self.Pointers.rootName     = self._name
        self.Pointers.ClassInstance = self   # <=== class pointer
        self.Pointers.realLogger   = self._realLogger
        self.Pointers.nullLogger   = self._nullLogger
        self.Pointers.LnFilter     = self._LnFilter
        self.Pointers.modulesToLog = self._modulesToLog
        self.Pointers.logLevel     = self._logLevel

        if False:
            print('pointers.rootName     = ', self.Pointers.rootName)
            print('pointers.ClassInstance  = ', self.Pointers.ClassInstance)
            print('pointers.realLogger   = ', self.Pointers.realLogger)
            print('pointers.nullLogger   = ', self.Pointers.nullLogger)
            print('pointers.LnFilter     = ', self.Pointers.LnFilter)
            print('pointers.modulesToLog = ', self.Pointers.modulesToLog)
            print('pointers.logLevel     = ', self.Pointers.logLevel)

        self._realLogger.setLevel(self._logLevel)
        self.info('initialised.....')
        # self._LnFilter.setFuncName(None) # reset al nome del modulo chiamante





    ##############################################################
    #
    ##############################################################
    def _prepareConsoleLog(self, toCONSOLE):
        ''' provides:
                create consoleHandler
                add consoleHandler to logger
        '''

        if toCONSOLE==False:
            self._to_console = False
            return

        elif toCONSOLE==[]:
            self._to_console = True
            self._modulesToLog = ['!ALL!']

        elif toCONSOLE:
            self._to_console = True
            self._modulesToLog = toCONSOLE


            ''' prepare log to console if required '''
        _consoleFormatter = logging.Formatter(fmt=self._console_format, datefmt=self._date_time_format)
        _consoleHandler   = logging.StreamHandler(stream=sys.stdout)
        _consoleHandler.setFormatter(_consoleFormatter)
        self._realLogger.addHandler(_consoleHandler)





    ##############################################################
    #
    ##############################################################
    def _prepareFileLog(self, toFILE, logfilename):
        ''' provides:
                open file
                set rotation policy
                create fileHandler
                add fileHandlet to logger
        '''

        if toFILE==False:
            self._to_file = False
            return


        if toFILE==[]:
            self._to_file = True
            self._modulesToLog = ['!ALL!']

        elif toFILE:
            self._to_file = True
            self._modulesToLog = toFILE



        _LOG_DIR = Path(logfilename).parent
        self._filename = logfilename

        try:
            _LOG_DIR.mkdir(parents=True)
        except (FileExistsError):           # skip error if exists
            pass

        print ('logFile:', str(self._filename))

        if self._rotation_type == 'time':
            fileHandler = handlers.TimedRotatingFileHandler(
                            str(self._filename),
                            when=self._when_rotate,
                            interval=self._rotation_interval,
                            backupCount=self._backup_count
                        )

        elif self._rotation_type == 'size':
            fileHandler = handlers.RotatingFileHandler(
                            str(self._filename),
                            maxBytes=self._max_bytes,
                            backupCount=self._backup_count
                        )

        else:
            fileHandler = logging.FileHandler(self._filename)

        fileFormatter = logging.Formatter(fmt=self._file_format, datefmt=self._date_time_format)
        fileHandler.setFormatter(fileFormatter)
        self._realLogger.addHandler(fileHandler)




    ##############################################################
    #
    ##############################################################
    @staticmethod
    def static_getMainPointers():
        return LnLogger.Pointers

    def setFilterDefaultStack(self, stackLevel):
        self._LnFilter.setDefaultStack(stackLevel)




    ##############################################################
    #
    ##############################################################
    def info(self, msg, extra=None, dictTitle=None):

        myLogger = self._myLogger.info
        if isinstance(msg, dict):
            savedAutoReset = self._LnFilter.getAutoReset()
            self._LnFilter.setAutoReset(False)    # blocca l'autoreset dello stack
            myLogger('{}: {}'.format(dictTitle, type(msg)))
            for key in msg.keys():
                myLogger('  {:<20}: {}'.format(key, msg[key]))
            self._LnFilter.setAutoReset(savedAutoReset)    # ripristina l'autoreset dello stack
        else:
            self._myLogger.info(msg, extra=extra)
        # self.commonLog(self._myLogger.info, msg, dictTitle=dictTitle)


    def error(self, msg, extra=None, dictTitle=None):
        # self.commonLog(self._myLogger.error, msg, dictTitle=dictTitle)
        if self._logEnabled:
            self._myLogger.error(msg, extra=extra)

    def debug(self, msg, extra=None, dictTitle=None):
        # self.commonLog(self._myLogger.debug, msg, dictTitle=dictTitle)
        if self._logEnabled:
            self._myLogger.debug(msg, extra=extra)

    def warn(self, msg, extra=None, dictTitle=None):
        # self.commonLog(self._myLogger.warn, msg, dictTitle=dictTitle)
        if self._logEnabled:
            self._myLogger.warn(msg, extra=extra)


    def commonLog(self, myLogger, msg, dictTitle='dictionary'):
            # cambio lo stackNum per saltare commonLog ed info/debug/...
        if self._logEnabled:
            self._LnFilter.addStack(1)

                # se è un dictionary stampiamolo come tale ad un livello solo
            if isinstance(msg, dict):
                savedAutoReset = self._LnFilter.getAutoReset()
                self._LnFilter.setAutoReset(False)    # blocca l'autoreset dello stack
                myLogger('{}: {}'.format(dictTitle, type(msg)))
                for key in msg.keys():
                    myLogger('  {:<20}: {}'.format(key, msg[key]))
                self._LnFilter.setAutoReset(savedAutoReset)    # ripristina l'autoreset dello stack

            else:
                myLogger(msg)




##############################################################################
# - classe che mi permette di lavorare nel caso il logger non sia richiesto
##############################################################################
class nullLogger():
    def __init__(self, package=None, stackNum=1, extra=None): pass
    def info(self, data, dictTitle=None):       self._dummy(data)
    def debug(self, data, dictTitle=None):      self._dummy(data)
    def error(self, data, dictTitle=None):      self._dummy(data)
    def warning(self, data, dictTitle=None):    self._dummy(data)
    def _dummy(self, data): pass

    '''
    def _print(self, data, stackNum=2):
        TAB = 4
        data = '{0}{1}'.format(TAB*' ',data)
        caller = inspect.stack()[stackNum]
        dummy, programFile, lineNumber, funcName, lineCode, rest = caller
        if funcName == '<module>': funcName = '__main__'
        pkg = package.split('.', 1)[1] + '.' +funcName
        str = "[{FUNC:<20}:{LINENO}] - {DATA}".format(FUNC=pkg, LINENO=lineNumber, DATA=data)
        print (str)
    '''



##############################################################
# http://stackoverflow.com/questions/16203908/how-to-input-variables-in-logger-formatter
##############################################################
class ContextFilter(logging.Filter):
    """
    This is a filter which injects contextual information into the log.

    Rather than use actual contextual information, we just use random
    data in this demo.
    """
    def __init__(self, defaultStack=6, autoReset=False):
        '''
        defaultStack=5 sembra OK
        defaultStack=6 sembra OK all'interno di una classe
        '''
        self._defaultStack  = defaultStack
        self._line          = None
        self._name          = None
        self._LnFuncName    = None      # creata da me
        self._stack         = defaultStack
        self._fDEBUG        = False
        self._autoReset     = autoReset
        self._Module_Funcname = True   # module.funcname else funcname



    def getAutoReset(self):
        return self._autoReset

    def setModuleFuncName(self, flag):
        return self._Module_Funcname

    def setAutoReset(self, flag):
        self._autoReset = flag

    def setLineNO(self, number):
        self._line = number

    def setFuncName(self, myname):
        self._LnFuncName = myname

    def setDefaultStack(self, number):
        self._defaultStack = number

    def setStack(self, number):
        self._stack = number if number else self._defaultStack

    def addStack(self, number):
        self._stack = (self._defaultStack + number) if number else self._defaultStack
        # print ('self._stack changed to:', self._stack)

    def filter(self, record):
        dummy, programFile, lineNO, funcName, lineCode, rest = inspect.stack()[self._stack]
        if self._autoReset: self._stack = self._defaultStack
        if funcName == '<module>': funcName = '__main__'

        if self._Module_Funcname == True:
            fname = os.path.basename(programFile).split('.')[0]
            funcName = "{0}.{1}".format(fname, funcName)




            # - modifica della riga
        if self._line:
            record.lineno = self._line
            if self._autoReset: self._line = None
        else:
            record.lineno = lineNO

            # - modifica della LnFuncName
        if self._LnFuncName:
            record.LnFuncName = self._LnFuncName
            if self._autoReset: self._LnFuncName = None
        else:
            record.LnFuncName = funcName


            # - modifica del name
        if self._name:
            record.name = self._name
            if self._autoReset: self._name = None
        else:
            record.name = funcName


        return True

























# ====================================================================================
# - dal package passato come parametro cerchiamo di individuare se la fuzione/modulo
# - è tra quelli da fare il log.
# - Il package mi server per verficare se devo loggare il modulo o meno
# ====================================================================================
def SetLogger(package, exiting=False, offsetSL=0):

    pointers = LnLogger.static_getMainPointers()
        # importante prendere questo pointer in quanto mi porta dietro anche i .info, .debug, ...
    logger = pointers.ClassInstance

    fDEBUG = False
    if fDEBUG:
        print('     rootName      = ', logger._name)
        print('     realLogger    = ', logger._realLogger)
        print('     ClassInstance = ', logger)
        print('     LnFilter      = ', logger._LnFilter)
        print('     modulesToLog  = ', logger._modulesToLog)
        print('     logLevel      = ', logger._logLevel)
        print('     nullLogger    = ', logger._nullLogger)


    caller_01 = GetCaller(1)


        # ---------------------------------
        # - individuiamo se è un modulo
        # - da tracciare o meno
        # ---------------------------------
    fullPkg = (package + '.' + caller_01._funcname)
    if '!ALL!' in logger._modulesToLog:
        LOG_LEVEL = logger._logLevel

    else:
        fullPkg_LOW = fullPkg.lower()
        LOG_LEVEL = None
        for moduleStr in logger._modulesToLog:
            if moduleStr.lower() in fullPkg_LOW:
                LOG_LEVEL = logger._logLevel


    if fDEBUG:
        print ('fullPkg   :', fullPkg )
        print ('LOG_LEVEL :', LOG_LEVEL )


    if not LOG_LEVEL:
        logger._logEnabled = False   #  by Loreto:  22-01-2018 09.15.02
        return logger  # in fase di verifica  #  by Loreto:  22-01-2018 09.14.58
        # return _nullLogger

    logger.setLevel(LOG_LEVEL)
    logger._LnFilter.addStack(1+offsetSL)    # cambio lo stackNum
    caller_03 = GetCaller(3)


    if exiting:
        logger.info('.... exiting\n')
    else:
        logger.info('.... entering called by: {CALLER}'.format(CALLER=caller_03._fullcaller))

    return logger



###############################################
#
###############################################
def GetCaller(stackLevel=0):
    retCaller = LnClass()
    retCaller._rcode  = 0

    try:
        dummy, programFile, lineNumber, funcName, lineCode, rest = inspect.stack()[stackLevel]

    except Exception as why:
        retCaller._fullcaller  = str(why)
        retCaller._rcode  = 1
        return retCaller   # potrebbe essere out of stack ma ritorniamo comunque la stringa


    if funcName == '<module>': funcName = '__main__'

    retCaller._funcname   = funcName
    retCaller._linecode   = lineCode
    retCaller._lineno     = lineNumber
    retCaller._fullfname  = programFile

    fname                 = os.path.basename(programFile).split('.')[0]
    retCaller._fname      = fname
    retCaller._fullcaller = "[{0}.{1}:{2}]".format(fname, funcName, lineNumber)

    return retCaller

