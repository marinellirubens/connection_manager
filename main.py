"""Aplication to manage database connections and store information like ip,ports,services, etc.
The ideia is to store passwords, usernames, etc. in a database and then use the information to
Also server informations and types of operating systems."""
import os

from config.logs import set_logger
from server.utils import create_app


def main(*args, **kwargs):
    """Main function of the application."""
    directory_files = kwargs.get('directory_files', './files')
    directory_logs = kwargs.get('directory_logs', './logs')
    directory_database = kwargs.get('directory_database', './sqlite')

    app = create_app('main', directory_database, directory_logs, directory_files)
    app.logger.info(os.getenv('ADMIN_PASSWORD'))

    if kwargs.get('debug', False):
        set_logger(app, directory_logs)
        app.run(host='127.0.0.1', port='7009', debug=False)
    return app


if __name__ == '__main__':
    main()
