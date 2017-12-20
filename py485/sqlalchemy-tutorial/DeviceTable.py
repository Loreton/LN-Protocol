from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy                 import Column, Integer, Float, Date, String, VARCHAR, Sequence
Base = declarative_base()

class Device(Base):
    __tablename__  = 'devices'
    Name           = Column('Name'      ,VARCHAR(40), primary_key = True, nullable = False)
    Address        = Column('Address'   ,Integer)
    Pin_Number     = Column('Pin_Number',Integer)
    Status         = Column('Status'    ,VARCHAR)


        # fld_Name           = Column('Name'      ,VARCHAR(40), primary_key = True, nullable = False)
        # fld_Address        = Column('Address'   ,Integer)
        # fld_Pin_Number     = Column('Pin_Number',Integer)
        # fld_Status         = Column('Status'    ,VARCHAR)