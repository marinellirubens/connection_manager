from flask_httpauth import HTTPBasicAuth
from database.models import UserModel
from flask import Flask
from server.app import App


auth = HTTPBasicAuth()
app: Flask = App('main')


@auth.verify_password
def verify(username, password):
    global app
    if not (username and password):
        return False

    rows = app.session.query(UserModel).where(UserModel.name == username)
    print(rows.count())
    if rows.count() == 0:
        return False

    return rows[0].validate_password(password)
