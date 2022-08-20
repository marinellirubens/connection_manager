from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from enum import Enum, auto

import database.models as models


class ServerTypeEnum(Enum):
    LINUX = auto()
    WINDOWS = auto()
    MAC = auto()


class ConnectionTypeEnum(Enum):
    SSH = auto()
    RDP = auto()
    SFTP = auto()
    FTP = auto()


class DatabaseEnum(Enum):
    ORACLE = auto()
    MYSQL = auto()
    POSTGRES = auto()
    SQLITE = auto()
    MONGODB = auto()
    REDIS = auto()
    MSSQL = auto()


class FunctionTypeEnum(Enum):
    CREATE_GROUP = auto()
    MODIFY_GROUP = auto()
    DELETE_GROUP = auto()
    CREATE_USER = auto()
    MODIFY_USER = auto()
    DELETE_USER = auto()
    CREATE_DATABASE = auto()
    MODIFY_DATABASE = auto()
    DELETE_DATABASE = auto()
    CREATE_SERVER = auto()
    MODIFY_SERVER = auto()
    DELETE_SERVER = auto()
    CREATE_TYPES = auto()
    MODIFY_TYPES = auto()
    DELETE_TYPES = auto()
    CREATE_LOGIN = auto()
    MODIFY_LOGIN = auto()
    DELETE_LOGIN = auto()


def populate_type_table(session, table, enum):
    """Method to populate the type tables."""
    objects = []
    for item in enum:
        if session.query(table).where(table.id == item.value).count() > 0:
            continue
        objects.append(table(item.value, item.name))

    session.bulk_save_objects(objects)
    session.commit()


def insert_types(session: scoped_session):
    populate_type_table(session, models.ServerTypeModel, ServerTypeEnum)
    populate_type_table(session, models.ConnectionTypeModel, ConnectionTypeEnum)
    populate_type_table(session, models.DatabaseTypeModel, DatabaseEnum)
    populate_type_table(session, models.FunctionTypeModel, FunctionTypeEnum)


def initiate_db():
    """Method to initiate the sqlit database using sqlalchemy."""
    engine = create_engine('sqlite:///./sqlite/api.db', echo=True)
    session = sessionmaker(bind=engine, autocommit=False, autoflush=False)()
    models.Base.metadata.create_all(engine)

    insert_types(session=session)
    return engine, session
