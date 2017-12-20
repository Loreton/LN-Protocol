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


def createDB():
    global Device, User
    class Device(Base):
        __tablename__  = 'devices'
        Name           = Column(VARCHAR(40), primary_key = True, nullable = False)
        Address        = Column(Integer)
        Pin_Number     = Column(Integer)
        Status         = Column(VARCHAR)


    class User(Base):
        __tablename__ = 'users'
        id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
        ''' comodo se si vogliono inserire più record con gli stessi valori '''
        name     = Column(String(50))
        fullname = Column(String(50))
        password = Column(String(12))

        def __repr__(self):
            return "<User(name='%s', fullname='%s', password='%s')>" % (
                                    self.name, self.fullname, self.password)

    engine = create_engine('sqlite:///loreto_01.db')
    if not database_exists(engine.url):
        print ('... creating db')
        Base.metadata.create_all(engine)
    else:
        print ('... db already exists')
    print(database_exists(engine.url))

    return engine



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
def Commit(session):
    try:
        session.commit()

    except Exception as ex:
        session.rollback()
        print (ex.__class__)
        print (str(ex))
        sys.exit()


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


if __name__ == '__main__':
    engine = createDB()

    Session = sessionmaker(bind=engine);
    session = Session()
    addRec(session, table=Device, commit=True)
    # addRecs(session)

    # http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#creating-a-session

'''



# --------------------------------------------------------------
# - http://docs.sqlalchemy.org/en/latest/core/engines.html
Base.metadata.create_all(myDB)
# To use a SQLite :memory: database, specify an empty URL:
# --------------------------------------------------------------
# engineMem = create_engine('sqlite://', encoding='latin1', echo=True)
# engineMem = create_engine('sqlite://',  echo=True, poolclass=QueuePool)
# Base.metadata.create_all(engineMem)

# t = table('t', column('x'))
# s = select([t]).where(t.c.x == 5)
# print s.compile(compile_kwargs={"literal_binds": True})

table='cdb2'
connection = engineMem.connect()
table.insert().values([
                    {"Name": "some name"},
                    {"Name": "some other name"},
                    {"Name": "yet another name"},
                ])


result = connection.execute("select Name from cdb2")
for row in result:
    print("Name:", row['Name'])
connection.close()
'''

# --------------------------------------------------------------
# - http://docs.sqlalchemy.org/en/latest/core/engines.html
# engine = create_engine('sqlite:///cdb.db')
# To use a SQLite :memory: database, specify an empty URL:
# --------------------------------------------------------------
# engineMem = create_engine('sqlite://', encoding='latin1', echo=True)



