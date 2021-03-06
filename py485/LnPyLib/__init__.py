#!/usr/bin/env python3
# -*- coding: iso-8859-1 -*-
#
# updated by ...: Loreto Notarantonio
# Version ......: 23-01-2018 12.17.45
#



# ---------- LnLIB Logger Functions ------
# from . Logger.LnLogger                  import init             as InitLogger
# from . Logger.LnLogger                  import SetLogger        as SetLogger
from . Logger.LnLogger_Class              import LnLogger        as InitLogger
from . Logger.LnLogger_Class              import SetLogger
# from . Logger.SetLogger                   import SetLogger

# ---------- LnLIB COMMON Functions ------
from . Common.Exit                        import Exit             as Exit
from . Common.LnColor                     import LnColor          as Color


# ---------- LnLIB PARSE INPUT ------
from . ParseInput.MainParseInput          import processInput         # start ParseInput process
from . ParseInput.PositionalParameters    import positionalParameters # check for positional parameters (0,1,2) if required
from . ParseInput.CreateParser            import createParser         # create myParser

from . ParseInput.Options.check_file      import check_file           # verify if inputFile esists
from . ParseInput.Options.ColoredHelp     import coloredHelp          # set coloredHelp for parameters
from . ParseInput.Options.Debug_Options   import debugOptions         # set debug and other options
from . ParseInput.Options.Log_Options     import logOptions           # set --log, --log-console, --log-file
from . ParseInput.Options.IniFile_Options import iniFileOptions       # get projectName.ini for base parameters

# ---------- LnLIB DotMap dictionary ------
# from . Dict_Prev.LnDict_DotMap          import DotMap           as Dict
from . Dict.Ln_DotMap                     import DotMap           as Dict


# ---------- LnLIB FILE functions ------
from . File.ReadIniFile_Class             import ReadIniFile      as ReadIniFile
# from . File.VerifyPath                  import VerifyPath       as VerifyPath

# ---------- LnLIB System functions ------
# from . System                           import SetOsEnv         as OsEnv
from . System.GetKeyboardInput            import getKeyboardInput as KeyboardInput

# ---------- LnLIB Process functions ------
from . Process.RunProgram                 import ExecGetOut       as runGetOut
from . Process.RunProgram                 import StartProgram     as runProgram
from . Process.RunProgram                 import OutOnFile        as runGetOnfile

# from . Monkey                           import LnMonkeyFunctions # per Path.LnCopy, Path.LnBackup


# from . Serial_Prev.LnRs232_Class               import LnRs232 as Rs232 #                                                         import di un membro
# from . Serial_Prev.LnRs485_Class               import LnRs485 as Rs485 #                                                         import di un membro
from . Serial.LnRs232_Class               import LnRs232 as Rs232 #                                                         import di un membro
from . Serial.LnRs485_Class               import LnRs485 as Rs485 #                                                         import di un membro
