#!/usr/bin/python3.5
#
# updated by ...: Loreto Notarantonio
# Version ......: 11-12-2017 07.41.15
#
# -----------------------------------------------



from . Main.Main                         import Main

# ------ SETUP -----
from . Setup                                import GlobalVars_Module as projectGlobalVars
from . Setup.Main_ParseInput                import ParseInput

# ------ User ParseInput -----
from . Setup.ParseInput.DigitalPin_Options     import read                as DIGITAL_READ
from . Setup.ParseInput.DigitalPin_Options     import write               as DIGITAL_WRITE
from . Setup.ParseInput.DigitalPin_Options     import toggle              as DIGITAL_TOGGLE
from . Setup.ParseInput.MonitorRS485_Options   import monitorRs485        as MONITOR_RS485
from . Setup.ParseInput.MonitorRS485_Options   import monitorRaw          as MONITOR_RAW
from . Setup.ParseInput.Program_Options        import programOptions




# from . LnRS485.LnRs485_Class             import LnRs485_Instrument as Rs485 # import di un membro
# from . LnRS485.LnRs485_Class             import Formatter485
# from . LnRS485.LnRs485_Formatter             import Formatter485


from . Main.OpenRs485Port                import openRs485Port
from . Main.OpenRs485Port                import openRs485Port


# - Monitor
from . Monitor.MonitorRs485              import monitorRS485
from . Monitor.MonitorRs485              import monitorRaw

# - Process
from . Process.DigitalPin                import digitalRead
from . Process.DigitalPin                import digitalToggle
from . Process.SendToRelay               import SendToRelay
# from . Process.DigitalPin                import digitalWrite