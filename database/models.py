from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Date, ColumnDefault
from sqlalchemy.ext.declarative import declarative_base
from flask import jsonify
import hashlib
from sqlalchemy.orm import Session


Base = declarative_base()


def format_date(date):
    return datetime.strftime(date, '%Y-%m-%d')


class DatabaseTypeModel(Base):
    __tablename__ = 'database_type'
    id = Column(Integer, primary_key=True)
    description = Column(String(50), nullable=False, unique=True)

    def __init__(self, id, description):
        self.id = id
        self.description = description

    def to_json(self):
        return dict(id=self.id, description=self.description)


class ConnectionTypeModel(Base):
    __tablename__ = 'connection_type'
    id = Column(Integer, primary_key=True)
    description = Column(String(50), nullable=False, unique=True)

    def __init__(self, id, description):
        self.id = id
        self.description = description

    def to_json(self):
        return dict(id=self.id, description=self.description)


class ServerTypeModel(Base):
    __tablename__ = 'server_type'
    id = Column(Integer, primary_key=True)
    description = Column(String(50), nullable=False, unique=True)

    def __init__(self, id, description):
        self.id = id
        self.description = description

    def to_json(self):
        return dict(id=self.id, description=self.description)


class FunctionTypeModel(Base):
    __tablename__ = 'function_type'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(255), nullable=False, unique=True)

    def __init__(self, id, description):
        self.id = id
        self.description = description

    def to_json(self):
        return dict(id=self.id, description=self.description)


class GroupModel(Base):
    __tablename__ = 'groups'
    group_id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(255), nullable=False, unique=True)
    creation_date = Column(Date, nullable=False, default=ColumnDefault(datetime.now()))

    def __init__(self, description):
        self.description = description

    def to_json(self):
        return dict(id=self.group_id, description=self.description)


class UserModel(Base):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    creation_date = Column(Date, nullable=False, default=ColumnDefault(datetime.now()))
    update_date = Column(Date, nullable=True, onupdate=ColumnDefault(datetime.now()))

    def __init__(self, name, password):
        self.name = name
        self.password = self.password_hash(password)

    @staticmethod
    def password_hash(password):
        return hashlib.md5(password.encode('utf-8')).hexdigest()

    def validate_password(self, password):
        return self.password == self.password_hash(password)

    def to_json(self):
        user_json = dict(
            user_id=self.user_id,
            name=self.name,
            creation_date=format_date(self.creation_date),
            update_date=format_date(self.update_date)
        )
        
        return user_json


class UserGroupModel(Base):
    __tablename__ = 'user_grp'
    id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(Integer, ForeignKey('groups.group_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)

    def __init__(self, group_id, user_id):
        self.group_id = group_id
        self.user_id = user_id
    
    def to_json(self, session: Session):
        
        group = session.query(GroupModel).filter(GroupModel.user_id == self.group_id).first()
        user = session.query(UserModel).filter(UserModel.user_id == self.user_id).first()
        
        return dict(id=self.id, group_id=group.to_json(), user_id=user.to_json())


class FunctionPermissionsModel(Base):
    __tablename__ = 'function_permissions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(Integer, ForeignKey('groups.group_id'), nullable=False)
    function_id = Column(Integer, ForeignKey('function_type.id'), nullable=False)
    
    def __init__(self, group_id, function_id):
        self.group_id = group_id
        self.function_id = function_id
        
    def to_json(self):
        return dict(id=self.id, group_id=self.group_id, function_id=self.function_id)


class DatabaseModel(Base):
    __tablename__ = 'database'
    database_id = Column(Integer, primary_key=True, autoincrement=True)
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

    def to_json(self):
        return dict(
            database_id=self.database_id,
            description=self.description,
            host=self.host,
            port=self.port,
            sid=self.sid,
            database_type_id=self.database_type_id
        )


class ServerModel(Base):
    __tablename__ = 'server'
    server_id = Column(Integer, primary_key=True, autoincrement=True)
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

    def to_json(self):
        return dict(
            server_id=self.server_id,
            description=self.description,
            host=self.host,
            port=self.port,
            server_type_id=self.server_type_id,
            connection_type=self.connection_type
        )


class ServerPermissionsModel(Base):
    __tablename__ = 'server_permissions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(Integer, ForeignKey('groups.group_id'), nullable=False)
    server_id = Column(Integer, ForeignKey('server.server_id'), nullable=False)


class LoginModel(Base):
    __tablename__ = 'login'
    login_id = Column(Integer, primary_key=True, autoincrement=True)
    user = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    connection_type = Column(Integer, nullable=False)


class ConnectionLoginModel(Base):
    __tablename__ = 'connection_login'
    id = Column(Integer, primary_key=True, autoincrement=True)
    login_id = Column(Integer, ForeignKey('connection_login.login_id'), nullable=False)
    connection_id = Column(Integer, nullable=False)
