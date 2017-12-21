from sqlalchemy import create_engine, Column, types
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.sql.expression import literal_column

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    login = Column(types.String(50), primary_key=True)
    name = Column(types.String(255))

    def __repr__(self):
        return "User(login=%r, name=%r)" % (self.login, self.name)




if __name__ == '__main__':

    engine = create_engine('sqlite:///:memory:', echo=False)
    # engine = create_engine('sqlite:///loreto_02.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine);
    session = Session()
    # session = scoped_session(sessionmaker(bind=engine))


    # create two users
    u1 = User(login='someone', name="Some one")
    u2 = User(login='someuser', name="Some User")
    u3 = User(login='user', name="User")
    u4 = User(login='anotheruser', name="Another User")
    session.add(u1)
    session.add(u2)
    session.add(u3)
    session.add(u4)
    session.commit()

    myTable = "User"
    myLogin = literal_column("login")
    myUSER = literal_column("User")
    print("using literal_column")
    print(session.query(User).filter(literal_column("login").in_(["someuser", "someone"])).all())
    print(session.query(User).filter(myLogin.in_(["someuser", "someone"])).all())

    print("using getattr")
    print(session.query(User).filter(getattr(User, "login").in_(["someuser", "someone"])).all())
    print(session.query(User).filter(myLogin.in_(["someuser", "someone"])).all())