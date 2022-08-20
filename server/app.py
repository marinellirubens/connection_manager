"""Method to handle requests to the server."""
from flask import Flask
from flask_restful import Api
from database.utils import initiate_db
from server.resources import get_app, DatabaseType, DatabaseTypes
from config.utils import create_directories


def create_app(app_name: str, database_directory: str = 'sqlite',
               log_dir: str = './logs', directory_files: str = './files') -> Flask:
    """Method to handle requests to the server."""
    create_directories([database_directory, directory_files, log_dir])

    app = get_app(app_name)
    api = Api(app)

    engine, session = initiate_db(database_directory)
    app.engine = engine
    app.session = session

    api.add_resource(DatabaseType,
                     '/database_type/<param>',
                     methods=['GET', 'POST', 'DELETE'])
    api.add_resource(DatabaseTypes, '/database_type/', '/', methods=['GET'])
    return app
