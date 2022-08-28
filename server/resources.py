"""Method to handle the resource for the API"""
from abc import ABC
import json

from database import models
from flask import Flask
from flask import request
from flask_restful import Resource

from server.app import App
from server.authentication import auth
from server import utils


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
        data = json.loads(request.get_data().decode('utf-8'))

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

    @auth.login_required
    def get(self):
        """Method to handle get of database types.
        ---
        security:
          - basicAuth: []

        definitions:
          DatabaseType:
            type: object
            properties:
              id:
                type: integer
                description: Id of the database type
              description:
                type: string
                description: Database type description
              creation_date:
                type: string
                description: Database type creation date
        responses:
          '200':
            description: A list of the database types
            schema:
              $ref: '#/definitions/DatabaseType'
          '401':
            description: Error if user is not authorized
            schema:
              type: string
              example: Unauthorized Access
        """
        return utils.basic_get(app.session, self.model_class, self.__class__.__name__)


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

        password_validation = utils.password_complexity_check(name, password)

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

    @auth.login_required
    def put(self, id):
        """Method to handle insert of new type.

        :param param: type description
        :return: type id that was inserted
        """
        verifier, row = utils.check_if_info_exists(self.model_class, id)
        if not verifier:
            return dict(
                error=f'{self.__class__.__name__} id not exists',
                id=id), 401

        data = json.loads(request.get_data().decode('utf-8'))

        if ['name', 'password'] not in data:
            return {'error': 'Invalid description provided'}, 401

        row.password = data['password']
        row.name = data['name']

        app.session.bulk_save_objects([row])
        app.session.commit()

        message = f"{self.__class__.__name__}:" + \
                  f" {row.id} saved successfully"
        app.logger.debug(f"[{request.authorization.username}] " + message)

        return dict(message=message, register=row.to_json())


class UserGroups(BasicTypes):
    """Class to handle user requests"""
    model_class = models.UserGroupModel

    @auth.login_required
    def get(self):
        """Method to handle get requests for type tables."""
        rows = app.session.query(self.model_class).all()
        app.logger.debug(
            f"[{request.authorization.username}] Returning all {self.__class__.__name__} rows")

        resp = {self.model_class.__tablename__: [row.to_json(app.session) for row in rows]}
        return resp

    @auth.login_required
    def post(self):
        """Method to handle post requests for type tables."""
        data = json.loads(request.get_data().decode('utf-8'))

        for item in ['group_id', 'user_id']:
            if item not in data:
                return {'error': 'Invalid body provided'}, 401

        if not utils.check_if_info_exists(models.GroupModel, data['group_id'])[0]:
            return {'error': 'Group not found'}, 401

        if not utils.check_if_info_exists(models.UserModel, data['user_id'])[0]:
            return {'error': 'User not found'}, 401

        row = app.session.query(self.model_class).\
            where(self.model_class.group_id == data['group_id'] and
                  self.model_class.user_id == data['user_id']).first()
        if row:
            return dict(
               error=f'{self.__class__.__name__}: Combination already exists'
            ), 401

        app.session.bulk_save_objects([self.model_class(data["group_id"], data['user_id'])])
        app.session.commit()

        row = app.session.query(self.model_class).\
            where(self.model_class.group_id == data['group_id'] and
                  self.model_class.user_id == data['user_id']).first()

        return {'success': 'Registered successfully', 'id': row.id}


class FunctionPermissions(Resource):
    """Method to handle function/permissions registration"""
    model_class = models.FunctionPermissionsModel

    @auth.login_required
    def get(self):
        """Method to handle get requests for type tables."""
        rows = app.session.query(self.model_class).all()
        app.logger.debug(
            f"[{request.authorization.username}] Returning all {self.__class__.__name__} rows")

        resp = {self.model_class.__tablename__: [row.to_json(app.session) for row in rows]}
        return resp

    @auth.login_required
    def post(self):
        """Method to handle post requests for type tables."""
        data = json.loads(request.get_data().decode('utf-8'))

        for item in ['group_id', 'function_id']:
            if item not in data:
                return {'error': 'Invalid body provided'}, 401

        if not utils.check_if_info_exists(models.GroupModel, data['group_id'])[0]:
            return {'error': 'Group not found'}, 401

        if not utils.check_if_info_exists(models.FunctionTypeModel, data['function_id'])[0]:
            return {'error': 'Function not found'}, 401

        row = app.session.query(self.model_class).\
            where(self.model_class.group_id == data['group_id'] and
                  self.model_class.function_id == data['function_id']).first()
        if row:
            return dict(
               error=f'{self.__class__.__name__}: Combination already exists'
            ), 401

        app.session.bulk_save_objects([self.model_class(data["group_id"], data['function_id'])])
        app.session.commit()

        row = app.session.query(self.model_class).\
            where(self.model_class.group_id == data['group_id'] and
                  self.model_class.function_id == data['function_id']).first()

        return {'success': 'Registered successfully', 'id': row.id}


class Databases(Resource):
    """Class to handle database requests"""
    model_class = models.DatabaseModel

    @auth.login_required
    def get(self):
        """Method to handle get requests"""
        return utils.basic_get(app.session, self.model_class, self.__class__.__name__)

    @auth.login_required
    def post(self):
        """Method to handle post requests for type tables."""
        data = json.loads(request.get_data().decode('utf-8'))

        class_fields = self.model_class.get_fields()
        for item in class_fields:
            if item not in data:
                return {
                    'error': 'Invalid body provided',
                    'required_fields': class_fields
                }, 401

        requirements = self.model_class.get_requirements()
        for requirement in requirements:
            requirement_result = utils.check_requirements(requirement[0], data[requirement[1]])
            if not requirement_result[0]:
                return {'error': requirement_result[1]}, 401

        fields = []
        for item in self.model_class.get_fields():
            fields.append(data[item])

        model = self.model_class(*fields)
        app.session.bulk_save_objects([model])
        app.session.commit()

        print(model.to_json())

        return {'success': 'Registered successfully'}
