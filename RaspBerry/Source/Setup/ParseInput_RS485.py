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
def SerialPort(myParser, required):
    mandatory = LnColor.getMagentaH('is MANDATORY - ') if required else LnColor.getCyanH('is OPTIONAL - ')

    myParser.add_argument( "--port",
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
def RelayPort(myParser, required):
    mandatory = LnColor.getMagentaH('is MANDATORY - ') if required else LnColor.getCyanH('is OPTIONAL - ')

    myParser.add_argument( "--relay",
                            type=isUsbDevice,
                            required=required,
                            dest="usbPort",
                            default=None,
                            help=mandatory + LnColor.getYellow("""nome della porta USB dove si trova il relay-Arduino.
    [DEFAULT: None]
    """))

####################################
# -
####################################
def Rs485Address(myParser, required):
    mandatory = LnColor.getMagentaH('is MANDATORY - ') if required else LnColor.getCyanH('is OPTIONAL - ')

    # nargs - importante: dopo il flag lasciare lo spazio....
    myDefault = None
    myParser.add_argument( "-a", "--address",
                            type=int,
                            required=required,
                            dest="rs485Address",
                            default=myDefault,
                            nargs='+',
                            help=mandatory + LnColor.getYellow("""indirizzo/i del dispositivo RS-485 [1-254]
                        separati da BLANK se più di uno.
    [DEFAULT: {0}]
    """.format(myDefault)))






# ---------------------------
# - DataProtocol
# ---------------------------
def DataProtocol(myParser, required=False):

    mandatory = LnColor.getMagentaH('is MANDATORY - ') if required else LnColor.getCyanH('is OPTIONAL - ')
    rs485Group = myParser.add_mutually_exclusive_group(required=True)  # True indica obbligatorietà di uno del gruppo


    DEFAULT = False
    rs485Group.add_argument( "--raw",
                            action="store_true",
                            dest="fRAW",
                            default=DEFAULT,
                            help=mandatory + LnColor.getYellow("""read data in raw format
            DEFAULT = {DEF}
    """.format(DEF=DEFAULT)))

    rs485Group.add_argument( "--rs485",
                            action="store_true",
                            dest="fRS485",
                            default=DEFAULT,
                            help=mandatory + LnColor.getYellow("""send data in LnRs485 protocol format
            DEFAULT = {DEF}
    """.format(DEF=DEFAULT)))






# ---------------------------
# - DataFormat
# ---------------------------
def DisplayDataFormat(myParser, required=False):
    mandatory = LnColor.getMagentaH('is MANDATORY - ') if required else LnColor.getCyanH('is OPTIONAL - ')

    # rawGroup = myParser.add_mutually_exclusive_group(required=True)  # True indica obbligatorietà di uno del gruppo
    # rawGroup = myParser.add_argument_group(
    #                         title=LnColor.getGreenH('raw data display'),
    #                         description=LnColor.getGreenH("definisce il formato dei dati per il display"),
    #                         )



    '''
    DEFAULT = True
    rawGroup.add_argument( "--hex",
                            action="store_true",
                            dest="fHEX",
                            default=DEFAULT,
                            help=mandatory + LnColor.getYellow("""remove HEX format display
            DEFAULT = {DEF}
    """.format(DEF=DEFAULT)))

    DEFAULT = False
    rawGroup.add_argument( "--char",
                            action="store_true",
                            dest="fCHAR",
                            default=DEFAULT,
                            help=mandatory + LnColor.getYellow("""ADD single char display
            DEFAULT = {DEF}
    """.format(DEF=DEFAULT)))


    rawGroup.add_argument( "--line",
                            action="store_true",
                            dest="fLINE",
                            default=DEFAULT,
                            help=mandatory + LnColor.getYellow("""ADD full line display
            DEFAULT = {DEF}
    """.format(DEF=DEFAULT)))
    '''

    myDefault = int('0x0A', 16) # integer
    myDefault = None
    myParser.add_argument( "--eod",
                            type=int,
                            required=required,
                            dest="eod_char",
                            default=myDefault,
                            help=mandatory + LnColor.getYellow("""end Of Data char (espresso in decimale es: 10 per NL).
        [DEFAULT: {0}]
    """.format(myDefault)))

    myParser.add_argument( "--type",
                            # type=int,
                            required=required,
                            nargs='*',
                            dest="displayDataformat",
                            choices=['hex', 'line', 'char'],
                            default=None,
                            help=mandatory + LnColor.getYellow("""displayed data format:
            hex:    hexadecima format
            line:   ascii lin data
            char:   print ascii char and hex value

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

