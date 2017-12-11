#!/usr/bin/python3.4
# -*- coding: iso-8859-1 -*-
# -*- coding: utf-8 -*-
#
# updated by ...: Loreto Notarantonio
# Version ......: 11-12-2017 17.10.44
#                                               by Loreto Notarantonio
# ######################################################################################
import sys; sys.dont_write_bytecode = True
import os
from pathlib import Path


# ----------------------------------------------
# - Inserimento del path corretto della LnLib
# - Le path per LnLib vanno impostate
# - prima di fare gli import
# ----------------------------------------------
LnLibPath = Path(sys.argv[0]).resolve().parent / 'bin' / 'LnLib_2017-12-11.zipx'
sys.path.insert(0, str(LnLibPath))


import  LnLib as Ln
import  Source as Prj

################################################################################
# - M A I N
################################################################################
if __name__ == "__main__":
    gv        = Ln.Dict()

    args      = Prj.ParseInput() # ; print (args)
    gv.args   = Ln.Dict(args)
    gv.fDEBUG = gv.args.debug
    if gv.fDEBUG: gv.args.printTree(fPAUSE=True)

    logger    = Ln.InitLogger(toFILE=gv.args.log, logfilename=gv.args.log_filename, toCONSOLE=gv.args.log_console, ARGS=args)

        # ------------------------
        # - Lettura del file.ini
        # ------------------------
    iniFile = Ln.ReadIniFile(gv.args.ini_file, strict=True)
    iniFile.read(resolveEnvVars=False)
    iniFile.setDebug(gv.fDEBUG)
    gv.iniFile = Ln.Dict(iniFile.dict)
    if gv.fDEBUG: gv.iniFile.printTree(header="INI File", fPAUSE=True)

        # ===================================================
        # - Inizio applicazione
        # ===================================================

    Prj.Main(gv)
    gv.Ln.Exit(0, "completed", printStack=False, stackLevel=9, console=True)
    sys.exit()




