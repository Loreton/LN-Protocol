#!/usr/bin/python3.5
#
# updated by ...: Loreto Notarantonio
# Version ......: 06-12-2017 15.21.30
#
# -----------------------------------------------
'''
    modulo che dovrà contenere tutte le variabili
    destinate ad essere condivise tra i vari moduli del progetto.
    Verrà riempito dinamicamente dai vai moduli e chi avrà necessità
    di accedere a tali variabili dovrà conoscerne il nome.
'''

import sys
from pathlib import Path

######### SET LIB PATH per la libreria LnLib #######################
######### SET LIB PATH per la libreria LnLib #######################
######### SET LIB PATH per la libreria LnLib #######################
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

    sys.path.insert(0, str(LnLibPath))  # deve essere una stringa e non WindowsPath
######### SET LIB PATH per la libreria LnLib #######################
######### SET LIB PATH per la libreria LnLib #######################
######### SET LIB PATH per la libreria LnLib #######################



def LnClass():
    pass
    def __str__(self):
        _str_ = []
        for key,val in self.__dict__.items():
            _str_.append('{:<15}: {}'.format(key, val))

        return '\n'.join(_str_)
