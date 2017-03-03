#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per ...........
# modified:  v2017-03-02_14.34.48
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################


import os, sys
import datetime
this_mod = sys.modules[__name__]


# ssh -o "NumberOfPasswordPrompts=1" -o "StrictHostKeyChecking=no" -i /cygdrive/c/Users/f602250/.ssh/id_rsa -l f602250 esil600.ac.bankit.it 'bash -s' < j:/GIT-REPO/Python3/ServerScan/conf/LnDiscovery.sh

################################################################################
# - M A I N
# - Prevede:
# -  2 - Controllo parametri di input
# -  5 - Chiamata al programma principale del progetto
################################################################################
def Main(gv, action):
    logger  = gv.Ln.SetLogger(package=__name__)
    C       = gv.Ln.LnColor()

    fEXECUTE = gv.INPUT_PARAM.fEXECUTE
    now      = str(datetime.datetime.now()).split('.')[0]







        # ===================================================
        # = 'server.struct'
        # ===================================================
    if gv.INPUT_PARAM.actionCommand == 'rs485.monitor':
        # DBdict.printTree()
        # colName = 'JBoss-Ver'
        return

    else:
        print(gv.INPUT_PARAM.actionCommand, 'not available')
        return

