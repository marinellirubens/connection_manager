"""Method to handle the resource for the API"""
from abc import ABC, abstractmethod
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

    @abstractmethod
    def get(self):
        """Method to handle get requests for type tables."""

    @abstractmethod
    def post(self):
        """Method to handle post requests for type tables."""

    @abstractmethod
    def options(self):
        """Method to handle options requests for type tables."""


class BasicTypeSingle(Resource, ABC):
    """Method to handle post requests for table when specific type requested."""
    model_class = None

    @abstractmethod
    def get(self, id):
        pass

    @abstractmethod
    def put(self, id):
        pass

    @abstractmethod
    def delete(self, id):
        pass

    @abstractmethod
    def options(self, id):
        pass


class DatabaseTypes(BasicTypes):
    """Method to handle post requests for database_type table when all lines requested."""
    model_class = models.DatabaseTypeModel
    methods = ['GET', 'POST', 'OPTIONS']

    @auth.login_required
    def get(self):
        """Method to get the database types.
        ---
        tags:
          - DatabaseType

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

    @auth.login_required
    def post(self):
        """Method to include a new database type.
        ---
        tags:
          - DatabaseType

        security:
          - basicAuth: []
        parameters:
          - in: body
            name: description
            description: Description of the database
            schema:
              $ref: '#/definitions/DatabaseTypeBody'

        definitions:
          DatabaseTypeBody:
            type: object
            properties:
              description:
                type: string
                description: Database type description
          BasicPost:
            type: object
            properties:
              status:
                type: string
                description: Message of the status
                example: Registered successfully
              id:
                type: integer
                description: Database type id
          Error:
            type: object
            properties:
              error:
                type: string
                description: Error message
                example: Invalid description provided
        responses:
          '200':
            description: A list of the database types
            schema:
              $ref: '#/definitions/BasicPost'
          '401':
            description: A list of the database types
            schema:
              $ref: '#/definitions/Error'
        """
        return utils.basic_post(app.session, request, self.model_class)

    def options(self):
        """Method to handle options requests for type tables.
        ---
        tags:
          - DatabaseType

        definitions:
          OptType:
            type: object
            properties:
              Allow:
                type: array
                description: Message of the status
                example: ['GET', 'POST', 'OPTIONS']
        responses:
          '200':
            description: A list of the database types
            schema:
              $ref: '#/definitions/OptType'
        """
        return dict(Allow=self.methods)


class DatabaseType(BasicTypeSingle):
    """Method to handle post requests for database_type table when specific database type requested.
    """
    model_class = models.DatabaseTypeModel
    methods = ['GET', 'PUT', 'OPTIONS', 'DELETE']

    @auth.login_required
    def get(self, id):
        """Method to get a database type by id.
        ---
        tags:
          - DatabaseType

        security:
          - basicAuth: []
        parameters:
          - in: path
            name: id
            description: Id of the Connection

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
            description: A list of the Connection types
            schema:
              $ref: '#/definitions/DatabaseType'
          '401':
            description: Error if user is not authorized
            schema:
              type: string
              example: Unauthorized Access
        """
        resp = utils.basic_single_get(
            id,
            app,
            self.model_class,
            request,
            self.__class__.__name__
        )
        return resp

    @auth.login_required
    def put(self, id):
        """Method to update database type description by id.
        ---
        tags:
          - DatabaseType

        security:
          - basicAuth: []

        parameters:
          - in: path
            name: id
            description: Id of the Connection

          - in: body
            name: description
            description: Description of the database
            schema:
              $ref: '#/definitions/DatabaseTypeBody'

        definitions:
          DatabaseTypeBody:
            type: object
            properties:
              description:
                type: string
                description: Database type description
                example: Oracle
          BasicPost:
            type: object
            properties:
              status:
                type: string
                description: Message of the status
                example: Registered successfully
              id:
                type: integer
                description: Database type id
          Error:
            type: object
            properties:
              error:
                type: string
                description: Error message
                example: Invalid description provided
        responses:
          '200':
            description: A list of the database types
            schema:
              $ref: '#/definitions/BasicPost'
          '401':
            description: A list of the database types
            schema:
              $ref: '#/definitions/Error'
        """
        resp = utils.basic_single_put(
            id,
            app,
            self.model_class,
            request,
            self.__class__.__name__
        )
        return resp

    @auth.login_required
    def delete(self, id):
        """Method to delete database type by id.
        ---
        tags:
          - DatabaseType

        security:
          - basicAuth: []

        parameters:
          - in: path
            name: id
            description: Id of the Connection

        definitions:
          BasicDelete:
            type: object
            properties:
              success:
                type: string
                description: Message of the status
                example: 1 deleted
          Error:
            type: object
            properties:
              error:
                type: string
                description: Error message
                example: DatabaseType if not exists
              id:
                type: int
                description: Id of the request
                example: 1
        responses:
          '200':
            description: A objects with a success message
            schema:
              $ref: '#/definitions/BasicDelete'
          '401':
            description: A object with the error message and the id requested
            schema:
              $ref: '#/definitions/Error'
        """
        resp = utils.basic_single_delete(
            id,
            app,
            self.model_class,
            self.__class__.__name__
        )
        return resp

    @auth.login_required
    def options(self, id):
        """Method to handle options requests for type tables.
        ---
        tags:
          - DatabaseType

        parameters:
          - in: query
            name: id
            description: Id of the Connection
        definitions:
          OptType:
            type: object
            properties:
              Allow:
                type: array
                description: Message of the status
                example: ['GET', 'POST', 'OPTIONS']
        responses:
          '200':
            description: A list of the database types
            schema:
              $ref: '#/definitions/OptType'
        """
        return dict(Allow=self.methods)


class ConnectionTypes(BasicTypes):
    """Method to handle post requests for connection_type table when all lines requested."""
    model_class = models.ConnectionTypeModel
    methods = ['GET', 'POST', 'OPTIONS']

    @auth.login_required
    def get(self):
        """Method to get the connection types.
        ---
        tags:
          - ConnectionType

        security:
          - basicAuth: []

        definitions:
          ConnectionType:
            type: object
            properties:
              id:
                type: integer
                description: Id of the Connection type
              description:
                type: string
                description: Connection type description
              creation_date:
                type: string
                description: Connection type creation date
        responses:
          '200':
            description: A list of the Connection types
            schema:
              $ref: '#/definitions/ConnectionType'
          '401':
            description: Error if user is not authorized
            schema:
              type: string
              example: Unauthorized Access
        """
        return utils.basic_get(app.session, self.model_class, self.__class__.__name__)

    @auth.login_required
    def post(self):
        """Method to include a new connection type.
        ---
        tags:
          - ConnectionType

        security:
          - basicAuth: []
        parameters:
          - in: body
            name: description
            description: Description of the database
            schema:
              $ref: '#/definitions/ConnectionTypeBody'

        definitions:
          ConnectionTypeBody:
            type: object
            properties:
              description:
                type: string
                description: Connection type description
          ConnectionType:
            type: object
            properties:
              description:
                type: string
                description: Connection type description
          BasicPost:
            type: object
            properties:
              status:
                type: string
                description: Message of the status
                example: Registered successfully
              id:
                type: integer
                description: Connection type id
          Error:
            type: object
            properties:
              error:
                type: string
                description: Error message
                example: Invalid description provided
        responses:
          '200':
            description: A list of the connection types
            schema:
              $ref: '#/definitions/BasicPost'
          '401':
            description: A list of the connection types
            schema:
              $ref: '#/definitions/Error'
        """
        return utils.basic_post(app.session, request, self.model_class)

    def options(self):
        """Method to handle options requests for type tables.
        ---
        tags:
          - ConnectionType

        definitions:
          OptType:
            type: object
            properties:
              Allow:
                type: array
                description: Message of the status
                example: ['GET', 'POST', 'OPTIONS']
        responses:
          '200':
            description: A list of the connection types
            schema:
              $ref: '#/definitions/OptType'
        """
        return dict(Allow=self.methods)


class ConnectionType(BasicTypeSingle):
    """Method to handle post requests for connection_type table when specific
    connection type requested.
    """
    model_class = models.ConnectionTypeModel
    methods = ['GET', 'PUT', 'OPTIONS', 'DELETE']

    @auth.login_required
    def get(self, id):
        """Method to get a connection type by id.
        ---
        tags:
          - ConnectionType

        security:
          - basicAuth: []
        parameters:
          - in: path
            name: id
            description: Id of the Connection

        definitions:
          ConnectionType:
            type: object
            properties:
              id:
                type: integer
                description: Id of the Connection type
              description:
                type: string
                description: Connection type description
              creation_date:
                type: string
                description: Connection type creation date
        responses:
          '200':
            description: A list of the Connection types
            schema:
              $ref: '#/definitions/ConnectionType'
          '401':
            description: Error if user is not authorized
            schema:
              type: string
              example: Unauthorized Access
        """
        resp = utils.basic_single_get(
            id,
            app,
            self.model_class,
            request,
            self.__class__.__name__
        )
        return resp

    @auth.login_required
    def put(self, id):
        """Method to update connection type description by id.
        ---
        tags:
          - ConnectionType

        security:
          - basicAuth: []

        parameters:
          - in: path
            name: id
            description: Id of the Connection

          - in: body
            name: description
            description: Description of the connection
            schema:
              $ref: '#/definitions/ConnectionTypeBody'

        definitions:
          ConnectionTypeBody:
            type: object
            properties:
              description:
                type: string
                description: Connection type description
                example: SSH
          BasicPost:
            type: object
            properties:
              status:
                type: string
                description: Message of the status
                example: Registered successfully
              id:
                type: integer
                description: Connection type id
          Error:
            type: object
            properties:
              error:
                type: string
                description: Error message
                example: Invalid description provided
        responses:
          '200':
            description: A list of the Connection types
            schema:
              $ref: '#/definitions/BasicPost'
          '401':
            description: A list of the Connection types
            schema:
              $ref: '#/definitions/Error'
        """
        resp = utils.basic_single_put(
            id,
            app,
            self.model_class,
            request,
            self.__class__.__name__
        )
        return resp

    @auth.login_required
    def delete(self, id):
        """Method to delete connection type by id.
        ---
        tags:
          - ConnectionType

        security:
          - basicAuth: []

        parameters:
          - in: path
            name: id
            description: Id of the Connection

        definitions:
          BasicDelete:
            type: object
            properties:
              success:
                type: string
                description: Message of the status
                example: 1 deleted
          Error:
            type: object
            properties:
              error:
                type: string
                description: Error message
                example: DatabaseType if not exists
              id:
                type: int
                description: Id of the request
                example: 1
        responses:
          '200':
            description: A objects with a success message
            schema:
              $ref: '#/definitions/BasicDelete'
          '401':
            description: A object with the error message and the id requested
            schema:
              $ref: '#/definitions/Error'
        """
        resp = utils.basic_single_delete(
            id,
            app,
            self.model_class,
            self.__class__.__name__
        )
        return resp

    @auth.login_required
    def options(self, id):
        """Method to handle options requests for type tables.
        ---
        tags:
          - DatabaseType

        parameters:
          - in: query
            name: id
            description: Id of the Connection
        definitions:
          OptType:
            type: object
            properties:
              Allow:
                type: array
                description: Message of the status
                example: ['GET', 'POST', 'OPTIONS']
        responses:
          '200':
            description: A list of the database types
            schema:
              $ref: '#/definitions/OptType'
        """
        return dict(Allow=self.methods)


class ServerTypes(BasicTypes):
    """Method to handle post requests for server_type table when all lines requested."""
    model_class = models.ServerTypeModel
    methods = ['GET', 'POST', 'OPTIONS']

    @auth.login_required
    def get(self):
        """Method to get the server types.
        ---
        tags:
          - ServerType

        security:
          - basicAuth: []

        definitions:
          ServerType:
            type: object
            properties:
              id:
                type: integer
                description: Id of the Server type
              description:
                type: string
                description: Server type description
              creation_date:
                type: string
                description: Server type creation date
          ServerTypes:
            type: object
            properties:
              server_type:
                type: array
                items:
                  $ref: '#/definitions/ServerType'
        responses:
          '200':
            description: A list of the Server types
            schema:
              $ref: '#/definitions/ServerTypes'
          '401':
            description: Error if user is not authorized
            schema:
              type: string
              example: Unauthorized Access
        """
        return utils.basic_get(app.session, self.model_class, self.__class__.__name__)

    @auth.login_required
    def post(self):
        """Method to include a new Server type.
        ---
        tags:
          - ServerType

        security:
          - basicAuth: []
        parameters:
          - in: body
            name: description
            description: Description of the database
            schema:
              $ref: '#/definitions/ServerTypeBody'

        definitions:
          ServerTypeBody:
            type: object
            properties:
              description:
                type: string
                description: Server type description
          BasicPost:
            type: object
            properties:
              status:
                type: string
                description: Message of the status
                example: Registered successfully
              id:
                type: integer
                description: Server type id
          Error:
            type: object
            properties:
              error:
                type: string
                description: Error message
                example: Invalid description provided
        responses:
          '200':
            description: A list of the Server types
            schema:
              $ref: '#/definitions/BasicPost'
          '401':
            description: A list of the Server types
            schema:
              $ref: '#/definitions/Error'
        """
        return utils.basic_post(app.session, request, self.model_class)

    def options(self):
        """Method to handle options requests for type tables.
        ---
        tags:
          - ServerType

        definitions:
          OptType:
            type: object
            properties:
              Allow:
                type: array
                description: Message of the status
                example: ['GET', 'POST', 'OPTIONS']
        responses:
          '200':
            description: A list of the Server types
            schema:
              $ref: '#/definitions/OptType'
        """
        return dict(Allow=self.methods)


class ServerType(BasicTypeSingle):
    """Method to handle post requests for server_type table when specific
    connection type requested.
    """
    model_class = models.ServerTypeModel
    methods = ['GET', 'PUT', 'OPTIONS', 'DELETE']

    @auth.login_required
    def get(self, id):
        """Method to get a Server type by id.
        ---
        tags:
          - ServerType

        security:
          - basicAuth: []
        parameters:
          - in: path
            name: id
            description: Id of the Server

        definitions:
          ServerType:
            type: object
            properties:
              id:
                type: integer
                description: Id of the Server type
              description:
                type: string
                description: Server type description
              creation_date:
                type: string
                description: Server type creation date
        responses:
          '200':
            description: A list of the Server types
            schema:
              $ref: '#/definitions/ServerType'
          '401':
            description: Error if user is not authorized
            schema:
              type: string
              example: Unauthorized Access
        """
        resp = utils.basic_single_get(
            id,
            app,
            self.model_class,
            request,
            self.__class__.__name__
        )
        return resp

    @auth.login_required
    def put(self, id):
        """Method to update Server type description by id.
        ---
        tags:
          - ServerType

        security:
          - basicAuth: []

        parameters:
          - in: path
            name: id
            description: Id of the Server

          - in: body
            name: description
            description: Description of the Server
            schema:
              $ref: '#/definitions/ServerTypeBody'

        definitions:
          ServerTypeBody:
            type: object
            properties:
              description:
                type: string
                description: Server type description
                example: SSH
          BasicPost:
            type: object
            properties:
              status:
                type: string
                description: Message of the status
                example: Registered successfully
              id:
                type: integer
                description: Server type id
          Error:
            type: object
            properties:
              error:
                type: string
                description: Error message
                example: Invalid description provided
        responses:
          '200':
            description: A list of the Server types
            schema:
              $ref: '#/definitions/BasicPost'
          '401':
            description: A list of the Server types
            schema:
              $ref: '#/definitions/Error'
        """
        resp = utils.basic_single_put(
            id,
            app,
            self.model_class,
            request,
            self.__class__.__name__
        )
        return resp

    @auth.login_required
    def delete(self, id):
        """Method to delete Server type by id.
        ---
        tags:
          - ServerType

        security:
          - basicAuth: []

        parameters:
          - in: path
            name: id
            description: Id of the Server

        definitions:
          BasicDelete:
            type: object
            properties:
              success:
                type: string
                description: Message of the status
                example: 1 deleted
          Error:
            type: object
            properties:
              error:
                type: string
                description: Error message
                example: DatabaseType if not exists
              id:
                type: int
                description: Id of the request
                example: 1
        responses:
          '200':
            description: A objects with a success message
            schema:
              $ref: '#/definitions/BasicDelete'
          '401':
            description: A object with the error message and the id requested
            schema:
              $ref: '#/definitions/Error'
        """
        resp = utils.basic_single_delete(
            id,
            app,
            self.model_class,
            self.__class__.__name__
        )
        return resp

    @auth.login_required
    def options(self, id):
        """Method to handle options requests for type tables.
        ---
        tags:
          - ServerType

        parameters:
          - in: query
            name: id
            description: Id of the Server
        definitions:
          OptType:
            type: object
            properties:
              Allow:
                type: array
                description: Message of the status
                example: ['GET', 'POST', 'OPTIONS']
        responses:
          '200':
            description: A list of the server types
            schema:
              $ref: '#/definitions/OptType'
        """
        return dict(Allow=self.methods)


class FunctionTypes(BasicTypes):
    """Method to handle post requests for function_type table when all lines requested."""
    model_class = models.FunctionTypeModel
    methods = ['GET', 'POST', 'OPTIONS']

    @auth.login_required
    def get(self):
        """Method to get the Function types.
        ---
        tags:
          - FunctionType

        security:
          - basicAuth: []

        definitions:
          FunctionType:
            type: object
            properties:
              id:
                type: integer
                description: Id of the Function type
              description:
                type: string
                description: Function type description
              creation_date:
                type: string
                description: Function type creation date
          FunctionTypes:
            type: object
            properties:
              function_type:
                type: array
                items:
                  $ref: '#/definitions/FunctionType'
        responses:
          '200':
            description: A list of the Function types
            schema:
              $ref: '#/definitions/FunctionTypes'
          '401':
            description: Error if user is not authorized
            schema:
              type: string
              example: Unauthorized Access
        """
        return utils.basic_get(app.session, self.model_class, self.__class__.__name__)

    @auth.login_required
    def post(self):
        """Method to include a new Function type.
        ---
        tags:
          - FunctionType

        security:
          - basicAuth: []
        parameters:
          - in: body
            name: description
            description: Description of the database
            schema:
              $ref: '#/definitions/FunctionTypeBody'

        definitions:
          FunctionTypeBody:
            type: object
            properties:
              description:
                type: string
                description: Function type description
          BasicPost:
            type: object
            properties:
              status:
                type: string
                description: Message of the status
                example: Registered successfully
              id:
                type: integer
                description: Function type id
          Error:
            type: object
            properties:
              error:
                type: string
                description: Error message
                example: Invalid description provided
        responses:
          '200':
            description: A list of the Function types
            schema:
              $ref: '#/definitions/BasicPost'
          '401':
            description: A list of the Function types
            schema:
              $ref: '#/definitions/Error'
        """
        return utils.basic_post(app.session, request, self.model_class)

    def options(self):
        """Method to handle options requests for type tables.
        ---
        tags:
          - FunctionType

        definitions:
          OptType:
            type: object
            properties:
              Allow:
                type: array
                description: Message of the status
                example: ['GET', 'POST', 'OPTIONS']
        responses:
          '200':
            description: A list of the Function types
            schema:
              $ref: '#/definitions/OptType'
        """
        return dict(Allow=self.methods)


class FunctionType(BasicTypeSingle):
    """Method to handle post requests for function_type table when specific
    function type requested.
    """
    model_class = models.FunctionTypeModel
    methods = ['GET', 'PUT', 'OPTIONS', 'DELETE']

    @auth.login_required
    def get(self, id):
        """Method to get a Function type by id.
        ---
        tags:
          - FunctionType

        security:
          - basicAuth: []
        parameters:
          - in: path
            name: id
            description: Id of the Function

        definitions:
          FunctionType:
            type: object
            properties:
              id:
                type: integer
                description: Id of the function type
              description:
                type: string
                description: Function type description
              creation_date:
                type: string
                description: Function type creation date
        responses:
          '200':
            description: A list of the Function types
            schema:
              $ref: '#/definitions/FunctionType'
          '401':
            description: Error if user is not authorized
            schema:
              type: string
              example: Unauthorized Access
        """
        resp = utils.basic_single_get(
            id,
            app,
            self.model_class,
            request,
            self.__class__.__name__
        )
        return resp

    @auth.login_required
    def put(self, id):
        """Method to update Function type description by id.
        ---
        tags:
          - FunctionType

        security:
          - basicAuth: []

        parameters:
          - in: path
            name: id
            description: Id of the Function

          - in: body
            name: description
            description: Description of the Function
            schema:
              $ref: '#/definitions/FunctionTypeBody'

        definitions:
          FunctionTypeBody:
            type: object
            properties:
              description:
                type: string
                description: Function type description
                example: SSH
          BasicPost:
            type: object
            properties:
              status:
                type: string
                description: Message of the status
                example: Registered successfully
              id:
                type: integer
                description: Function type id
          Error:
            type: object
            properties:
              error:
                type: string
                description: Error message
                example: Invalid description provided
        responses:
          '200':
            description: A list of the Function types
            schema:
              $ref: '#/definitions/BasicPost'
          '401':
            description: A list of the Function types
            schema:
              $ref: '#/definitions/Error'
        """
        resp = utils.basic_single_put(
            id,
            app,
            self.model_class,
            request,
            self.__class__.__name__
        )
        return resp

    @auth.login_required
    def delete(self, id):
        """Method to delete Function type by id.
        ---
        tags:
          - FunctionType

        security:
          - basicAuth: []

        parameters:
          - in: path
            name: id
            description: Id of the Function

        definitions:
          BasicDelete:
            type: object
            properties:
              success:
                type: string
                description: Message of the status
                example: 1 deleted
          Error:
            type: object
            properties:
              error:
                type: string
                description: Error message
                example: FunctionType if not exists
              id:
                type: int
                description: Id of the request
                example: 1
        responses:
          '200':
            description: A objects with a success message
            schema:
              $ref: '#/definitions/BasicDelete'
          '401':
            description: A object with the error message and the id requested
            schema:
              $ref: '#/definitions/Error'
        """
        resp = utils.basic_single_delete(
            id,
            app,
            self.model_class,
            self.__class__.__name__
        )
        return resp

    @auth.login_required
    def options(self, id):
        """Method to handle options requests for type tables.
        ---
        tags:
          - FunctionType

        parameters:
          - in: query
            name: id
            description: Id of the Function
        definitions:
          OptType:
            type: object
            properties:
              Allow:
                type: array
                description: Message of the status
                example: ['GET', 'POST', 'OPTIONS']
        responses:
          '200':
            description: A list of the function types
            schema:
              $ref: '#/definitions/OptType'
        """
        return dict(Allow=self.methods)


class Groups(BasicTypes):
    """Method to handle post requests for groups table when all lines requested."""
    model_class = models.GroupModel
    methods = ['GET', 'POST', 'OPTIONS']

    @auth.login_required
    def get(self):
        """Method to get the Group types.
        ---
        tags:
          - Groups

        security:
          - basicAuth: []

        definitions:
          GroupType:
            type: object
            properties:
              id:
                type: integer
                description: Id of the Group type
              description:
                type: string
                description: Group type description
              creation_date:
                type: string
                description: Group type creation date
          GroupTypes:
            type: object
            properties:
              group_type:
                type: array
                items:
                  $ref: '#/definitions/GroupType'
        responses:
          '200':
            description: A list of the Group types
            schema:
              $ref: '#/definitions/GroupTypes'
          '401':
            description: Error if user is not authorized
            schema:
              type: string
              example: Unauthorized Access
        """
        return utils.basic_get(app.session, self.model_class, self.__class__.__name__)

    @auth.login_required
    def post(self):
        """Method to include a new Group type.
        ---
        tags:
          - Groups

        security:
          - basicAuth: []

        parameters:
          - in: body
            name: description
            description: Description of the database
            schema:
              $ref: '#/definitions/GroupTypeBody'

        definitions:
          GroupTypeBody:
            type: object
            properties:
              description:
                type: string
                description: Group type description
          BasicPost:
            type: object
            properties:
              status:
                type: string
                description: Message of the status
                example: Registered successfully
              id:
                type: integer
                description: Group type id
          Error:
            type: object
            properties:
              error:
                type: string
                description: Error message
                example: Invalid description provided
        responses:
          '200':
            description: A list of the Group types
            schema:
              $ref: '#/definitions/BasicPost'
          '401':
            description: A list of the Group types
            schema:
              $ref: '#/definitions/Error'
        """
        return utils.basic_post(app.session, request, self.model_class)

    def options(self):
        """Method to handle options requests for type tables.
        ---
        tags:
          - Groups

        definitions:
          OptType:
            type: object
            properties:
              Allow:
                type: array
                description: Message of the status
                example: ['GET', 'POST', 'OPTIONS']
        responses:
          '200':
            description: A list of the Group types
            schema:
              $ref: '#/definitions/OptType'
        """
        return dict(Allow=self.methods)


class Group(BasicTypeSingle):
    """Method to handle post requests for groups table when specific group requested."""
    model_class = models.GroupModel
    methods = ['GET', 'PUT', 'OPTIONS', 'DELETE']

    @auth.login_required
    def get(self, id):
        """Method to get a Group type by id.
        ---
        tags:
          - Groups

        security:
          - basicAuth: []
        parameters:
          - in: path
            name: id
            description: Id of the Group

        definitions:
          GroupType:
            type: object
            properties:
              id:
                type: integer
                description: Id of the Group type
              description:
                type: string
                description: Group type description
              creation_date:
                type: string
                description: Group type creation date
        responses:
          '200':
            description: A list of the Group types
            schema:
              $ref: '#/definitions/GroupType'
          '401':
            description: Error if user is not authorized
            schema:
              type: string
              example: Unauthorized Access
        """
        resp = utils.basic_single_get(
            id,
            app,
            self.model_class,
            request,
            self.__class__.__name__
        )
        return resp

    @auth.login_required
    def put(self, id):
        """Method to update Group type description by id.
        ---
        tags:
          - Groups

        security:
          - basicAuth: []

        parameters:
          - in: path
            name: id
            description: Id of the Group

          - in: body
            name: description
            description: Description of the Group
            schema:
              $ref: '#/definitions/GroupTypeBody'

        definitions:
          GroupTypeBody:
            type: object
            properties:
              description:
                type: string
                description: Group type description
                example: SSH
          BasicPost:
            type: object
            properties:
              status:
                type: string
                description: Message of the status
                example: Registered successfully
              id:
                type: integer
                description: Group type id
          Error:
            type: object
            properties:
              error:
                type: string
                description: Error message
                example: Invalid description provided
        responses:
          '200':
            description: A list of the Group types
            schema:
              $ref: '#/definitions/BasicPost'
          '401':
            description: A list of the Group types
            schema:
              $ref: '#/definitions/Error'
        """
        resp = utils.basic_single_put(
            id,
            app,
            self.model_class,
            request,
            self.__class__.__name__
        )
        return resp

    @auth.login_required
    def delete(self, id):
        """Method to delete Group type by id.
        ---
        tags:
          - Groups

        security:
          - basicAuth: []

        parameters:
          - in: path
            name: id
            description: Id of the Group

        definitions:
          BasicDelete:
            type: object
            properties:
              success:
                type: string
                description: Message of the status
                example: 1 deleted
          Error:
            type: object
            properties:
              error:
                type: string
                description: Error message
                example: GroupType if not exists
              id:
                type: int
                description: Id of the request
                example: 1
        responses:
          '200':
            description: A objects with a success message
            schema:
              $ref: '#/definitions/BasicDelete'
          '401':
            description: A object with the error message and the id requested
            schema:
              $ref: '#/definitions/Error'
        """
        resp = utils.basic_single_delete(
            id,
            app,
            self.model_class,
            self.__class__.__name__
        )
        return resp

    @auth.login_required
    def options(self, id):
        """Method to handle options requests for type tables.
        ---
        tags:
          - Groups

        parameters:
          - in: query
            name: id
            description: Id of the Group
        definitions:
          OptType:
            type: object
            properties:
              Allow:
                type: array
                description: Message of the status
                example: ['GET', 'POST', 'OPTIONS']
        responses:
          '200':
            description: A list of the Group types
            schema:
              $ref: '#/definitions/OptType'
        """
        return dict(Allow=self.methods)


class Users(BasicTypes):
    """Class to handle user requests"""
    model_class = models.UserModel
    methods = ['GET', 'POST', 'OPTIONS']

    @auth.login_required
    def get(self):
        """Method to get the Users list.
        ---
        tags:
          - Users

        security:
          - basicAuth: []

        definitions:
          UserType:
            type: object
            properties:
              id:
                type: integer
                description: Id of the User type
              name:
                type: string
                description: User name
              creation_date:
                type: string
                description: User creation date
              update_date:
                type: string
                description: User update date
          UserTypes:
            type: object
            properties:
              user_type:
                type: array
                items:
                  $ref: '#/definitions/UserType'
        responses:
          '200':
            description: A list of the User types
            schema:
              $ref: '#/definitions/UserTypes'
          '401':
            description: Error if user is not authorized
            schema:
              type: string
              example: Unauthorized Access
        """
        return utils.basic_get(app.session, self.model_class, self.__class__.__name__)

    @auth.login_required
    def post(self):
        """Method to handle the user insert
        ---
        tags:
          - Users

        security:
          - basicAuth: []

        parameters:
          - in: body
            name: user
            description: User information
            schema:
              $ref: '#/definitions/UserBody'

        definitions:
          UserBody:
            type: object
            properties:
              name:
                type: string
                description: User name
              password:
                type: string
                description: User password
          BasicPost:
            type: object
            properties:
              status:
                type: string
                description: Message of the status
                example: Registered successfully
              id:
                type: integer
                description: User id
          Error:
            type: object
            properties:
              error:
                type: string
                description: Error message
                example: Invalid description provided
        responses:
          '200':
            description: A list of Users
            schema:
              $ref: '#/definitions/BasicPost'
          '401':
            description: Error on the request
            schema:
              $ref: '#/definitions/Error'
          '400':
            description: error on the request parameters
            schema:
              $ref: '#/definitions/Error'
        """
        data = json.loads(request.get_data().decode('utf-8'))

        name = data.get('name', None)
        password = data.get('password', None)

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

    def options(self):
        return dict(Allow=self.methods)


class User(BasicTypeSingle):
    """Class to handle user single request"""
    model_class = models.UserModel
    methods = ['GET', 'PUT', 'OPTIONS', 'DELETE']

    @auth.login_required
    def get(self, id):
        """Method to get a User type by id.
        ---
        tags:
          - Users

        security:
          - basicAuth: []

        parameters:
          - in: path
            name: id
            description: Id of the User

        definitions:
          UserType:
            type: object
            properties:
              id:
                type: integer
                description: Id of the User type
              name:
                type: string
                description: User name
              creation_date:
                type: string
                description: User creation date
              update_date:
                type: string

        responses:
          '200':
            description: returns a user
            schema:
              $ref: '#/definitions/UserType'
          '401':
            description: Error if user is not authorized
            schema:
              type: string
              example: Unauthorized Access
        """
        resp = utils.basic_single_get(
            id,
            app,
            self.model_class,
            request,
            self.__class__.__name__
        )
        return resp

    @auth.login_required
    def put(self, id):
        """Method to handle insert of new type.

        :param param: type description
        :return: type id that was inserted
        ---
        tags:
          - Users

        security:
          - basicAuth: []

        parameters:
          - in: path
            name: id
            description: Id of the User

          - in: body
            name: description
            description: Description of the Group
            schema:
              $ref: '#/definitions/UserBody'

        definitions:
          UserBody:
            type: object
            properties:
              name:
                type: string
                description: User name
              password:
                type: string
                description: User password
          Error:
            type: object
            properties:
              error:
                type: string
                description: Error message
                example: Invalid description provided
        responses:
          '200':
            description: Status of the update
            schema:
              $ref: '#/definitions/BasicPost'
          '401':
            description: Error message
            schema:
              $ref: '#/definitions/Error'
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

    @auth.login_required
    def delete(self, id):
        """Method to delete User by id.
        ---
        tags:
          - Users

        security:
          - basicAuth: []

        parameters:
          - in: path
            name: id
            description: Id of the User

        definitions:
          BasicDelete:
            type: object
            properties:
              success:
                type: string
                description: Message of the status
                example: 1 deleted
          Error:
            type: object
            properties:
              error:
                type: string
                description: Error message
                example: User does not exists
              id:
                type: int
                description: Id of the request
                example: 1
        responses:
          '200':
            description: A objects with a success message
            schema:
              $ref: '#/definitions/BasicDelete'
          '401':
            description: A object with the error message and the id requested
            schema:
              $ref: '#/definitions/Error'
        """
        resp = utils.basic_single_delete(
            id,
            app,
            self.model_class,
            self.__class__.__name__
        )
        return resp

    def options(self):
        return dict(Allow=self.methods)


class UserGroup(Resource):
    """Class to handle user group individual requests."""
    model_class = models.UserGroupModel
    methods = ['GET', 'PUT', 'OPTIONS', 'DELETE']

    @auth.login_required
    def get(self, id):
        """Method to get single conbination of user / group.
        ---
        tags:
          - UserGroups

        security:
          - basicAuth: []

        parameters:
          - in: path
            name: id
            description: Id of the User / Group combination

        definitions:
          UserGroupType:
            type: object
            properties:
              id:
                type: integer
                description: Id of the User type
              group_id:
                type: integer
                description: Group id
              user_id:
                type: integer
                description: User id

        responses:
          '200':
            description: returns a user / group combination
            schema:
              $ref: '#/definitions/UserGroupType'
          '401':
            description: Error if user is not authorized
            schema:
              type: string
              example: Unauthorized Access
        """
        resp = utils.basic_single_get(
            id,
            app,
            self.model_class,
            request,
            self.__class__.__name__
        )
        return resp

    @auth.login_required
    def put(self, id):
        """Method to change single combination of user / group.
        ---
        tags:
          - UserGroups

        security:
          - basicAuth: []

        parameters:
          - in: body
            name: user_group
            description: User group link
            schema:
              $ref: '#/definitions/UserGroupBody'

        definitions:
          UserGroupBody:
            type: object
            properties:
              group_id:
                type: integer
                description: Group id
              user_id:
                type: integer
                description: User id
          Error:
            type: object
            properties:
              error:
                type: string
                description: Error message
                example: Invalid description provided
        responses:
          '200':
            description: Status of the update
            schema:
              $ref: '#/definitions/BasicPost'
          '401':
            description: Error message
            schema:
              $ref: '#/definitions/Error'
        """
        verifier, row = utils.check_if_info_exists(self.model_class, id)
        if not verifier:
            return dict(
                error=f'{self.__class__.__name__} id not exists',
                id=id), 401

        data = json.loads(request.get_data().decode('utf-8'))

        if ['group_id', 'user_id'] not in data:
            return {'error': 'Invalid description provided'}, 401

        row.user_id = data['user_id']
        row.group_id = data['group_id']

        app.session.bulk_save_objects([row])
        app.session.commit()

        message = f"{self.__class__.__name__}:" + \
                  f" {row.id} saved successfully"
        app.logger.debug(f"[{request.authorization.username}] " + message)

        return dict(message=message, register=row.to_json())

    @auth.login_required
    def delete(self, id):
        """Method to change single combination of user / group.
        ---
        tags:
          - UserGroups

        security:
          - basicAuth: []

        parameters:
          - in: path
            name: id
            description: Id of the User Group combination.

        definitions:
          BasicDelete:
            type: object
            properties:
              success:
                type: string
                description: Message of the status
                example: 1 deleted
          Error:
            type: object
            properties:
              error:
                type: string
                description: Error message
                example: User does not exists
              id:
                type: int
                description: Id of the request
                example: 1
        responses:
          '200':
            description: A objects with a success message
            schema:
              $ref: '#/definitions/BasicDelete'
          '401':
            description: A object with the error message and the id requested
            schema:
              $ref: '#/definitions/Error'
        """
        resp = utils.basic_single_delete(
            id,
            app,
            self.model_class,
            self.__class__.__name__
        )
        return resp

    def options(self, id):
        """Method to get the methods allowd for this enpoint."""
        return dict(Allow=self.methods)


class UserGroups(BasicTypes):
    """Class to handle user requests"""
    model_class = models.UserGroupModel
    methods = ['GET', 'POST', 'OPTIONS']

    @auth.login_required
    def get(self):
        """Method to handle get requests for type tables.
        ---
        tags:
          - UserGroups

        security:
          - basicAuth: []

        definitions:
          UserType:
            type: object
            properties:
              id:
                type: integer
                description: Id of the User type
                example: 1
              name:
                type: string
                description: User name
                example: admin
              creation_date:
                type: string
                description: User creation date
                example: 2022-08-28
              update_date:
                type: string
                description: User update date
                example: 2022-08-28
          GroupType:
            type: object
            properties:
              id:
                type: integer
                description: Id of the Group type
                example: 1
              description:
                type: string
                description: Group type description
                example: admin
              creation_date:
                type: string
                description: Group type creation date
                example: 2022-08-28
          UserGroup:
            type: object
            properties:
              id:
                type: integer
                description: Id of the database type
                example: 1
              group:
                type: object
                description: Group object mapped to user
                schema:
                  $ref: '#/definitions/GroupType'
              user:
                type: object
                description: User maped to group
                schema:
                  $ref: '#/definitions/UserType'
          UserGroups:
            type: object
            properties:
              user_grp:
                type: array
                items:
                  $ref: '#/definitions/UserGroup'
        responses:
          '200':
            description: A list of the user by group
            schema:
              $ref: '#/definitions/UserGroups'
          '401':
            description: Error if user is not authorized
            schema:
              type: string
              example: Unauthorized Access
        """
        return utils.basic_get(app.session, self.model_class, self.__class__.__name__)

    @auth.login_required
    def post(self):
        """Method to handle post requests for type tables.
        ---
        tags:
          - UserGroups

        security:
          - basicAuth: []

        parameters:
          - in: body
            name: user_group
            description: User group link
            schema:
              $ref: '#/definitions/UserGroupBody'

        definitions:
          UserGroupBody:
            type: object
            properties:
              group_id:
                type: integer
                description: Group id
              user_id:
                type: integer
                description: User id
          BasicPost:
            type: object
            properties:
              status:
                type: string
                description: Message of the status
                example: Registered successfully
              id:
                type: integer
                description: User id
          Error:
            type: object
            properties:
              error:
                type: string
                description: Error message
                example: Invalid description provided
        responses:
          '200':
            description: A list of Users
            schema:
              $ref: '#/definitions/BasicPost'
          '401':
            description: Error on the request
            schema:
              $ref: '#/definitions/Error'
          '400':
            description: error on the request parameters
            schema:
              $ref: '#/definitions/Error'
        """
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

    def options(self):
        return dict(Allow=self.methods)


class FunctionPermission(Resource):
    """Class to handle function/permissions registration."""
    model_class = models.FunctionPermissionsModel
    methods = ['GET', 'PUT', 'OPTIONS', 'DELETE']

    @auth.login_required
    def get(self, id):
        """Method to get single conbination of Function / Permission.
        ---
        tags:
          - FunctionPermissions

        security:
          - basicAuth: []

        parameters:
          - in: path
            name: id
            description: Id of the User / Group combination

        definitions:
          FunctionPermissionType:
            type: object
            properties:
              id:
                type: integer
                description: Id of the User type
              group_id:
                type: integer
                description: Group id
              function_id:
                type: integer
                description: Function id

        responses:
          '200':
            description: returns a user / group combination
            schema:
              $ref: '#/definitions/FunctionPermissionType'
          '401':
            description: Error if user is not authorized
            schema:
              type: string
              example: Unauthorized Access
        """
        resp = utils.basic_single_get(
            id,
            app,
            self.model_class,
            request,
            self.__class__.__name__
        )
        return resp

    @auth.login_required
    def put(self, id):
        """Method to change single combination of user / group.
        ---
        tags:
          - FunctionPermissions

        security:
          - basicAuth: []

        parameters:
          - in: body
            name: user_group
            description: Function/Permission combination.
            schema:
              $ref: '#/definitions/FunctionPermissionBody'

        definitions:
          FunctionPermissionBody:
            type: object
            properties:
              group_id:
                type: integer
                description: Group id
              function_id:
                type: integer
                description: Function id
          Error:
            type: object
            properties:
              error:
                type: string
                description: Error message
                example: Invalid description provided
        responses:
          '200':
            description: Status of the update
            schema:
              $ref: '#/definitions/BasicPost'
          '401':
            description: Error message
            schema:
              $ref: '#/definitions/Error'
        """
        verifier, row = utils.check_if_info_exists(self.model_class, id)
        if not verifier:
            return dict(
                error=f'{self.__class__.__name__} id not exists',
                id=id), 401

        data = json.loads(request.get_data().decode('utf-8'))

        if ['group_id', 'function_id'] not in data:
            return {'error': 'Invalid description provided'}, 401

        row.user_id = data['user_id']
        row.function_id = data['function_id']

        app.session.bulk_save_objects([row])
        app.session.commit()

        message = f"{self.__class__.__name__}:" + \
                  f" {row.id} saved successfully"
        app.logger.debug(f"[{request.authorization.username}] " + message)

        return dict(message=message, register=row.to_json())

    @auth.login_required
    def delete(self, id):
        """Method to handle the delete of a function/permission combination
        ---
        tags:
          - FunctionPermissions

        security:
          - basicAuth: []

        parameters:
          - in: path
            name: id
            description: Id of the function/permission combination.

        definitions:
          BasicDelete:
            type: object
            properties:
              success:
                type: string
                description: Message of the status
                example: 1 deleted
          Error:
            type: object
            properties:
              error:
                type: string
                description: Error message
                example: User does not exists
              id:
                type: int
                description: Id of the request
                example: 1
        responses:
          '200':
            description: A objects with a success message
            schema:
              $ref: '#/definitions/BasicDelete'
          '401':
            description: A object with the error message and the id requested
            schema:
              $ref: '#/definitions/Error'
        """
        resp = utils.basic_single_delete(
            id,
            app,
            self.model_class,
            self.__class__.__name__
        )
        return resp

    def options(self, id):
        """Method to get the methods allowd for this enpoint."""
        return dict(Allow=self.methods)


class FunctionPermissions(Resource):
    """Method to handle function/permissions registration"""
    model_class = models.FunctionPermissionsModel
    methods = ['GET', 'POST', 'OPTIONS']

    @auth.login_required
    def get(self):
        """(Incomplete) Method to handle get requests for type tables.
          ---
          tags:
            - FunctionPermissions

          security:
            - basicAuth: []

          definitions:
            FunctionTypeBody:
              type: object
              properties:
                description:
                  type: string
                  description: Function type description
            GroupType:
              type: object
              properties:
                id:
                  type: integer
                  description: Id of the Group type
                description:
                  type: string
                  description: Group type description
                creation_date:
                  type: string
                  description: Group type creation date
            FunctionPermission:
              type: object
              properties:
                id:
                  type: integer
                  description: Function / Group permission
                group:
                  type: object
                  description: Group object
                  schema:
                    $ref: '#/definitions/GroupType'
                function:
                  type: object
                  description: Function information
                  schema:
                    $ref: '#/definitions/FunctionTypeBody'
            FunctionPermissions:
              type: object
              properties:
                function_permission:
                  type: array
                  items:
                    $ref: '#/definitions/FunctionPermission'

          responses:
            '200':
              description: A list of Function permissions
              schema:
                $ref: '#/definitions/FunctionPermissions'
            '401':
              description: Error if user is not authorized
              schema:
                type: string
                example: Unauthorized Access
        """
        return utils.basic_get(app.session, self.model_class, self.__class__.__name__)

    @auth.login_required
    def post(self):
        """(Incomplete) Method to handle post requests for type tables.
        ---
        tags:
          - FunctionPermissions

        security:
          - basicAuth: []

        parameters:
          - in: body
            name: function_permission
            description: link of the function and group
            schema:
              $ref: '#/definitions/FunctionPermissionBody'

        definitions:
          FunctionPermissionBody:
            type: object
            properties:
              group_id:
                type: integer
                description: The id of the Group
              function_id:
                type: integer
                description: The id of the function
          BasicPost:
            type: object
            properties:
              status:
                type: string
                description: Message of the status
                example: Registered successfully
              id:
                type: integer
                description: Group type id
          Error:
            type: object
            properties:
              error:
                type: string
                description: Error message
                example: Invalid description provided

        responses:
          '200':
            description: Object with the status of the request, and id of the new functionpermission
            schema:
              $ref: '#/definitions/BasicPost'
          '401':
            description: Object with the status of the request
            schema:
              $ref: '#/definitions/Error'
        """
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

    def options(self):
        return dict(Allow=self.methods)


class Database(Resource):
    """Class to handle database requests."""
    model_class = models.DatabaseModel
    methods = ['GET', 'PUT', 'OPTIONS', 'DELETE']

    @auth.login_required
    def get(self, id):
        """Method to get single Database.
        ---
        tags:
          - Databases

        security:
          - basicAuth: []

        parameters:
          - in: path
            name: id
            description: Id of the Database

        definitions:
          Database:
            type: object
            properties:
              id:
                type: integer
                description: Id of the User type
              description:
                type: string
                description: database description
              host:
                type: string
                description: hostnane or ip
              port:
                type: integer
                description: database port
              sid:
                type: string
                description: datanbase sid name
              database_type_id:
                type: integer
                description: id of the database id.

        responses:
          '200':
            description: returns a user / group combination
            schema:
              $ref: '#/definitions/Database'
          '401':
            description: Error if user is not authorized
            schema:
              type: string
              example: Unauthorized Access
        """
        resp = utils.basic_single_get(
            id,
            app,
            self.model_class,
            request,
            self.__class__.__name__
        )
        return resp

    @auth.login_required
    def put(self, id):
        """Method to change single Database.
        ---
        tags:
          - Databases

        security:
          - basicAuth: []

        parameters:
          - in: body
            name: user_group
            description: Function/Permission combination.
            schema:
              $ref: '#/definitions/DatabaseBody'

        definitions:
          DatabaseBody:
            type: object
            properties:
              description:
                type: string
                description: database description
              host:
                type: string
                description: hostnane or ip
              port:
                type: integer
                description: database port
              sid:
                type: string
                description: datanbase sid name
              database_type_id:
                type: integer
                description: id of the database id.
          Error:
            type: object
            properties:
              error:
                type: string
                description: Error message
                example: Invalid description provided
        responses:
          '200':
            description: Status of the update
            schema:
              $ref: '#/definitions/BasicPost'
          '401':
            description: Error message
            schema:
              $ref: '#/definitions/Error'
        """
        verifier, row = utils.check_if_info_exists(self.model_class, id)
        if not verifier:
            return dict(
                error=f'{self.__class__.__name__} id not exists',
                id=id), 401

        data = json.loads(request.get_data().decode('utf-8'))

        for item in row.get_fields():
            if item not in data:
                return {
                    'error': 'Invalid body provided',
                    'required_fields': row.get_fields()
                }, 401

        row.description = data['description']
        row.host = data['host']
        row.port = data['port']
        row.sid = data['sid']
        row.database_type_id = data['database_type_id']

        app.session.bulk_save_objects([row])
        app.session.commit()

        message = f"{self.__class__.__name__}:" + \
                  f" {row.id} saved successfully"
        app.logger.debug(f"[{request.authorization.username}] " + message)

        return dict(message=message, register=row.to_json())

    @auth.login_required
    def delete(self, id):
        """Method to handle the delete of a Databases
        ---
        tags:
          - Databases

        security:
          - basicAuth: []

        parameters:
          - in: path
            name: id
            description: Id of the Databases.

        definitions:
          BasicDelete:
            type: object
            properties:
              success:
                type: string
                description: Message of the status
                example: 1 deleted
          Error:
            type: object
            properties:
              error:
                type: string
                description: Error message
                example: User does not exists
              id:
                type: int
                description: Id of the request
                example: 1
        responses:
          '200':
            description: A objects with a success message
            schema:
              $ref: '#/definitions/BasicDelete'
          '401':
            description: A object with the error message and the id requested
            schema:
              $ref: '#/definitions/Error'
        """
        resp = utils.basic_single_delete(
            id,
            app,
            self.model_class,
            self.__class__.__name__
        )
        return resp

    def options(self, id):
        """Method to get the methods allowd for this enpoint."""
        return dict(Allow=self.methods)


class Databases(Resource):
    """Class to handle database requests"""
    model_class = models.DatabaseModel
    methods = ['GET', 'POST', 'OPTIONS']

    @auth.login_required
    def get(self):
        """Method to handle get requests
        ---
        tags:
          - Databases

        security:
          - basicAuth: []

        definitions:
          Database:
            type: object
            properties:
              description:
                type: string
                description: Database description
              host:
                type: string
                description: Hostname or ip address for the database
              port:
                type: string
                description: port used by the database
              sid:
                type: string
                description: sid of the database
              database_type_id:
                type: integer
                description: database type id
          Databases:
            type: object
            properties:
              databases:
                type: array
                items:
                  $ref: '#/definitions/Database'
        responses:
          '200':
            type: object
            description: A list of Databases
            schema:
              $ref: '#/definitions/Databases'
          '401':
            description: Error if user is not authorized
            schema:
              type: string
              example: Unauthorized Access
        """
        return utils.basic_get(app.session, self.model_class, self.__class__.__name__)

    @auth.login_required
    def post(self):
        """Method to handle post requests for type tables.
        ---
        tags:
          - Databases

        security:
          - basicAuth: []

        parameters:
          - in: body
            name: database
            description: Description of the database
            schema:
              $ref: '#/definitions/DatabaseBody'

        definitions:
          DatabaseBody:
            type: object
            properties:
              description:
                type: string
                description: Database description
              host:
                type: string
                description: Hostname or ip address for the database
              port:
                type: string
                description: port used by the database
              sid:
                type: string
                description: sid of the database
              database_type_id:
                type: integer
                description: database type id

          BasicPost:
            type: object
            properties:
              status:
                type: string
                description: Message of the status
                example: Registered successfully
              id:
                type: integer
                description: Group type id
          Error:
            type: object
            properties:
              error:
                type: string
                description: Error message
                example: Invalid description provided

        responses:
          '200':
            description: Object with the status of the request, and id of the new database
            schema:
              $ref: '#/definitions/BasicPost'
          '401':
            description: Object with the status of the request
            schema:
              $ref: '#/definitions/Error'
        """
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

    def options(self):
        return dict(Allow=self.methods)
