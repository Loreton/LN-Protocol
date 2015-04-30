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
def preparePATHs(fDEBUG):
    thisModuleDIR   = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
    # print (thisModuleDIR)
    if thisModuleDIR.endswith('.zip'):
        myPaths = [ '.', '../', '../../', '../../../' , '../../../../', '/home/pi/gitREPO']

    else:
        myPaths = [ '.', '../', '../../', '../../../', '/home/pi/gitREPO']

    myPaths.reverse()
    if fDEBUG: print ("...... l'ordine va letto dal basso verso l'alto")
    for path in myPaths:
        path = os.path.abspath(os.path.join(thisModuleDIR, path))
        if fDEBUG: print ('......', path)
        sys.path.insert(0, path)

    import LnFunctionsLight as Lnf
    return Lnf
