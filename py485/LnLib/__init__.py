#!/usr/bin/env python3
# -*- coding: iso-8859-1 -*-

from  sys import version_info as sysVersion, path as sysPath, exit as sysExit
import platform
# from pathlib import Path

# migliore implementazione di pathlib.Path
#    https://pathpy.readthedocs.io/en/latest/
# from LnLib.File.LnPath import Path as Path

'''
scriptMain  = Path(sys.argv[0]).resolve()
projectDir  = scriptMain.parent
currDir  = Path.cwd()
currDir  = Path('.').resolve()
print (scriptMain)
print (projectDir)
'''

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
    # print (ProjectDir)
    # print (LnLibDir)
    # print (LnLibDir.joinpath('Common'))
    for path in sysPath: print (path)
    print ()
# sysExit()



# ############### OpSy type & version
# - sys.version_info(major=3, minor=3, micro=2, releaselevel='final', serial=0)
v = sysVersion
pyVer = '{0}{1}{2}'.format(v.major, v.minor, v.micro)
opSys = platform.system()
if opSys.lower() == 'windows':
    isWindows = True
else:
    isWindows = False
isUnix    = not isWindows
# ############### OpSy type & version


from . Common.LnLogger                 import init             as InitLogger
from . Common.LnLogger                 import SetLogger        as SetLogger
from . Common.Exit                     import Exit             as Exit
from . Common.LnColor                  import LnColor          as Color
# from   .                             import ParseInput

from . ParseInput.PositionalParameters import positionalParameters
from . ParseInput.check_file           import check_file
from . ParseInput.CreateParser         import createParser
from . ParseInput.ColoredHelp          import coloredHelp
from . ParseInput.Debug_Options        import debugOptions
from . ParseInput.Log_Options          import logOptions
from . ParseInput.IniFile_Options      import iniFileOptions

from . Dict.LnDict_DotMap              import DotMap           as Dict

from . File.ReadIniFile_Class          import ReadIniFile      as ReadIniFile


from . File.VerifyPath                 import VerifyPath       as VerifyPath

from . System                          import SetOsEnv         as OsEnv
from . System.GetKeyboardInput         import getKeyboardInput as KeyboardInput

from . Process.RunProgram              import ExecGetOut       as runGetOut
from . Process.RunProgram              import StartProgram     as runProgram
from . Process.RunProgram              import OutOnFile        as runGetOnfile


