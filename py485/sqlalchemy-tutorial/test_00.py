from sqlalchemy                 import Column, Integer, Float, Date, String, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy                 import create_engine
from sqlalchemy.orm             import sessionmaker
import csv
# import pandas as pd


#def Load_Data(file_name):
    #data = csv.reader(file_name, delimiter=',')# skiprows=1, converters={0: lambda s: str(s)})
    #return data.tolist()

Base = declarative_base()

class cdb1(Base):
    #Tell SQLAlchemy what the table name is and if there's any table-specific arguments it should know about
    __tablename__  = 'cdb2'
    # __table_args__ = {'sqlite_autoincrement': True}
    #tell SQLAlchemy the name of column and its attributes:
    Name           = Column(VARCHAR(40), primary_key = True, nullable = False)
    Address        = Column(Integer)
    Pin_Number     = Column(Integer)
    Status         = Column(VARCHAR)

engine = create_engine('sqlite:///cdb.db')
Base.metadata.create_all(engine)

