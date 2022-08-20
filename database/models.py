from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
from enum import Enum, auto


Base = declarative_base()
# db = SQLAlchemy()

class ConnectionEnum(Enum):
    LINUX = auto()
    WINDOWS = auto()
    MAC = auto()


class DatabaseEnum(Enum):
    ORACLE = auto()
    MYSQL = auto()
    POSTGRES = auto()
    SQLITE = auto()
    MONGODB = auto()
    REDIS = auto()
    MSSQL = auto()


class DatabaseTypeModel(Base):
    __tablename__ = 'database_type'
    id = Column(Integer, primary_key=True)
    description = Column(String(50), nullable=False)

    def __init__(self, id, description):
        self.id = id
        self.description = description    

    def to_json(self):
        return dict(id=self.id, description=self.description)

class ConnectionType(Base):
    __tablename__ = 'connection_type'
    id = Column(Integer, primary_key=True)
    description = Column(String(50), nullable=False)

    def __init__(self, id, description):
        self.id = id
        self.description = description 


class Server(Base):
    __tablename__ = 'server'
    id = Column(Integer, primary_key=True)
    description = Column(String(50), nullable=False)
    host = Column(String(50), nullable=False)
    port = Column(Integer, nullable=False)
    platform = Column(String(50), nullable=False)
    connection_type = Column(Integer, ForeignKey('connection_type.id'), nullable=False)


class Database(Base):
    __tablename__ = 'database'
    id = Column(Integer, primary_key=True)
    description = Column(String(50), nullable=False)
    host = Column(String(50), nullable=False)
    port = Column(Integer, nullable=False)
    sid = Column(String(50), nullable=False)
    database_type = Column(String(50), ForeignKey('database_type.id'), nullable=False)


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    description = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    user_type = Column(String(50), nullable=False)
    related_connection_id = Column(Integer, nullable=False)


def insert_types(session: scoped_session):
    objects = []
    for item in DatabaseEnum:
        if session.query(DatabaseTypeModel).where(DatabaseTypeModel.id == item.value).count() > 0:
            continue
        objects.append(DatabaseTypeModel(item.value, item.name))

    session.bulk_save_objects(objects)            
    session.commit()

    objects.clear()
    for item in ConnectionEnum:
        if session.query(ConnectionType).where(ConnectionType.id == item.value).count() > 0:
            continue
        objects.append(ConnectionType(item.value, item.name))

    session.bulk_save_objects(objects)            
    session.commit()


def initiate_db():
    """Method to initiate the sqlit database using sqlalchemy."""
    engine = create_engine('sqlite:///./database/api.db', echo=True)
    session = sessionmaker(bind=engine, autocommit=False, autoflush=False)()
    Base.metadata.create_all(engine)

    insert_types(session=session)
    return engine, session
