import sys

from sqlalchemy.sql             import table, column, select
# from sqlalchemy.sql.expression  import insert

# from sqlalchemy.pool import QueuePool
# from sqlalchemy.orm             import sessionmaker
# import csv

# exceptions
import  sqlalchemy              as sa
from sqlalchemy                 import exc, exists
from sqlalchemy                 import Column, Integer, Float, Date, String, VARCHAR, Sequence
from sqlalchemy                 import create_engine

# sessions
from sqlalchemy.orm             import sessionmaker

# creation
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression  import literal_column, text

# http://sqlalchemy-utils.readthedocs.io/en/latest/data_types.html
from sqlalchemy_utils import database_exists, create_database

Base = declarative_base()
''' http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#declare-a-mapping '''

class LnClass(): pass



#############################################################
# -
#############################################################
class LnDB():
    def __init__(self, tableClass, url, myDict=LnClass):
        self._myTable     = tableClass
        self._url       = url
        self._engine    = self._open()
        self._myTableName = tableClass.__table__

            # creaiamo la section
        _Session = sessionmaker(bind=self._engine);
        self._session = _Session()

            # individuiamo la/le primaryKey/s in una LIST
        self._pKeys   = [pk.name for pk in self._myTableName.primary_key]
            # -prepara il comando di query sulla tabella
        self._query   = self._session.query(self._myTable)
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
    def _keyExists2(self, keyField):
        assert type(keyField) == dict
        colPtr = getattr(self._myTable, keyField['name'])
        _exists = self._session.query(sa.exists().where(colPtr==keyField['value'])).scalar()
        return _exists

    def _keyExists(self, keyName, keyValue):
        colPtr = getattr(self._myTable, keyName)
        _exists = self._session.query(sa.exists().where(colPtr==keyValue)).scalar()
        return _exists


    #########################################
    # check if record/priKey already exists
    # @TODO: gestire il caso di più chiavi primarie
    #########################################
    def _recExists(self, rec):
        '''
        _exists = False
        for keyName, keyValue in rec.items():
            if keyName in self._pKeys:
                keyFieldName = getattr(self._myTable, keyName)
                foo_col      = sqlalchemy.sql.column(keyName)
                print ('...........', keyFieldName.name, keyName, foo_col)
                _exists = self._session.query(exists().where(keyFieldName==keyValue)).scalar()
                if _exists:
                    for server in self._query.filter_by(Name="server01"): # OK
                         print (server.Name)
                         print (server.Address)
                         # ...
                    print ('{}="{}"'.format(keyFieldName.name, 'server01'))
                    for server in self._query.filter(text('{}="{}"'.format(keyFieldName.name, keyValue))): # OK
                         print (server.Name)
                         print (server.Address)

                    filterText = text('{}="{}"'.format(keyFieldName.name, keyValue))
                    for server in self._query.filter(filterText): # OK
                         print (server.Name)
                         print (server.Address)

                    sys.exit()

        '''

        _exists, record = False, None
        for keyName in self._pKeys:
            keyValue = rec[keyName]
            keyFieldName = getattr(self._myTable, keyName)
            print ('...........', keyFieldName.name, keyName)
            _exists = self._session.query(sa.exists().where(keyFieldName==keyValue)).scalar()

                # if exists return record for the spefiic key
            if _exists:
                filterText = text('{}="{}"'.format(keyFieldName.name, keyValue))
                record = self._query.filter(filterText).first()
                # print (record)
                # print (record.Name)

                ''' formato con valori diretti delle colonne
                for server in self._query.filter(filterText): # OK
                     print (server.Name)
                     print (server.Address)

                for server in self._query.filter_by(Name="server01"): # OK
                     print (server.Name)
                     print (server.Address)
                     # ...
                '''




        return _exists, record
        # return {'exists':_exists, 'record':record}



    ################################
    # convert to dictionary
    ################################
    def _toDict(self, data):
        assert type(data) == LnClass or type(data) == dict

        dataDict = data
        if isinstance(data, LnClass):
            dataDict = {}
            for item in vars(data):
                dataDict[item] = getattr(data, item)

        return dataDict

    ################################
    # update...
    ################################
    def _update(self, rec, commit=False):
        self._insert(rec, commit=commit, replace=True)



    ################################
    # insertNewRecord
    ################################
    def _insert(self, rec, commit=False, replace=False):
        assert type(rec) == LnClass or type(rec) == dict

            # - trasportiamo tutto in dict per gestirlo meglio
        myRec = self._toDict(rec)

            # -------------------------------------------
            # - searching the primary-key
            # - skip if its value already exists
            # -------------------------------------------
        (_exists, record) = self._recExists(myRec)

        if _exists and replace:
            print ('updating record')
            for (key, value) in myRec.items():
                    # - skip primary keys field
                if key in self._pKeys: continue
                if hasattr(self._myTable, key):
                    setattr(record, key, value)

            if commit: self._session.commit()

        elif not _exists:
            print ('inserting new record')
                # -------------------------
                # unpack dictionary
                # and add Record
                # -------------------------
            mydata = self._myTable(**myRec)
            self._session.add(mydata)
            if commit: self._session.commit()

        else:
            print ('record exists bat no action has been taken.')

        '''
        if not _exists:
            print ('inserting new record')
                # -------------------------
                # unpack dictionary
                # and add Record
                # -------------------------
            mydata = self._myTable(**myRec)
            self._session.add(mydata)
                # oppure....
            # connection.execute(self._myTable.insert(), [myRec])
            if commit: self._session.commit()

        else:  # udpate the columns
            print ('updating record')
            for (key, value) in myRec.items():
                    # - skip primary keys field
                if key in self._pKeys: continue
                if hasattr(self._myTable, key):
                    setattr(record, key, value)

            if commit: self._session.commit()
        '''









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
    myRec.Name='server02'; myRec.Address=0x0D; myRec.Pin_Number=6
    # myRec = {'Name': 'server01', 'Address':0x0C, 'Pin_Number':5}
    myDB._insert(myRec, commit=True)
    myDB._update(myRec, commit=True)

    # Session = sessionmaker(bind=engine);
    # session = Session()
    # addRecs(session)

    # http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#creating-a-session

