#!/usr/bin/python3.5
#
# Scope:  Programma per ...........
# LnVer_2017-11-05_18.26.32
# -----------------------------------------------
# from . Common.MyHelp                import myHELP
# from . Common.check_file            import check_file

import  LnLib as Ln
pInp    = Ln.ParseInput
import  LnLib as Ln; C=Ln.Color()
#######################################################
# PROGRAM options
#######################################################
def noPositionalParameters(gv, myParser):

        # ---------------------------------------
        # - devo mettere un carattere prima
        # - altrimenti da errore a causa
        # - dei char speciali del colore.
        # ---------------------------------------
    mySeparatorText = '-' + C.getColored(color=C.magentaH, text='---------------program options ----')
    myParser.add_argument(mySeparatorText,
                                required=False,
                                action='store_true',
                                help=pInp.coloredHelp('', None))


    myParser.add_argument('--config-file',
                                metavar='',
                                type=pInp.check_file,
                                required=False,
                                default=gv.defaultConfigFile,
                                help=pInp.coloredHelp('Specifies config fileName...', default=gv.defaultConfigFile))

