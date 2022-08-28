"""Module to contain the database models and related functions."""
import base64
import hashlib
from datetime import datetime

from Crypto.Cipher import AES
from sqlalchemy import Column
from sqlalchemy import ColumnDefault
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session


Base = declarative_base()


def format_date(date: datetime):
    """Formats a date to string so it can be showed on a json response.

    Example:
        >>> format_date(datetime(2020, 8, 21))
        '2020-08-21'

    :param date: Date to be formatted.
    :type date: datetime
    :return: Formatted date.
    :rtype: str
    """
    return datetime.strftime(date, '%Y-%m-%d')


def password_hash(password: str) -> str:
    """Hashes a password, hashs are not reversible, so if you need to reverse after
    use encript_password instead.

    Example:
        >>> password_hash('password')
        '5f4dcc3b5aa765d61d8327deb882cf99'

    :param password: Password to be hashed.
    :type password: str
    :return: Hashed password.
    :rtype: str
    """
    return hashlib.md5(password.encode('utf-8')).hexdigest()


def get_cipher() -> AES:
    """Returns a cipher object to encript and decript passwords.

    :return: Cipher object.
    :rtype: AES
    """
    secret_key = b'connection_manager_key20220821'
    cipher = AES.new(secret_key, AES.MODE_ECB)

    return cipher


def encript_password(password: str) -> bytes:
    """Encripts a password, encripted passwords are reversible, so if you need to
    hash it, use password_hash instead.

    Example:
        >>> encript_password('password')
        'b\\x1d\\x8c\\x97\\x19\\x2f\\xdb\\x28\\xdd\\x3c\\x81\\x99\\x2d\\x02\\xd0\\x5f'

        >>> decript_password(encript_password('password'))
        b'password'

    :param password: Password to be encripted.
    :type password: str
    :return: Encripted password.
    :rtype: bytes
    """
    cipher = get_cipher()

    encoded = base64.encodebytes(cipher.encrypt(password))

    return encoded


def decript_password(password: str) -> bytes:
    """Decripts a password, encripted by encript_password.

    Example:
        >>> password='b\\x1d\\x8c\\x97\\x19\\x2f\\xdb\\x28\\xdd\\x3c\\x81\\x99\\x2d\\x02\\xd0\\x5f'
        >>> decript_password(password)
        b'password'

    :param password: Password to be decripted.
    :type password: str
    :return: Decripted password.
    :rtype: bytes
    """
    cipher = get_cipher()
    decoded = base64.decodebytes(cipher.decrypt(password))

    return decoded


class DatabaseTypeModel(Base):
    __tablename__ = 'database_type'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(50), nullable=False, unique=True)
    creation_date = Column(Date, nullable=False, default=ColumnDefault(datetime.now()))

    def __init__(self, description):
        self.description = description

    def to_json(self, *args, **kwargs):
        return dict(id=self.id, description=self.description,
                    creation_date=format_date(self.creation_date))


class ConnectionTypeModel(Base):
    __tablename__ = 'connection_type'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(50), nullable=False, unique=True)
    creation_date = Column(Date, nullable=False, default=ColumnDefault(datetime.now()))

    def __init__(self, description):
        self.description = description

    def to_json(self, *args, **kwargs):
        return dict(id=self.id, description=self.description,
                    creation_date=format_date(self.creation_date))


class ServerTypeModel(Base):
    __tablename__ = 'server_type'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(50), nullable=False, unique=True)
    creation_date = Column(Date, nullable=False, default=ColumnDefault(datetime.now()))

    def __init__(self, description):
        self.description = description

    def to_json(self, *args, **kwargs):
        return dict(id=self.id, description=self.description,
                    creation_date=format_date(self.creation_date))


class FunctionTypeModel(Base):
    __tablename__ = 'function_type'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(255), nullable=False, unique=True)
    creation_date = Column(Date, nullable=False, default=ColumnDefault(datetime.now()))

    def __init__(self, description):
        self.description = description

    def to_json(self, *args, **kwargs):
        return dict(id=self.id, description=self.description,
                    creation_date=format_date(self.creation_date))


class GroupModel(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(255), nullable=False, unique=True)
    creation_date = Column(Date, nullable=False, default=ColumnDefault(datetime.now()))

    def __init__(self, description):
        self.description = description

    def to_json(self, *args, **kwargs):
        return dict(id=self.id, description=self.description,
                    creation_date=format_date(self.creation_date))


class UserModel(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    creation_date = Column(Date, nullable=False, default=ColumnDefault(datetime.now()))
    update_date = Column(Date, nullable=True, onupdate=ColumnDefault(datetime.now()))

    def __init__(self, name, password):
        self.name = name
        self.password = password_hash(password)

    def validate_password(self, password):
        return self.password == password_hash(password)

    def to_json(self, *args, **kwargs):
        user_json = dict(
            id=self.id,
            name=self.name,
            creation_date=format_date(self.creation_date),
            update_date=format_date(self.update_date)
        )

        return user_json


class UserGroupModel(Base):
    __tablename__ = 'user_grp'
    id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    def __init__(self, group_id, user_id):
        self.group_id = group_id
        self.user_id = user_id

    def to_json(self, session: Session, *args, **kwargs):

        group = session.query(GroupModel).filter(GroupModel.id == self.group_id).first()
        user = session.query(UserModel).filter(UserModel.id == self.user_id).first()

        return dict(id=self.id, group=group.to_json(), user=user.to_json())


class FunctionPermissionsModel(Base):
    __tablename__ = 'function_permissions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    function_id = Column(Integer, ForeignKey('function_type.id'), nullable=False)

    def __init__(self, group_id, function_id):
        self.group_id = group_id
        self.function_id = function_id

    def to_json(self, session: Session, *args, **kwargs):
        group = session.query(GroupModel).filter(GroupModel.id == self.group_id).first()
        function = session.query(FunctionTypeModel).filter(
            FunctionTypeModel.id == self.function_id).first()

        return dict(id=self.id, group=group.to_json(), function=function.to_json())


class DatabaseModel(Base):
    __tablename__ = 'database'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(50), nullable=False)
    host = Column(String(50), nullable=False)
    port = Column(Integer, nullable=False)
    sid = Column(String(50), nullable=False)
    database_type_id = Column(String(50),
                              ForeignKey('database_type.id'),
                              nullable=False)

    def __init__(self, description, host, port, sid, database_type_id):
        self.description = description
        self.host = host
        self.port = port
        self.sid = sid
        self.database_type_id = database_type_id

    @staticmethod
    def get_fields() -> tuple:
        """Function to return fields that should be used on the insert of the model"""
        return ('description', 'host', 'port', 'sid', 'database_type_id')

    @staticmethod
    def get_requirements() -> tuple:
        """Function to return the requirements for the insert"""
        requirements = ((DatabaseTypeModel, 'database_type_id'), )
        return requirements

    def to_json(self, *args, **kwargs):
        return dict(
            id=self.id,
            description=self.description,
            host=self.host,
            port=self.port,
            sid=self.sid,
            database_type_id=self.database_type_id
        )


class ServerModel(Base):
    __tablename__ = 'server'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(50), nullable=False)
    host = Column(String(50), nullable=False)
    port = Column(Integer, nullable=False)
    server_type_id = Column(String(50), ForeignKey('server_type.id'), nullable=False)
    connection_type = Column(Integer, ForeignKey('connection_type.id'), nullable=False)

    def __init__(self, description, host, port, server_type_id, connection_type):
        self.description = description
        self.host = host
        self.port = port
        self.server_type_id = server_type_id
        self.connection_type = connection_type

    def to_json(self, *args, **kwargs):
        return dict(
            id=self.id,
            description=self.description,
            host=self.host,
            port=self.port,
            server_type_id=self.server_type_id,
            connection_type=self.connection_type
        )


class ServerPermissionsModel(Base):
    __tablename__ = 'server_permissions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    server_id = Column(Integer, ForeignKey('server.id'), nullable=False)

    def __init__(self, group_id, server_id):
        self.group_id = group_id
        self.server_id = server_id

    def to_json(self, session: Session, *args, **kwargs):
        group = session.query(GroupModel).filter(GroupModel.user_id == self.group_id).first()
        server = session.query(ServerModel).filter(ServerModel.server_id == self.server_id).first()

        return dict(id=self.id, group=group.to_json(), server=server.to_json())


class LoginModel(Base):
    __tablename__ = 'login'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    connection_type = Column(Integer, nullable=False)

    def __init__(self, user, password, connection_type):
        self.user = user
        self.password = encript_password(password)
        self.connection_type = connection_type

    def to_json(self, *args, **kwargs):
        return dict(
            id=self.id,
            user=self.user,
            password=decript_password(self.password),
            connection_type=self.connection_type
        )


class ConnectionLoginModel(Base):
    __tablename__ = 'connection_login'
    id = Column(Integer, primary_key=True, autoincrement=True)
    login_id = Column(Integer, ForeignKey('login.id'), nullable=False)
    connection_id = Column(Integer, nullable=False)

    def __init__(self, login_id, connection_id):
        self.login_id = login_id
        self.connection_id = connection_id

    def to_json(self, session: Session, *args, **kwargs):
        login = session.query(LoginModel).filter(LoginModel.login_id == self.login_id).first()
        connection = session.query(ServerModel).filter(
            ServerModel.server_id == self.connection_id).first()

        if connection is None:
            connection = session.query(DatabaseModel).filter(
                DatabaseModel.database_id == self.connection_id).first()

        return dict(id=self.id, login=login.to_json(), connection=connection.to_json())
