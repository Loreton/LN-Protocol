#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import sys
import os
import argparse

LnColor = None
Ln      = None
def SetGlobals(color, gvLn):
    global LnColor, Ln
    LnColor = color
    Ln = gvLn




####################################
# - executeOptions
####################################
def ExecuteOptions(myParser, required=False):
    mandatory = LnColor.getMagentaH('is MANDATORY - ') if required else LnColor.getCyanH('is OPTIONAL - ')
    myParser.add_argument( "--go",
                            action="store_true",
                            dest="fEXECUTE",
                            default=required,
                            help=mandatory + LnColor.getYellow("""Execute commands.
    [DEFAULT: False, run in DRY-RUN mode]
    """))



####################################
# -
####################################
def UsbPort(myParser, required):
    mandatory = LnColor.getMagentaH('is MANDATORY - ') if required else LnColor.getCyanH('is OPTIONAL - ')

    myParser.add_argument( "-p", "--port",
                            type=isUsbDevice,
                            required=required,
                            dest="usbPort",
                            default=None,
                            help=mandatory + LnColor.getYellow("""nome della porta USB da monitorare.
    [DEFAULT: None]
    """))

####################################
# -
####################################
def Rs485Address(myParser, required):
    mandatory = LnColor.getMagentaH('is MANDATORY - ') if required else LnColor.getCyanH('is OPTIONAL - ')

    myDefault = None
    myParser.add_argument( "-a", "--address",
                            type=int,
                            required=required,
                            dest="rs485Address",
                            default=myDefault,
                            help=mandatory + LnColor.getYellow("""indirizzo del dispositivo RS-485 [1-254].
    [DEFAULT: {0}]
    """.format(myDefault)))



####################################
# # isUsbDevice()
####################################
def isUsbDevice(usbDevName):
    usbDevPath =  Ln.isUsbDevice(usbDevName)
    if not usbDevPath:
        print('[{MOD}]: {DEV} - is not a valid USB device'.format(MOD=__name__.split('.')[-1], DEV=usbDevName))
        sys.exit()

    return usbDevPath

