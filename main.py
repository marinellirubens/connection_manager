"""Aplication to manage database connections and store information like ip,ports,services, etc.
The ideia is to store passwords, usernames, etc. in a database and then use the information to
Also server informations and types of operating systems."""

import os
from server.app import create_app
from database.utils import initiate_db


def main():
    """Main function of the application."""
    # TODO: implement cli arguments and parsing
    # TODO: implement logging
    create_directories()

    app = create_app(__name__)
    engine, session = initiate_db()
    app.engine = engine
    app.session = session
    app.run(host='0.0.0.0', port=8081, debug=False)


def create_directories():
    directories = ['logs', 'files', 'sqlite']

    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)


if __name__ == '__main__':
    main()
