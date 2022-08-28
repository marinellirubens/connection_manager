"""Module to handle utillity methods"""
import re
from typing import Tuple

from config.utils import create_directories
from database.utils import initiate_db
from flask import Flask, request
from flask_cors import CORS
from flask_restful import Api
from flasgger import Swagger

from server import resources
from server.app import App

template = {
    "swagger": "2.0",
    "info": {},
    "host": "localhost",
    "basePath": "api",
    "schemes": ["http"]
}


app: Flask = App('main')


def create_app(app_name: str, database_directory: str = 'sqlite',
               log_dir: str = './logs', directory_files: str = './files') -> Flask:
    """Method to handle requests to the server."""
    create_directories([database_directory, directory_files, log_dir])

    app: Flask = App(app_name)

    CORS(app)
    api = Api(app)

    engine, session = initiate_db(database_directory)
    app.engine = engine
    app.session = session

    basic_methods = ['GET', 'POST', 'OPTIONS']
    individual_methods = ['GET', 'PUT', 'OPTIONS', 'DELETE']

    api.add_resource(resources.DatabaseTypes, '/database_types/', methods=basic_methods)
    api.add_resource(resources.DatabaseType, '/database_types/<id>', methods=individual_methods)

    api.add_resource(resources.ConnectionTypes, '/connection_types/', methods=basic_methods)
    api.add_resource(resources.ConnectionType, '/connection_types/<id>', methods=individual_methods)

    api.add_resource(resources.ServerTypes, '/server_types/', methods=basic_methods)
    api.add_resource(resources.ServerType, '/server_types/<id>', methods=individual_methods)

    api.add_resource(resources.FunctionTypes, '/function_types/', methods=basic_methods)
    api.add_resource(resources.FunctionType, '/function_types/<id>', methods=individual_methods)

    api.add_resource(resources.Groups, '/groups/', methods=basic_methods)
    api.add_resource(resources.Group, '/groups/<id>', methods=individual_methods)

    api.add_resource(resources.Users, '/users/', methods=basic_methods)
    api.add_resource(resources.User, '/users/<id>', methods=individual_methods)

    api.add_resource(resources.UserGroups, '/user_groups/', methods=basic_methods)
    api.add_resource(resources.FunctionPermissions, '/function_permissions/', methods=basic_methods)
    api.add_resource(resources.Databases, '/databases/', methods=basic_methods)

    swagger = Swagger(app, template=template)
    print(swagger)
    return app


def check_requirements(model_class, id) -> Tuple[bool, str]:
    """Checks if the requirement exists

    :param model_class: Model class name
    :type model_class: Callable
    :param id: The id of the model
    :type id: int
    :return: Tuple with the result
    :rtype: tuple
    """
    if not check_if_info_exists(model_class, id)[0]:
        return False, f'{model_class.__name__} not found'

    return True, 'Info exists'


def check_if_info_exists(model, id) -> tuple:
    """Checks if the model exists already

    :param model: model class
    :type model: Base
    :param id: id
    :type id: str
    """
    row = app.session.query(model).\
        where(model.id == id).first()
    if not row:
        return False, None

    return True, row


def password_complexity_check(user, password) -> Tuple[bool, str]:
    """Method to check the complexity of a given password

    :param user: user to validate with password
    :param password: password to be validated
    :return: True if is valid otherwise false
    :rtype: tuple
    """

    if user == password:
        return False, 'User and password cant be the same'

    if len(password.strip()) < 8:
        return False, 'Password needs to be at least 8 characters long'

    if '123456' in password:
        return False, 'Password should not contain sequetial characteres'

    if re.match(r'(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^A-Za-z0-9])(?=.{8,})', password):
        return False, 'Invalid password'

    if password in ['admin', 'password', 'senha']:
        return False, 'Invalid password'

    return True, 'Valid'


def basic_get(session, model_class, request_class_name):
    """Method to handle get requests for type tables."""
    rows = app.session.query(model_class).all()
    app.logger.debug(
        f"[{request.authorization.username}] Returning all {request_class_name} rows")

    resp = {model_class.__tablename__: [row.to_json(session) for row in rows]}
    return resp
