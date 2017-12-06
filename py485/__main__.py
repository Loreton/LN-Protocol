#!/usr/bin/python3.4
# -*- coding: iso-8859-1 -*-
# -*- coding: utf-8 -*-
#
# updated by ...: Loreto Notarantonio
# Version ......: 06-12-2017 15.35.55
#                                               by Loreto Notarantonio
# ######################################################################################
import sys; sys.dont_write_bytecode = True
import os

# current:  03-12-2017
#               attualmente in simulator con ritorno in RS485
#               leggere la porta del Relay in RS485

#@TODO: impostare il monitoring leggendo una porta specifica di un Arduino.
#       La lettura potrà avvenire come TEXT oppure come Rs485

import  Source as Prj
# Inserimento del path corretto per il caricamneto della LnLib
Prj.projectGlobalVars.LibPath('LnLib_20171123', libType='zipx')

import  LnLib  as Ln

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




