
from config.utils import create_directories
from database.utils import initiate_db
from flask import Flask
from flask_restful import Api

from server import resources
from server.app import App
    

def create_app(app_name: str, database_directory: str = 'sqlite',
               log_dir: str = './logs', directory_files: str = './files') -> Flask:
    """Method to handle requests to the server."""
    create_directories([database_directory, directory_files, log_dir])

    app = App(app_name)
    api = Api(app)

    engine, session = initiate_db(database_directory)
    app.engine = engine
    app.session = session

    api.add_resource(resources.DatabaseType,
                     '/database_type/<param>',
                     methods=['GET', 'POST', 'DELETE'])
    api.add_resource(resources.DatabaseTypes, '/database_types/', methods=['GET'])

    api.add_resource(resources.ConnectionTypes, '/connection_types/', methods=['GET'])
    api.add_resource(resources.ConnectionType, '/connection_type/<param>', methods=['GET', 'POST'])

    api.add_resource(resources.ServerTypes, '/server_types/', methods=['GET'])
    api.add_resource(resources.ServerType, '/server_type/<param>', methods=['GET', 'POST'])

    api.add_resource(resources.FunctionTypes, '/function_types/', methods=['GET'])
    api.add_resource(resources.FunctionType, '/function_type/<param>', methods=['GET', 'POST'])

    api.add_resource(resources.Groups, '/groups/', methods=['GET'])
    api.add_resource(resources.Group, '/group/<param>', methods=['GET', 'POST'])

    api.add_resource(resources.Users, '/users/', methods=['GET'])
    api.add_resource(resources.User, '/user/<param>', methods=['GET', 'OPTIONS'])
    
    api.add_resource(resources.UserGroups, '/user_groups/', methods=['GET'])

    return app
