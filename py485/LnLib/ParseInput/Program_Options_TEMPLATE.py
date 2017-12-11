#!/usr/bin/python3.5
#
# updated by ...: Loreto Notarantonio
# Version ......: 23-11-2017 17.08.14
#
# -----------------------------------------------

import  LnLib as Ln; C=Ln.Color()
#######################################################
# PROGRAM options
#######################################################
def programOptions(myParser):

        # ---------------------------------------
        # - devo mettere un carattere prima
        # - altrimenti da errore a causa
        # - dei char speciali del colore.
        # ---------------------------------------
    mySeparatorText = '-' + C.getColored(color=C.magentaH, text='---------------program options ----')
    myParser.add_argument(mySeparatorText,
                                required=False,
                                action='store_true',
                                help=Ln.coloredHelp('', None))
