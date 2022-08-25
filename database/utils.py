from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from enum import Enum, auto

import database.models as models
import os


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
        objects.append(table(item.name))

    session.bulk_save_objects(objects)
    session.commit()


def insert_admin_login(session):
    """Method to insert the admin login into the database."""
    admin_group = models.GroupModel(description='admin')
    admin_user = models.UserModel(name='admin', password='admin')
    admin_user_group = models.UserGroupModel(group_id=1, user_id=1)
    session.bulk_save_objects([admin_user, admin_group, admin_user_group])
    session.commit()


def insert_types(session: scoped_session):
    populate_type_table(session, models.ServerTypeModel, ServerTypeEnum)
    populate_type_table(session, models.ConnectionTypeModel, ConnectionTypeEnum)
    populate_type_table(session, models.DatabaseTypeModel, DatabaseEnum)
    populate_type_table(session, models.FunctionTypeModel, FunctionTypeEnum)

    insert_admin_login(session)


def initiate_db(database_directory: str = 'sqlite') -> tuple:
    """Method to initiate the sqlit database using sqlalchemy."""
    database_destination = os.path.join(database_directory, 'api.db')

    poputate_database = False
    if not os.path.exists(database_destination):
        poputate_database = True

    engine = create_engine(f'sqlite:///{database_destination}', echo=False,
                           connect_args={'check_same_thread': False})
    session = sessionmaker(bind=engine, autocommit=False, autoflush=False)()

    # only populate the database if it is a new one
    if poputate_database:
        models.Base.metadata.create_all(engine)
        insert_types(session=session)

    return engine, session
