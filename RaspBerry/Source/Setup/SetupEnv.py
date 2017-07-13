#!/opt/python3.4/bin/python3.4

import sys, os
import time

def SetupEnv(gv, prjName, fDEBUG=False):
    if gv.Ln.pyVer >= '340':
        # setupEnv340(gv, fDEBUG=False)
        setupEnv300(gv, prjName, fDEBUG=fDEBUG)
    else:
        setupEnv300(gv, prjName, fDEBUG=fDEBUG)

def setupEnv300(gv, prjName, fDEBUG=False):
    cPrint        = gv.Ln.LnColor()
    gv.env        = gv.Ln.LnDict()              # default = _dynamic = False
    gv.env.name   = prjName
    gv.env.prefix = gv.env.name


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
    iniFileName = os.path.abspath(os.path.join(configDIR, gv.env.name + '_config.ini'))


    gv.env.scriptName    = scriptName
    gv.env.prjBaseDIR    = prjBaseDIR
    # gv.env.configDIR     = configDIR
    gv.env.mainConfigDIR = configDIR
    gv.env.dataDIR       = dataDIR
    gv.env.iniFileName   = iniFileName


    now             = time.localtime()
    gv.env.now      = now
    gv.env.today    = '{YY:04}.{MM:02}.{DD:02}'.format(YY=now.tm_year, MM=now.tm_mon, DD=now.tm_mday)
    gv.env.DATE     = '{YY:04}{MM:02}{DD:02}'.format(YY=now.tm_year, MM=now.tm_mon, DD=now.tm_mday)
    gv.env.TIME     = '{HH:02}{MM:02}{SS:02}'.format(HH=now.tm_hour, MM=now.tm_min, SS=now.tm_sec)

    if fDEBUG:
        cPrint.Yellow('.'*10 + __name__ + '.'*10, tab=4)
        cPrint.Cyan('scriptName       {0}'.format(gv.env.scriptName), tab=8)
        cPrint.Cyan('prjBaseDIR       {0}'.format(gv.env.prjBaseDIR), tab=8)
        cPrint.Cyan('configDIR        {0}'.format(gv.env.configDIR), tab=8)
        cPrint.Cyan('dataDIR          {0}'.format(gv.env.dataDIR), tab=8)
        cPrint.Cyan('iniFileName      {0}'.format(gv.env.iniFileName), tab=8)
        print ()
        cPrint.Cyan('today            {0}'.format(gv.env.today), tab=8)
        cPrint.Cyan('DATE - TIME      {0} - {1}'.format(gv.env.DATE, gv.env.TIME), tab=8)
        cPrint.Cyan('now              {0}'.format(gv.env.now), tab=8)
        cPrint.Yellow('.'*10 + __name__ + '.'*10, tab=4)
        print ()




def setupEnv340(gv, fDEBUG=False):
    fDEBUG=True
    import pathlib as p         # dalla versione 3.4
    cPrint = gv.Ln.LnColor()
        # ------------------------------------------
        # - Preparazione directories
        # ------------------------------------------
    scriptMain  = p.Path(sys.argv[0]).resolve()
    print (scriptMain)
    # scriptMain  = os.path.abspath(os.path.join(__file__, '../../../'))
    # print (scriptMain)
    prjBaseDIR  = scriptMain.parent
    scriptName  = scriptMain.name
    prjName     = prjBaseDIR.stem
    scriptExt   = scriptMain.suffix[1:]


    configDIR   = prjBaseDIR.joinpath('conf')
    dataDIR     = prjBaseDIR.joinpath('data')

        # ---------------------------------------------------------
        # - file di configurazione
        # ---------------------------------------------------------
    iniFileName = p.PurePath(configDIR).joinpath(gv.env.prefix + '_config.ini')


    # gv.env.scriptName    = str(scriptName)
    # gv.env.prjBaseDIR    = str(prjBaseDIR)
    # gv.env.mainConfigDIR = str(configDIR)
    # gv.env.dataDIR       = str(dataDIR)
    # gv.env.iniFileName   = str(iniFileName)

    gv.env.scriptName    = scriptName
    gv.env.prjBaseDIR    = prjBaseDIR
    gv.env.mainConfigDIR = configDIR
    gv.env.dataDIR       = dataDIR
    gv.env.iniFileName   = iniFileName


    now     = time.localtime()
    gv.env.now     = now
    gv.env.today   = '{YY:04}.{MM:02}.{DD:02}'.format(YY=now.tm_year, MM=now.tm_mon, DD=now.tm_mday)
    gv.env.DATE    = '{YY:04}{MM:02}{DD:02}'.format(YY=now.tm_year, MM=now.tm_mon, DD=now.tm_mday)
    gv.env.TIME    = '{HH:02}{MM:02}{SS:02}'.format(HH=now.tm_hour, MM=now.tm_min, SS=now.tm_sec)

    if fDEBUG:
        cPrint.Yellow('.'*10 + __name__ + '.'*10, tab=4)
        cPrint.Cyan('scriptName       {0}'.format(gv.env.scriptName), tab=8)
        cPrint.Cyan('prjBaseDIR       {0}'.format(gv.env.prjBaseDIR), tab=8)
        cPrint.Cyan('mainConfigDIR    {0}'.format(gv.env.mainConfigDIR), tab=8)
        cPrint.Cyan('dataDIR          {0}'.format(gv.env.dataDIR), tab=8)
        cPrint.Cyan('iniFileName      {0}'.format(gv.env.iniFileName), tab=8)
        print ()
        cPrint.Cyan('scriptName       {0}'.format(p.PurePosixPath(gv.env.scriptName)), tab=8)
        cPrint.Cyan('prjBaseDIR       {0}'.format(p.PurePosixPath(gv.env.prjBaseDIR)), tab=8)
        cPrint.Cyan('mainConfigDIR    {0}'.format(p.PurePosixPath(gv.env.mainConfigDIR)), tab=8)
        cPrint.Cyan('dataDIR          {0}'.format(p.PurePosixPath(gv.env.dataDIR)), tab=8)
        cPrint.Cyan('iniFileName      {0}'.format(p.PurePosixPath(gv.env.iniFileName)), tab=8)
        print ()
        cPrint.Cyan('today            {0}'.format(gv.env.today), tab=8)
        cPrint.Cyan('DATE - TIME      {0} - {1}'.format(gv.env.DATE, gv.env.TIME), tab=8)
        cPrint.Cyan('now              {0}'.format(gv.env.now), tab=8)
        cPrint.Yellow('.'*10 + __name__ + '.'*10, tab=4)
        print ()




