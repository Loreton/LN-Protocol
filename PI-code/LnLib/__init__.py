#!/usr/bin/env python3
# -*- coding: iso-8859-1 -*-

import sys, os
import platform


# - sys.version_info(major=3, minor=3, micro=2, releaselevel='final', serial=0)
v = sys.version_info
pyVer = '{0}{1}{2}'.format(v.major, v.minor, v.micro)
OpSys = platform.system()


from . LnCommon.LnLogger                import SetLogger
from . LnCommon.LnLogger                import InitLogger
from . LnCommon.LnLogger                import SetNullLogger
from . LnCommon.LnColor                 import LnColor
from . LnCommon.Exit                    import Exit

from . System.GetKeyboardInput          import getKeyboardInput
from . System.ExecRcode                 import ExecRcode
from . System.ExecGetOut                import ExecGetOut
from . System.GetFunctionPtr            import GetFunctionPtr

from . LnDict                           import DotMap  as LnDict

from . LnFile.ReadIniFile_Class         import ReadIniFile
from . LnFile.ReadWriteTextFile         import readTextFile
from . LnFile.ReadWriteTextFile         import WriteTextFile
from . LnFile.WriteCSVFile              import WriteCSVFile

from . LnDevices.isUsbDevice              import  isUsbDevice

from . LnString.LnCRC8                  import  strCheckSum
from . LnString.LnCRC8                  import  hexCheckSum
from . LnString.LnCRC8                  import  byteArrayCheckSum
from . LnString.LnCRC8                  import  calculateCRC8
