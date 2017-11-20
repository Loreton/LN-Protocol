#!/usr/bin/python3.4
#
# updated by ...: Loreto Notarantonio
# Version ......: 20-11-2017 17.08.43
#                                               by Loreto Notarantonio
# ######################################################################################
import sys; sys.dont_write_bytecode = True
import os


from pathlib import Path

######### SET LIB PATH #######################
def LibPath(libName, libType='zip'):
    thisFile      = Path(sys.argv[0]).resolve()
    projectDir    = thisFile.parent
    extensionFile = thisFile.suffix.lower()

    if libType == 'zip' or extensionFile.lower() == '.zip':
        zipFile   = '{}.zip'.format(libName)
        LnLibPath = Path(sys.argv[0]).resolve().parent / 'bin' / zipFile
    else:
        LnLibPath = Path(sys.argv[0]).resolve().parent
        # LnLibPath = Path('y:\GIT-REPO\Python3\LnPythonLib\@LNLIB_BASE')
        print(' loading LnLibrary from Source directory.....')

    sys.path.append(str(LnLibPath))  # deve essere una stringa e non WindowsPath


LibPath('LnLib_20171120', libType='zip')

import  LnLib  as Ln
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

    # Lettura del file.ini

    # iniFile = Ln.ReadIniFile(gv.args.config_file, strict=True, logger=logger)
    iniFile = Ln.ReadIniFile(gv.args.config_file, strict=True)
    iniFile.read(resolveEnvVars=False)
    iniFile.setDebug(gv.fDEBUG)
    gv.iniFile = Ln.Dict(iniFile.dict)
    if gv.fDEBUG: gv.iniFile.printTree(header="INI File", fPAUSE=True)

    # gv.cfgFile = Ln.Dict(iniFile.dict)
    # if gv.fDEBUG: gv.cfgFile.printTree(header="INI File", fPAUSE=True)


        # ===================================================
        # - Inizio applicazione
        # ===================================================

    Prj.Main(gv)
    gv.Ln.Exit(0, "completed", printStack=False, stackLevel=9, console=True)
    sys.exit()




