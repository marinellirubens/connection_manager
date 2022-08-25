
from config.utils import create_directories
from database.utils import initiate_db
from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from server import resources
from server.app import App


def create_app(app_name: str, database_directory: str = 'sqlite',
               log_dir: str = './logs', directory_files: str = './files') -> Flask:
    """Method to handle requests to the server."""
    create_directories([database_directory, directory_files, log_dir])

    app = App(app_name)
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

    return app
