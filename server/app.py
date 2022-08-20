"""Method to handle requests to the server."""
import os
import uuid
from crypt import methods

from database.models import DatabaseTypeModel
from flask import Flask, Response, jsonify, request, send_file
from flask_restful import Api, Resource
from sqlalchemy import func


app: Flask


class DatabaseTypes(Resource):
    def get(self):
        rows = app.session.query(DatabaseTypeModel).all()
        
        return {'Database types': [row.to_json() for row in rows]}

class DatabaseType(Resource):
    def get(self, param):
        row = app.session.query(DatabaseTypeModel).where(DatabaseTypeModel.id == param)
        
        if row.count() == 0:
            return {'error': 'No database type found'}, 401

        return row[0].to_json()
    
    def post(self, param):
        row = app.session.query(DatabaseTypeModel).where(DatabaseTypeModel.description == param)
        
        if row.count() > 0:
            return {'error': 'database type id already exists', 'database_type_id': row[0].id}, 401
        
        max_id = app.session.query(func.max(DatabaseTypeModel.id))[0]
        max_id = int(max_id[0]) + 1
        app.session.bulk_save_objects([DatabaseType(max_id, param)])
        app.session.commit()

        return jsonify(message=f'Database type {max_id} created successfully', database_id=max_id)


class Teste(Resource):
    """Class to handle requests to the server."""
    def get(self, file_id=None) -> Response:
        """Method to handle requests to the server."""
        if not os.path.exists(os.path.join('files', file_id)):
            return {'error': 'file not found'}, 404
        
        return send_file(
            path_or_file=open(os.path.join('files', file_id), 'rb'),
            download_name=file_id,
            mimetype='image/png')
    
    def post(self) -> Response:
        """Method to handle requests to the server."""
        request_data = request.files['teste']
        file_id = str(uuid.uuid4())
        request_data.save(os.path.join('files', file_id))
        return {'file_id': file_id}, 200
    
    def delete(self, file_id) -> Response:
        if not os.path.exists(os.path.join('files', file_id)):
            return {'error': 'file not found'}, 404

        os.remove(os.path.join('files', file_id))
        return {'message': 'file deleted'}, 200


def create_app(app_name: str) -> Flask:
    """Method to handle requests to the server."""
    global app

    app = Flask(app_name)
    api = Api(app)

    # api.add_resource(Database, '/', methods=['PUT'])
    api.add_resource(DatabaseType,
                     '/database_type/<param>',
                     methods=['GET', 'POST', 'DELETE'])
    api.add_resource(DatabaseTypes, '/database_type/', methods=['GET'])
    return app