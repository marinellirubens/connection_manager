from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class DatabaseTypeModel(Base):
    __tablename__ = 'database_type'
    id = Column(Integer, primary_key=True)
    description = Column(String(50), nullable=False)

    def __init__(self, id, description):
        self.id = id
        self.description = description

    def to_json(self):
        return dict(id=self.id, description=self.description)


class ConnectionTypeModel(Base):
    __tablename__ = 'connection_type'
    id = Column(Integer, primary_key=True)
    description = Column(String(50), nullable=False)

    def __init__(self, id, description):
        self.id = id
        self.description = description

    def to_json(self):
        return dict(id=self.id, description=self.description)


class ServerTypeModel(Base):
    __tablename__ = 'server_type'
    id = Column(Integer, primary_key=True)
    description = Column(String(50), nullable=False)

    def __init__(self, id, description):
        self.id = id
        self.description = description

    def to_json(self):
        return dict(id=self.id, description=self.description)


class FunctionTypeModel(Base):
    __tablename__ = 'function_type'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(255), nullable=False)

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


class UserGroupModel(Base):
    __tablename__ = 'user_grp'
    id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(Integer, ForeignKey('groups.group_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)

    def __init__(self, group_id, user_id):
        self.group_id = group_id
        self.user_id = user_id


class FunctionPermissionsModel(Base):
    __tablename__ = 'function_permissions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(Integer, ForeignKey('groups.group_id'), nullable=False)
    function_id = Column(Integer, ForeignKey('function_type.id'), nullable=False)


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


class ServerModel(Base):
    __tablename__ = 'server'
    server_id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(50), nullable=False)
    host = Column(String(50), nullable=False)
    port = Column(Integer, nullable=False)
    server_type_id = Column(String(50), ForeignKey('server_type.id'), nullable=False)
    connection_type = Column(Integer, ForeignKey('connection_type.id'), nullable=False)


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
