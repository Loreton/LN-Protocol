#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# -*- coding: latin-1 -*-
#                                               &  Loreto Notarantonio 2014, July
# ######################################################################################
import os, sys

################################################################################
# - inseriamo la lista delle dir dove possiamo trovare le LnFunctions
# - vale anche per quando siamo all'interno del .zip
################################################################################
def preparePaths(mainModule, fDEBUG=False):
    # mainModule                      = os.path.abspath(os.path.realpath(__file__))
    mainModuleDIR                   = os.path.dirname(mainModule)
    mainModuleName, mainModuleExt   = os.path.basename(mainModule).split('.')

    # print(mainModuleDIR, mainModuleName, mainModuleExt)

    # sys.exit()
    pathsLevels = [ '.', '../', '../../', '../../../', '../../../../' ]

    if mainModuleExt == 'zip':
        level = 3
        zipFnameList = ['LnFunctions.zip', 'LnFunctions_2015-10-16.zip']
    else:
        level = 2
        zipFnameList = ''
        zipFnameList = ['LnFunctions_2015-10-16.zip']

    for i in reversed(range(level)):
        for zipName in zipFnameList:
            path = os.path.abspath(os.path.join(mainModuleDIR, pathsLevels[i], zipName))
            if os.path.isfile(path):
                sys.path.insert(0, path)

        path = os.path.abspath(os.path.join(mainModuleDIR, pathsLevels[i]))
        sys.path.insert(0, path)


    if fDEBUG:
        for path in sys.path:
            print ('......', path)

    import LnFunctions       as Ln          # All'interno dello zip deve esserci la dir LnFunction

    return Ln