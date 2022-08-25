"""Method to handle the resource for the API"""
import re
from abc import ABC
from typing import Tuple
import json


from database import models
from flask import Flask
from flask import request
from flask_restful import Resource

from server.app import App
from server.authentication import auth


app: Flask = App('main')


# TODO: Implement other verbs on the resources

class BasicTypes(Resource, ABC):
    model_class = None

    @auth.login_required
    def get(self):
        """Method to handle get requests for type tables."""
        rows = app.session.query(self.model_class).all()
        app.logger.debug(
            f"[{request.authorization.username}] Returning all {self.__class__.__name__} rows")

        resp = {self.model_class.__tablename__: [row.to_json() for row in rows]}
        return resp

    @auth.login_required
    def post(self):
        """Method to handle post requests for type tables."""
        data = request.get_data()

        if 'description' not in data:
            return {'error': 'Invalid description provided'}, 401

        row = app.session.query(self.model_class).\
            where(self.model_class.description == data['description']).first()

        if row:
            return dict(
               error=f'{self.model_class.__class__.__name__}: {data["description"]} already exists'
            ), 401

        app.session.bulk_save_objects([self.model_class(data["description"])])
        app.session.commit()

        row = app.session.query(self.model_class).\
            where(self.model_class.description == data['description']).first()

        return {'success': 'Registered successfully', 'id': row.id}

    @auth.login_required
    def options(self):
        """Method to handle options requests for type tables."""
        return dict(Allow=['POST', 'GET'])


class BasicTypeSingle(Resource, ABC):
    """Method to handle post requests for table when specific type requested."""
    model_class = None

    @auth.login_required
    def get(self, id):
        row = app.session.query(self.model_class)\
            .where(self.model_class.id == id).first()

        if not row:
            error_message = f'No information found on {self.__class__.__name__} found'
            app.logger.debug(f'[{request.authorization.username}] {error_message}')

            return dict(error=error_message), 401

        app.logger.debug(
            f'[{request.authorization.username}] '
            f'Returning {self.__class__.__name__} id {id}')
        return row.to_json()

    @auth.login_required
    def put(self, id):
        """Method to handle insert of new type.

        :param param: type description
        :return: type id that was inserted
        """
        row = app.session.query(self.model_class)\
            .where(self.model_class.id == id).first()

        if not row:
            return dict(
                error=f'{self.__class__.__name__} id not exists',
                id=id), 401

        data = json.loads(request.get_data().decode('utf-8'))

        if 'description' not in data:
            return {'error': 'Invalid description provided'}, 401

        row.description = data['description']

        app.session.bulk_save_objects([row])
        app.session.commit()

        message = f"{self.__class__.__name__}:" + \
                  f" {row.id} saved successfully"
        app.logger.debug(f"[{request.authorization.username}] " + message)

        return dict(message=message, register=row.to_json())

    @auth.login_required
    def delete(self, id):
        """Method to handle deleted requests for type tables."""
        row = app.session.query(self.model_class)\
            .where(self.model_class.id == id).first()

        if not row:
            return dict(
                error=f'{self.__class__.__name__} id not exists',
                id=id), 401

        app.session.delete(row)
        app.session.commit()

        return dict(success=f'{id} deleted')

    @auth.login_required
    def options(self, id):
        """Method to handle options requests for type tables."""
        return dict(Allow=['DELETE', 'PUT', 'GET'])


class DatabaseTypes(BasicTypes):
    """Method to handle post requests for database_type table when all lines requested."""
    model_class = models.DatabaseTypeModel


class DatabaseType(BasicTypeSingle):
    """Method to handle post requests for database_type table when specific database type requested.
    """
    model_class = models.DatabaseTypeModel


class ConnectionTypes(BasicTypes):
    """Method to handle post requests for connection_type table when all lines requested."""
    model_class = models.ConnectionTypeModel


class ConnectionType(BasicTypeSingle):
    """Method to handle post requests for connection_type table when specific
    connection type requested.
    """
    model_class = models.ConnectionTypeModel


class ServerTypes(BasicTypes):
    """Method to handle post requests for server_type table when all lines requested."""
    model_class = models.ServerTypeModel


class ServerType(BasicTypeSingle):
    """Method to handle post requests for server_type table when specific
    connection type requested.
    """
    model_class = models.ServerTypeModel


class FunctionTypes(BasicTypes):
    """Method to handle post requests for function_type table when all lines requested."""
    model_class = models.FunctionTypeModel


class FunctionType(BasicTypeSingle):
    """Method to handle post requests for function_type table when specific
    function type requested.
    """
    model_class = models.FunctionTypeModel


class Groups(BasicTypes):
    """Method to handle post requests for groups table when all lines requested."""
    model_class = models.GroupModel


class Group(BasicTypeSingle):
    """Method to handle post requests for groups table when specific group requested."""
    model_class = models.GroupModel


class Users(BasicTypes):
    """Class to handle user requests"""
    model_class = models.UserModel

    @auth.login_required
    def post(self):
        """Method to handle the user insert"""
        name = request.headers.get('name', None)
        password = request.headers.get('password', None)

        if not any([name, password]):
            return {
                'error':
                'parameters not correct you need to inform (name, password, connection_type)'
            }, 400

        row = app.session.query(models.UserModel).\
            where(models.UserModel.name == name)

        if row.count() > 0:
            return dict(
                error=' user name already exists',
                name=name
            ), 401

        password_validation = password_complexity_check(name, password)

        if not password_validation[0]:
            return {
                'error': password_validation[1]
            }, 401

        user = models.UserModel(name, password)
        app.session.bulk_save_objects([user])
        app.session.commit()

        row = app.session.query(models.UserModel).\
            where(models.UserModel.name == name).first()

        return {'success': f'User {name} created.', 'id': row.id}


class User(BasicTypeSingle):
    """Class to handle user single request"""
    model_class = models.UserModel


class UserGroups(BasicTypes):
    """Class to handle user requests"""
    model_class = models.UserGroupModel


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
