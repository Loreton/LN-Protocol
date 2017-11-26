#!/usr/bin/python3.5
#
# updated by ...: Loreto Notarantonio
# Version ......: 26-11-2017 18.17.02
#
# -----------------------------------------------



from . Main.Main                         import Main

# ------ User ParseInput -----
from . ParseInput.Main_ParseInput        import ParseInput
from . ParseInput.DigitalPin             import read                as DIGITAL_READ
from . ParseInput.DigitalPin             import write               as DIGITAL_WRITE
from . ParseInput.MonitorRS485           import monitorRs485        as MONITOR_RS485
from . ParseInput.MonitorRS485           import monitorRaw          as MONITOR_RAW
from . ParseInput.Program_Options        import programOptions




from . LnRS485.LnRs485_Class             import LnRs485_Instrument as Rs485 # import di un membro
from . Main.OpenRs485Port                import openRs485Port
from . Main.OpenRs485Port                import openRs485Port


# - Monitor
from . Monitor.MonitorRs485              import monitorRS485
from . Monitor.MonitorRs485              import monitorRaw

# - Process
from . Process.DigitalPin                import digitalRead
# from . Process.DigitalPin                import digitalWrite