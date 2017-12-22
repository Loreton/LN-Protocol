import  sys
import  sqlalchemy                  as sa
import  sqlalchemy.sql              as sql
import  sqlalchemy.orm              as orm
from    sqlalchemy.sql.expression   import literal_column, text as textExpr
from    sqlalchemy.ext.declarative  import declarative_base
from    sqlalchemy_utils            import database_exists, create_database

# from sqlalchemy.sql.expression  import insert
# from sqlalchemy.pool import QueuePool
# from sqlalchemy.orm             import sessionmaker
# exceptions
# from sqlalchemy                 import exc, exists
# from sqlalchemy                 import create_engine


# http://sqlalchemy-utils.readthedocs.io/en/latest/data_types.html

''' http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#declare-a-mapping '''

# class LnClass(): pass


# la devo passare come parametro....
# Base = declarative_base()

#############################################################
# -
#############################################################
class LnDB():
    def __init__(self, url, tableClass, Base, myDict={}, logger=None):
        self._myTable       = tableClass
        self._url           = url
        self._myDict        = myDict

        self._setLogger     = logger if logger else self._setNullLogger


        self._engine        = self._open(Base)
        self._myTableName   = tableClass.__table__
        self._myCol         = tableClass.__table__.columns

            # creaiamo la section
        _Session = orm.sessionmaker(bind=self._engine);
        self._session = _Session()

            # individuiamo la/le primaryKey/s in una LIST
        self._pKeys   = [pk.name for pk in self._myTableName.primary_key]
        # print ('{:<15}{}'.format('pKeys', self._pKeys))

            # -prepara il comando di query sulla tabella
        self._query   = self._session.query(self._myTable)

            # salviamo i nomi delle columns
        self._colName =  self._myTableName.columns.keys()
        # print (self._colName)
        # print (self._myTableName.columns['Name'].name)
        # print (self._myCol['Name'].name)



    ################################
    #  se vogliamo crearlo da un dictionary vedere:
    #     https://gist.github.com/sprin/5846464
    ################################
    def _open(self, Base):
        logger = self._setLogger(__name__)

        logger.info ('... creating db: {}'.format(self._url))
        _engine = sa.create_engine(self._url, echo=False)

        if not database_exists(_engine.url):
            Base.metadata.create_all(_engine)
        else:
            logger.info ('... db already exists')
        logger.info ( 'Database exists: {}'.format(database_exists(_engine.url)))
        return _engine



    ##############################################################################
    # - logger dummy
    ##############################################################################
    def _setNullLogger(self, package=None):
        import inspect
            ##############################################################################
            # - classe che mi permette di lavorare nel caso il logger non sia richiesto
            ##############################################################################
        class nullLogger():
            def __init__(self, package=None, stackNum=1): pass
            def info(self, data):       self._print(data)
            def debug(self, data):      self._print(data)
            def error(self, data):      self._print(data)
            def warning(self, data):    self._print(data)

            def _print(self, data, stackNum=2):
                TAB = 4
                data = '{0}{1}'.format(TAB*' ',data)
                caller = inspect.stack()[stackNum]
                dummy, programFile, lineNumber, funcName, lineCode, rest = caller
                if funcName == '<module>': funcName = '__main__'
                # pkg = package.split('.', 1)[1] + '.' + funcName
                pkg = package.split('.')[-1] + '.' + funcName
                firstStr = "[{FUNC:<25}:{LINENO:4}]".format(FUNC=pkg, LINENO=lineNumber)
                str = "{FIRST:<30} - {DATA}".format(FIRST=firstStr, DATA=data)
                # str = "[{FUNC:<20}:{LINENO}] - {DATA}".format(FUNC=pkg, LINENO=lineNumber, DATA=data)
                print (str)
        return nullLogger()


    ################################
    #
    ################################
    def _Commit(self):
        logger = self._setLogger(__name__)

        try:
            self._session.commit()
            logger.info('committed...')

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
        # colPtr = getattr(self._myTable, keyField['name'])
        colPtr = getattr(self._myCol, keyField['name'])
        _exists = self._session.query(sa.exists().where(colPtr==keyField['value'])).scalar()
        return _exists

    def _keyExists(self, keyName, keyValue):
        # colPtr = getattr(self._myTable, keyName)
        colPtr = getattr(self._myCol, keyName)
        _exists = self._session.query(sa.exists().where(colPtr==keyValue)).scalar()
        return _exists


    #########################################
    # check if record/priKey already exists
    # @TODO: gestire il caso di più chiavi primarie
    #########################################
    def _recExists(self, rec):
        logger = self._setLogger(__name__)

        assert type(rec) == dict
        _exists, record = False, None

        for keyName in self._pKeys:
            keyValue = rec[keyName]
            # keyFieldName = getattr(self._myTable, keyName) # utilizza la classe
            keyFieldName = getattr(self._myCol, keyName)    # preleva dalla table direttamente
            logger.debug('searching for REC: {}=={}'.format(keyFieldName, keyValue))
            _exists = self._session.query(sa.exists().where(keyFieldName==keyValue)).scalar()
            logger.debug('exists: {}'.format(_exists))

                # if exists return record for the spefiic key
            if _exists:
                filterText = textExpr('{}="{}"'.format(keyFieldName.name, keyValue))
                record = self._query.filter(filterText).first()


        return _exists, record
        # return {'exists':_exists, 'record':record}



    ################################
    # convert to dictionary
    ################################
    def _toDict(self, data):
        assert type(data) == self._myDict or type(data) == dict

        dataDict = data
        if isinstance(data, self._myDict):
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
    def _insert(self, myRec, commit=False, replace=False):
        logger = self._setLogger(__name__)
        assert type(myRec) == dict

            # -------------------------------------------
            # - searching the primary-key
            # - skip if its value already exists
            # -------------------------------------------
        logger.debug('processing record: {}'.format(myRec))

        (_exists, existingRecord) = self._recExists(myRec)

        if _exists and replace:
            logger.debug('record exists... REPLACE was required.')
            for (key, value) in myRec.items():
                    # - skip primary keys field
                if key in self._pKeys: continue
                # if hasattr(self._myTable, key):
                if hasattr(self._myCol, key):
                    setattr(existingRecord, key, value)

            if commit: self._session.commit()

        elif not _exists:
            logger.debug("doesn't exists, inserting it")
                # -------------------------
                # unpack dictionary
                # and add Record
                # -------------------------
            mydata = self._myTable(**myRec)
            self._session.add(mydata)
            if commit: self._session.commit()

        else:
            logger.debug('record exists bat no action has been taken')



