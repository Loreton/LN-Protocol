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


    myParser.add_argument('-a', '--slave-address',
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




