#!/usr/bin/python3.5
#
# updated by ...: Loreto Notarantonio
# Version ......: 17-01-2018 15.00.55
#
# -----------------------------------------------

import    Source as Prj

#######################################################
# PROGRAM options
#######################################################
def programOptions(myParser):
    # ----- common part into the Prj modules --------
    # import    Source as Prj
    Ln     = Prj.LnLib
    C      = Ln.Color()
    # logger = Ln.SetLogger(__package__)
    # -----

        # ---------------------------------------
        # - devo mettere un carattere prima
        # - altrimenti da errore a causa
        # - dei char speciali del colore.
        # ---------------------------------------
    mySeparatorText = '-' + C.getColored(color=C.magentaH, text='---------------program options ----')
    myParser.add_argument(mySeparatorText,
                                required=False,
                                action='store_true',
                                help=C.coloredHelp('', None))
