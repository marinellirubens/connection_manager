"""Method to handle the resource for the API"""
# import os
# import uuid

import re
from abc import abstractmethod
from typing import Tuple

from database import models
from flask import Flask
from flask import jsonify
from flask import request
# from flask import Response, request, send_file
from flask_restful import Resource
from sqlalchemy import func

from server.app import App
from server.authentication import auth


app: Flask = App('main')


# TODO: Implement other verbs on the resources

class BasicTypes(Resource):
    @abstractmethod
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.model_class = None

    @auth.login_required
    def get(self):
        """Method to handle get requests for type tables."""
        rows = app.session.query(self.model_class).all()
        app.logger.debug(
            f"[{request.authorization.username}] Returning all {self.__class__.__name__} rows")

        resp = {self.model_class.__tablename__: [row.to_json() for row in rows]}
        return resp


class BasicTypeSingle(Resource):
    """Method to handle post requests for table when specific type requested."""
    @abstractmethod
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.model_class = None

    @auth.login_required
    def get(self, param):
        row = app.session.query(self.model_class)\
            .where(self.model_class.id == param)

        if row.count() == 0:
            error_message = f'No information found on {self.__class__.__name__} found'
            app.logger.debug(f'[{request.authorization.username}] {error_message}')

            return jsonify(error=error_message), 401

        app.logger.debug(
            f'[{request.authorization.username}] '
            f'Returning {self.__class__.__name__} id {param}')
        return row[0].to_json()

    @auth.login_required
    def post(self, param):
        """Method to handle insert of new type.

        :param param: type description
        :return: type id that was inserted
        """
        row = app.session.query(self.model_class)\
            .where(self.model_class.description == param)

        if row.count() > 0:
            return jsonify(
                error=f'[{request.authorization.username}] '
                      f'{self.__class__.__name__} id already exists',
                id=row[0].id), 401

        max_id = app.session.query(func.max(self.model_class.id))[0]
        next_id = int(max_id[0]) + 1
        app.session.bulk_save_objects([self.model_class(next_id, param)])
        app.session.commit()

        message = f"{self.__class__.__name__}:" + \
                  f" {next_id} created successfully"
        app.logger.debug(f"[{request.authorization.username}] " + message)

        return jsonify(message=message, database_id=next_id)


class DatabaseTypes(BasicTypes):
    """Method to handle post requests for database_type table when all lines requested."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.model_class = models.DatabaseTypeModel


class DatabaseType(BasicTypeSingle):
    """Method to handle post requests for database_type table when specific database type requested.
    """
    @abstractmethod
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.model_class = models.DatabaseTypeModel


class ConnectionTypes(BasicTypes):
    """Method to handle post requests for connection_type table when all lines requested."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.model_class = models.ConnectionTypeModel


class ConnectionType(BasicTypeSingle):
    """Method to handle post requests for connection_type table when specific
    connection type requested.
    """
    @abstractmethod
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.model_class = models.ConnectionTypeModel


class ServerTypes(BasicTypes):
    """Method to handle post requests for server_type table when all lines requested."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.model_class = models.ServerTypeModel


class ServerType(BasicTypeSingle):
    """Method to handle post requests for server_type table when specific
    connection type requested.
    """
    @abstractmethod
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.model_class = models.ServerTypeModel


class FunctionTypes(BasicTypes):
    """Method to handle post requests for function_type table when all lines requested."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.model_class = models.FunctionTypeModel


class FunctionType(BasicTypeSingle):
    """Method to handle post requests for function_type table when specific
    function type requested.
    """
    @abstractmethod
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.model_class = models.FunctionTypeModel


class Groups(BasicTypes):
    """Method to handle post requests for groups table when all lines requested."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.model_class = models.GroupModel


class Group(BasicTypeSingle):
    """Method to handle post requests for groups table when specific group requested."""
    @abstractmethod
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.model_class = models.GroupModel


class Users(BasicTypes):
    """Class to handle user requests"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.model_class = models.UserModel


class UserGroups(BasicTypes):
    """Class to handle user requests"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.model_class = models.UserGroupModel


'''
class Teste(Resource):
    """Class to handle requests to the server."""
    @auth.login_required
    def get(self, file_id=None) -> Response:
        """Method to handle requests to the server."""
        if not os.path.exists(os.path.join('files', file_id)):
            return {'error': 'file not found'}, 404

        return send_file(
            path_or_file=open(os.path.join('files', file_id), 'rb'),
            download_name=file_id,
            mimetype='image/png')

    @auth.login_required
    def post(self) -> Response:
        """Method to handle requests to the server."""
        request_data = request.files['teste']
        file_id = str(uuid.uuid4())
        request_data.save(os.path.join('files', file_id))
        return {'file_id': file_id}, 200

    @auth.login_required
    def delete(self, file_id) -> Response:
        if not os.path.exists(os.path.join('files', file_id)):
            return {'error': 'file not found'}, 404

        os.remove(os.path.join('files', file_id))
        return {'message': 'file deleted'}, 200
'''
