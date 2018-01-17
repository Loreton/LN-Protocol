#!/usr/bin/python3.5
#
# updated by ...: Loreto Notarantonio
# Version ......: 09-01-2018 07.51.23
#
# -----------------------------------------------

# ------ User ParseInput -----
from . DigitalPin_Options     import read                as DIGITAL_READ
from . DigitalPin_Options     import write               as DIGITAL_WRITE
from . DigitalPin_Options     import toggle              as DIGITAL_TOGGLE

from . MonitorRS485_Options   import monitorRs485        as MONITOR_RS485
from . MonitorRS485_Options   import monitorRaw          as MONITOR_RAW

from . Program_Options        import programOptions