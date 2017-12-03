#!/usr/bin/python3.5
#
# Scope:  Programma per ...........
# LnVer_2017-11-05_18.26.32
# -----------------------------------------------
# from . Common.MyHelp                import myHELP
# from . Common.check_file            import check_file

import  LnLib as Ln; C=Ln.Color()


#######################################################
# PROGRAM options
#######################################################
def read(myParser):
    digitalPin(myParser)

def toggle(myParser):
    digitalPin(myParser)

def write(myParser):
    digitalPin(myParser)

    onOffGroup = myParser.add_mutually_exclusive_group(required=True)  # True indica obbligatorietà di uno del gruppo

    onOffGroup.add_argument( "--on",
                                # required=False,
                                action='store_true',
                                help=Ln.coloredHelp("Set pin ON.", required=True))

    onOffGroup.add_argument( "--off",
                                # required=False,
                                action='store_true',
                                help=Ln.coloredHelp("Set pin OFF.", required=True))


#######################################################
# PROGRAM options
#######################################################
def digitalPin(myParser):

        # ---------------------------------------
        # - devo mettere un carattere prima
        # - altrimenti da errore a causa
        # - dei char speciali del colore.
        # ---------------------------------------
    mySeparatorText = '-' + C.getColored(color=C.magentaH, text='---------------digital write options ----')
    myParser.add_argument(mySeparatorText,
                                required=False,
                                action='store_true',
                                help=Ln.coloredHelp('', None))


    myParser.add_argument('-s', '--slave-address',
                                metavar='',
                                type=int,
                                required=True,
                                default=None,
                                help=Ln.coloredHelp('slave address to send command...', default=None, required=True))

    myParser.add_argument('-p', '--pin-number',
                                metavar='',
                                type=int,
                                required=True,
                                default=None,
                                help=Ln.coloredHelp('pin number...', default=None, required=True))




