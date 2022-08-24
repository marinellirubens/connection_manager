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
    model_class = None

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
    model_class = None

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


class User(BasicTypeSingle):
    """Class to handle user single request"""
    model_class = models.UserModel

    @app.route('/user', methods=['POST'])
    @auth.login_required
    @staticmethod
    def post():
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
    
    if '123456'in password:
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
