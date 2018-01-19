#!/usr/bin/python3.4
# -*- coding: iso-8859-1 -*-
# -*- coding: utf-8 -*-
#
# updated by ...: Loreto Notarantonio
# Version ......: 19-01-2018 16.37.40
#
# ######################################################################################
import sys; sys.dont_write_bytecode = True
# from pathlib import Path


import    Source as Prj

myLibName = ['LnPyLib', 'xxxLnLib_2018-01-04.zip']
Prj.LnLib = Prj.SPE.LibPath(myLibName, fDEBUG=False)

# -------------------------------------------------------
# - inseriamo la LnLib e le gVars all'interno della Prj
# - in modo che ce la ritroviamo in tutti i moduli
# - facendo il solo import della Prj
# -------------------------------------------------------
Prj.gv    = Prj.LnLib.Dict()



################################################################################
# - M A I N
#    python.exe __main__.py ....
################################################################################
if __name__ == "__main__":
    # ----- common part into the Prj modules --------
    Ln          = Prj.LnLib
    gv          = Prj.gv
    # -----------------------------------------------
        # -------------------------------
        # - Lettura parametri di input
        # -------------------------------
    args      = Prj.ParseInput()
    gv.args   = Ln.Dict(args)
    gv.fDEBUG = gv.args.debug
    if gv.fDEBUG: gv.args.printTree(fPAUSE=True)

        # -------------------------------
        # - Inizializzazione del logger
        # -------------------------------
    # logger    = Ln.InitLogger(  name='LnLoggerClass',
    logger    = Ln.InitLogger(
                                logfilename=gv.args.log_filename,
                                toFILE=gv.args.log,
                                toCONSOLE=gv.args.log_console,
                                defaultLogLevel=gv.args.loglevel,
                                rotationType='time', when="m", interval=60,
                                # rotationType='size', maxBytes=500000,
                                backupCount=5,
                                filterDefaultStack=5
                            )

    logger.info(gv.args, dictTitle='command line parameters...')



        # ------------------------
        # - Lettura del file.ini
        # ------------------------
    iniFile = Ln.ReadIniFile(gv.args.ini_file, strict=True)
    iniFile.read(resolveEnvVars=False)
    gv.iniFile = Ln.Dict(iniFile.dict)
    gv.args.iniFile = Ln.Dict(iniFile.dict)
    if gv.fDEBUG: gv.iniFile.printTree(header="INI File", fPAUSE=True)

        # ===================================================
        # - Inizio applicazione
        # ===================================================

    Prj.Main(gv)
    gv.Ln.Exit(0, "completed", printStack=False, stackLevel=9, console=True)
    sys.exit()




