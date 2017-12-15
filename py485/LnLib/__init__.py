#!/usr/bin/env python3
# -*- coding: iso-8859-1 -*-

from  sys import version_info as sysVersion, path as sysPath, exit as sysExit
import platform

# --------------------------------------------
# - inserire i path per fare l'import delle funzioni LnLib
# - ... sembra che non serva in quanto il path del progetto
# - ... è già inserito... comunque non si sa mai.
# --------------------------------------------
# LnLibDir    = Path(__file__).parent
# ProjectDir  = Path(LnLibDir).parent
# sysPath.insert(0, LnLibDir)
# sysPath.insert(0, ProjectDir)

if False:
    print ()
    for path in sysPath: print (path)
    print ()



'''
    # - sys.version_info(major=3, minor=3, micro=2, releaselevel='final', serial=0)
    v = sysVersion
    pyVer = '{0}{1}{2}'.format(v.major, v.minor, v.micro)
    opSys = platform.system()
    if opSys.lower() == 'windows':
        isWindows = True
    else:
        isWindows = False
    isUnix    = not isWindows

'''


# ---------- LnLIB COMMON Functions ------
from . Common.LnLogger                 import init             as InitLogger
from . Common.LnLogger                 import SetLogger        as SetLogger
from . Common.Exit                     import Exit             as Exit
from . Common.LnColor                  import LnColor          as Color


# ---------- LnLIB PARSE INPUT ------
from . ParseInput.PositionalParameters import positionalParameters # check for positional parameters (0,1,2) if required
from . ParseInput.check_file           import check_file           # verify if inputFile esists
from . ParseInput.CreateParser         import createParser         # create myParser
from . ParseInput.ColoredHelp          import coloredHelp          # set coloredHelp for parameters
from . ParseInput.Debug_Options        import debugOptions         # set debug and other options
from . ParseInput.Log_Options          import logOptions           # set --log, --log-console, --log-file
from . ParseInput.IniFile_Options      import iniFileOptions       # get projectName.ini for base parameters
from . ParseInput.MainParseInput       import processInput         # start ParseInput process

# ---------- LnLIB DotMap dictionary ------
# from . Dict_Prev.LnDict_DotMap         import DotMap           as Dict
from . Dict.Ln_DotMap              import DotMap           as Dict


# ---------- LnLIB FILE functions ------
from . File.ReadIniFile_Class          import ReadIniFile      as ReadIniFile
from . File.VerifyPath                 import VerifyPath       as VerifyPath

# ---------- LnLIB System functions ------
from . System                          import SetOsEnv         as OsEnv
from . System.GetKeyboardInput         import getKeyboardInput as KeyboardInput

# ---------- LnLIB Process functions ------
from . Process.RunProgram              import ExecGetOut       as runGetOut
from . Process.RunProgram              import StartProgram     as runProgram
from . Process.RunProgram              import OutOnFile        as runGetOnfile


from . String.LnEnum                   import LnEnum         as Enum


# ---------- RS485 functions ------
# from . LnRS485.LnRs485_Class             import LnRs485 as Rs485 # import di un membro

from . LnSerial.LnRs232_Class             import LnRs232 as Rs232 # import di un membro
from . LnSerial.LnRs485_Class             import LnRs485 as Rs485 # import di un membro
