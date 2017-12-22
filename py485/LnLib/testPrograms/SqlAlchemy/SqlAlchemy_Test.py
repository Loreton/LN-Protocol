import sys; sys.dont_write_bytecode = True


# - inserimento pathe per la LnLib
from  pathlib import Path
LnLibPath = Path(sys.argv[0]).resolve().parent.parent.parent.parent
sys.path.insert(0, str(LnLibPath))
# -----------------------------------

import  LnLib as Ln
from    LnLib.SQL.LnSqlAlchemy import LnDB as LnDB




import DeviceTable as DT

#-------------------------------------------------
# - import della classe contenente la/le tabbelle
#-------------------------------------------------

if __name__ == '__main__':
    # print (dbFile)
    # sys.exit()
    # print ('sqlite:///' + str(wkdir) + 'LnDB_01.db')

    # db =  Path(sys.argv[0]).resolve().parent / 'LnDB_01.db'
    dbFile = Path(sys.argv[0]).resolve().parent / 'LnDB_01.db'
    myDB   = LnDB(tableClass=DT.Device, url='sqlite:///' + str(dbFile), Base=DT.Base, myDict=Ln.Dict)
    # myDB   = LnDB(tableClass=DT.Device, url='sqlite://', Base=DT.Base, myDict=Ln.Dict)

    # myRec = Ln.LnClass()
    # myRec.Name='server02'; myRec.Address=0x0D; myRec.Pin_Number=6
    # xx = Ln.toDict(myRec)
    # print (xx)

    myRec = Ln.Dict()
    myRec.Name='server02'; myRec.Address=0x0D; myRec.Pin_Number=6
    xx = Ln.toDict(myRec)
    # print (xx)
    # sys.exit()
    # myRec = Ln.Dict()
    # myRec = {'Name': 'server01', 'Address':0x0C, 'Pin_Number':5}
    myDB._insert(myRec.toDict(), commit=True)
    myDB._update(myRec.toDict(), commit=True)

