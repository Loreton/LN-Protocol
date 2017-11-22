#!/usr/bin/python3.5
#
# Scope:  Programma per ...........
# LnVer_2017-11-05_18.26.32
# -----------------------------------------------
# from . Common.MyHelp                import myHELP
# from . Common.check_file            import check_file

import  LnLib as Ln; C=Ln.Color()
pInp    = Ln.ParseInput

#######################################################
# PROGRAM options
#######################################################
def digitalWrite(gv, myParser):

        # ---------------------------------------
        # - devo mettere un carattere prima
        # - altrimenti da errore a causa
        # - dei char speciali del colore.
        # ---------------------------------------
    mySeparatorText = '-' + C.getColored(color=C.magentaH, text='---------------digital write options ----')
    myParser.add_argument(mySeparatorText,
                                required=False,
                                action='store_true',
                                help=pInp.coloredHelp('', None))


    myParser.add_argument('-cf', '--config-file',
                                metavar='',
                                type=pInp.check_file,
                                required=False,
                                default=gv.defaultConfigFile,
                                help=pInp.coloredHelp('Specifies config fileName...', default=gv.defaultConfigFile))

    myParser.add_argument('-a', '--slave-address',
                                metavar='',
                                type=int,
                                required=True,
                                default=None,
                                help=pInp.coloredHelp('slave address to send command...', default=None))

    myParser.add_argument('-p', '--pin-number',
                                metavar='',
                                type=int,
                                required=True,
                                default=None,
                                help=pInp.coloredHelp('pin number...', default=None))

    myParser.add_argument('-r', '--relay',
                                metavar='',
                                required=False,
                                action='store_false',
                                help=pInp.coloredHelp('user Arduino RELAY ...', default=True))

