#!/opt/python3.4/bin/python3.4

import sys, os
import time

def SetupEnv(gv, fDEBUG=False):
    # print (gv.Ln.pyVer)
    if gv.Ln.pyVer >= '340':
        # setupEnv340(gv)
        setupEnv300(gv, fDEBUG=fDEBUG)
    else:
        setupEnv300(gv, fDEBUG=fDEBUG)

def setupEnv300(gv, fDEBUG=False):
    C = gv.Ln.LnColor()
        # ------------------------------------------
        # - Preparazione directories
        # ------------------------------------------
    scriptMain  = os.path.abspath(sys.argv[0])
    scriptName  = os.path.basename(scriptMain).split('.')[0]
    scriptExt   = os.path.basename(scriptMain).split('.')[1]
    prjBaseDIR  = os.path.abspath(os.path.dirname(scriptMain))
    lastSubDir  = os.path.basename(prjBaseDIR)
    if lastSubDir in ['bin', 'Source']:
        prjBaseDIR = os.path.abspath(os.path.join(prjBaseDIR, '../'))
    prjName     = os.path.basename(prjBaseDIR)


    configDIR   = os.path.abspath(os.path.join(prjBaseDIR, 'conf'))
    dataDIR     = os.path.abspath(os.path.join(prjBaseDIR, 'data'))

        # ---------------------------------------------------------
        # - file di configurazione
        # ---------------------------------------------------------
    iniFileName = os.path.abspath(os.path.join(configDIR, gv.Prj.name + '_config.ini'))



    gv.Prj.scriptName  = scriptName
    gv.Prj.prjBaseDIR  = prjBaseDIR
    gv.Prj.configDIR   = configDIR
    gv.Prj.dataDIR     = dataDIR
    gv.Prj.iniFileName = iniFileName


    now             = time.localtime()
    gv.Prj.now      = now
    gv.Prj.today    = '{YY:04}.{MM:02}.{DD:02}'.format(YY=now.tm_year, MM=now.tm_mon, DD=now.tm_mday)
    gv.Prj.DATE     = '{YY:04}{MM:02}{DD:02}'.format(YY=now.tm_year, MM=now.tm_mon, DD=now.tm_mday)
    gv.Prj.TIME     = '{HH:02}{MM:02}{SS:02}'.format(HH=now.tm_hour, MM=now.tm_min, SS=now.tm_sec)

    if fDEBUG:
        C.printYellow('.'*10 + __name__ + '.'*10, tab=4)
        C.printCyan('scriptName       {0}'.format(gv.Prj.scriptName), tab=8)
        C.printCyan('prjBaseDIR       {0}'.format(gv.Prj.prjBaseDIR), tab=8)
        C.printCyan('configDIR        {0}'.format(gv.Prj.configDIR), tab=8)
        C.printCyan('dataDIR          {0}'.format(gv.Prj.dataDIR), tab=8)
        C.printCyan('iniFileName      {0}'.format(gv.Prj.iniFileName), tab=8)
        print ()
        C.printCyan('today            {0}'.format(gv.Prj.today), tab=8)
        C.printCyan('DATE - TIME      {0} - {1}'.format(gv.Prj.DATE, gv.Prj.TIME), tab=8)
        C.printCyan('now              {0}'.format(gv.Prj.now), tab=8)
        C.printYellow('.'*10 + __name__ + '.'*10, tab=4)
        print ()




def setupEnv340(gv):
    import pathlib as p         # dalla versione 3.4
    C = gv.Ln.Colors()
        # ------------------------------------------
        # - Preparazione directories
        # ------------------------------------------
    scriptMain  = p.Path(sys.argv[0]).resolve()
    scriptMain  = os.path.abspath(os.path.join(__file__, '../../../'))
    prjBaseDIR  = scriptMain.parent
    scriptName  = scriptMain.name
    prjName     = prjBaseDIR.stem
    scriptExt   = scriptMain.suffix[1:]


    configDIR   = prjBaseDIR.joinpath('conf')
    dataDIR     = prjBaseDIR.joinpath('data')

        # ---------------------------------------------------------
        # - file di configurazione
        # ---------------------------------------------------------
    iniFileName = configDIR.joinpath(gv.Prj.prefix + '_' + gv.Prj.Version + '.ini')


    gv.Prj.scriptName  = str(scriptName)
    gv.Prj.prjBaseDIR  = str(prjBaseDIR)
    gv.Prj.configDIR   = str(configDIR)
    gv.Prj.dataDIR     = str(dataDIR)
    gv.Prj.iniFileName = str(iniFileName)


    now     = time.localtime()
    gv.Prj.now     = now
    gv.Prj.today   = '{YY:04}.{MM:02}.{DD:02}'.format(YY=now.tm_year, MM=now.tm_mon, DD=now.tm_mday)
    gv.Prj.DATE    = '{YY:04}{MM:02}{DD:02}'.format(YY=now.tm_year, MM=now.tm_mon, DD=now.tm_mday)
    gv.Prj.TIME    = '{HH:02}{MM:02}{SS:02}'.format(HH=now.tm_hour, MM=now.tm_min, SS=now.tm_sec)

    if gv.fDEBUG:
        C.printYellow('.'*10 + __name__ + '.'*10, tab=4)
        C.printCyan('scriptName       {0}'.format(gv.Prj.scriptName), tab=8)
        C.printCyan('prjBaseDIR       {0}'.format(gv.Prj.prjBaseDIR), tab=8)
        C.printCyan('configDIR        {0}'.format(gv.Prj.configDIR), tab=8)
        C.printCyan('dataDIR          {0}'.format(gv.Prj.dataDIR), tab=8)
        C.printCyan('iniFileName      {0}'.format(gv.Prj.iniFileName), tab=8)
        print ()
        C.printCyan('today            {0}'.format(gv.Prj.today), tab=8)
        C.printCyan('DATE - TIME      {0} - {1}'.format(gv.Prj.DATE, gv.Prj.TIME), tab=8)
        C.printCyan('now              {0}'.format(gv.Prj.now), tab=8)
        C.printYellow('.'*10 + __name__ + '.'*10, tab=4)
        print ()




