import sys

from sqlalchemy.sql             import table, column, select
# from sqlalchemy.sql.expression  import insert

# from sqlalchemy.pool import QueuePool
# from sqlalchemy.orm             import sessionmaker
# import csv

# exceptions
from sqlalchemy                 import exc

# sessions
from sqlalchemy.orm             import sessionmaker

# creation
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy                 import Column, Integer, Float, Date, String, VARCHAR, Sequence
from sqlalchemy                 import create_engine

# http://sqlalchemy-utils.readthedocs.io/en/latest/data_types.html
from sqlalchemy_utils import database_exists, create_database

Base = declarative_base()
''' http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#declare-a-mapping '''

class LnClass(): pass

class LnDB():
    def __init__(self, tableClass, url, myDict=LnClass):
        self._myTable     = tableClass
        self._url       = url
        self._engine    = self._open()
        self._myTableName = tableClass.__table__
        # for attr in vars(tableClass):
        #     if not attr.startswith('_'):
        #         print (name)
        #         name = '_' + attr
        #         eval(self.name = attr)


            # creaiamo la section
        _Session = sessionmaker(bind=self._engine);
        self._session = _Session()

            # individuiamo la/le primaryKey/s in una LIST
        self._pKeys   = [pk.name for pk in self._myTableName.primary_key]
            # salviamo i nomi delle columns
        self._colName =  self._myTableName.columns.keys()

    ################################
    #
    ################################
    def _open(self):
        _engine = create_engine(self._url)
        if not database_exists(_engine.url):
            print ('... creating db')
            Base.metadata.create_all(_engine)
        else:
            print ('... db already exists')
        print(database_exists(_engine.url))
        return _engine



    ################################
    #
    ################################
    def _Commit(self):
        try:
            self._session.commit()

        except Exception as ex:
            self._session.rollback()
            print (ex.__class__)
            print (str(ex))
            sys.exit()


    ################################
    #
    ################################
    def _keyExists(self, keyField):
        assert type(keyField) == dict
        colPtr = getattr(self._myTable, keyField['name'])
        _exists = self._session.query(exists().where(colPtr==keyField['value'])).scalar()
        return _exists

    def _keyExists(self, keyName, keyValue):
        colPtr = getattr(self._myTable, keyName)
        _exists = self._session.query(exists().where(colPtr==keyValue)).scalar()
        return _exists


    ################################
    #
    ################################
    def _addRec(self, rec, commit=False):
        from sqlalchemy import exists
        assert type(rec) == LnClass or type(rec) == dict

            # - trasportiamo tutto in dict per gestirlo meglio
        myRec = rec
        if isinstance(rec, LnClass):
            myRec = {}
            for item in vars(rec):
                # print (item, getattr(rec,item))
                myRec[item] = getattr(rec,item)

        elif isinstance(rec, dict):
            pass


            # - skip if REC-primary-key already exists
        _exists = False
        for colName, colValue in myRec.items():
            if colName in self._pKeys:
                # _exists = self._keyExists(colName, colValue)
                _exists = self._keyExists( keyField={'name':colName, 'value':colValue} )


        if not _exists:
                # unpack dictionary
            mydata = self._myTable(**myRec)
            self._session.add(mydata)

                # oppure....
            connection.execute(self._myTable.insert(), [myRec])

            if commit: self._session.commit()
            # for (key, value) in dynamic_cols.items():
            #     if hasattr(table, key):
            #         setattr(col_info, key, value)


        # connection.execute(table.insert(), [
        #         {'id':'12','name':'a','lang':'eng'},
        #         {'id':'13','name':'b','lang':'eng'},
        #         {'id':'14','name':'c','lang':'eng'},
        #     ]
        # )


            print (item, myRec[item])

    ################################
    #
    ################################
    def _update(self, rec, commit=False):
        pass
        # https://stackoverflow.com/questions/23152337/how-to-update-sqlalchemy-orm-object-by-a-python-dict





################################
#
################################
def getPriKeys(myTable):
    tblName = myTable.__table__
    METODO = 3

    if METODO == 1:
        pKeys = list(tblName.primary_key)
        for key in pKeys:
            print ('primary Key: {}'.format(key.name))
        print()

    elif METODO == 2:
        pKeys = [pk.name for pk in tblName.primary_key]
        for key in pKeys:
            print ('primary Key: {}'.format(key))
        print()

    else:
        from sqlalchemy import Table, MetaData
        # METODO3
        # https://stackoverflow.com/questions/44089396/get-primary-key-column-name-from-table-in-sqlalchemy-core
        meta  = MetaData()
        tablePtr = Table(tblName, meta, autoload=True, autoload_with=engine)
        # pKeys    = tablePtr.primary_key.columns.values()
        pKeys = [pk.name for pk in tablePtr.primary_key.columns.values()]
        for key in pKeys:
            print ('primary Key: {}'.format(key))
        print()

    return pKeys






################################
#
################################
def addRec(session, table, commit=False):
    priKey = getPriKeys(table)
    from sqlalchemy import exists

    ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')
    session.add(ed_user)

    # verify the record whith the same key is present
    # https://stackoverflow.com/questions/12748926/sqlalchemy-check-if-object-is-already-present-in-table
    pKeyExists1 = session.query(exists().where(table.Name=='server01')).scalar()
    # for key in priKey:
    #     q = session.query(table[key]).filter(table[key]=='server01')
    #     pKeyExists1 = session.query(q.exists()).scalar()    # returns True or False

    # pKeyExists2 = session.query(Device).filter_by(x=Device.Name).count() == 0
    # pKeyExists = session.query(Devices).filter_by(x=Devices.Name, y=item.y).count() == 0

    # print('{:<12}: {}'.format("q",      q))
    print('{:<12}: {}'.format("pKeyExists1", pKeyExists1))
    # print('{:<12}: {}'.format("pKeyExists2", pKeyExists2))
    if not pKeyExists1:    # returns True or False
        device = table(Name='server01', Address=0x0C, Pin_Number=5 )
        session.add(device)

    if commit: Commit(session)


################################
#
################################
def addRecs(session):
    session.add_all([
                    User(name='wendy', fullname='Wendy Williams', password='foobar'),
                    User(name='mary', fullname='Mary Contrary', password='xxg527'),
                    User(name='fred', fullname='Fred Flinstone', password='blah')
                ])



from DeviceTable import Device

if __name__ == '__main__':

    class Device2(Base):
        __tablename__  = 'devices'
        Name           = Column('Name'      ,VARCHAR(40), primary_key = True, nullable = False)
        Address        = Column('Address'   ,Integer)
        Pin_Number     = Column('Pin_Number',Integer)
        Status         = Column('Status'    ,VARCHAR)

        # fld_Name           = Column('Name'      ,VARCHAR(40), primary_key = True, nullable = False)
        # fld_Address        = Column('Address'   ,Integer)
        # fld_Pin_Number     = Column('Pin_Number',Integer)
        # fld_Status         = Column('Status'    ,VARCHAR)


    myDB = LnDB(Device, 'sqlite:///LnDB_01.db')
    myRec = LnClass()
    myRec.Name='server01'; myRec.Address=0x0C; myRec.Pin_Number=5
    # myRec = {'Name': 'server01', 'Address':0x0C, 'Pin_Number':5}
    myDB._addRec(myRec, commit=True)

    # Session = sessionmaker(bind=engine);
    # session = Session()
    # addRecs(session)

    # http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#creating-a-session

