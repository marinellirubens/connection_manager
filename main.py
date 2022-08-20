"""Aplication to manage database connections and store information like ip,ports,services, etc.
The ideia is to store passwords, usernames, etc. in a database and then use the information to
Also server informations and types of operating systems."""

from server.utils import create_app
from flask import Flask
from config.logs import set_logger


# TODO: Move that to config files or cli arguments
DIRECTORY_FILES = './files'
DIRECTORY_LOGS = './logs'
DIRECTORY_DATABASE = './sqlite'
app: Flask = create_app('main', DIRECTORY_DATABASE, DIRECTORY_LOGS, DIRECTORY_FILES)


def main():
    """Main function of the application."""
    # TODO: implement cli arguments and parsing
    # TODO: implement logging

    set_logger(app, DIRECTORY_LOGS)
    app.run(host='127.0.0.1', port='7009', debug=False)


if __name__ == '__main__':
    main()
