"""Method to handle requests to the server."""
from flask import Flask
from flask_restful import Api
from database.utils import initiate_db
from server.resources import get_app, DatabaseType, DatabaseTypes
from config.utils import create_directories

app: Flask

def create_app(app_name: str) -> Flask:
    """Method to handle requests to the server."""

    app = get_app(app_name)
    api = Api(app)

    # api.add_resource(Database, '/', methods=['PUT'])
    api.add_resource(DatabaseType,
                     '/database_type/<param>',
                     methods=['GET', 'POST', 'DELETE'])
    api.add_resource(DatabaseTypes, '/database_type/', methods=['GET'])
    return app
