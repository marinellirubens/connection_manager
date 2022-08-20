"""Aplication to manage database connections and store information like ip,ports,services, etc.
The ideia is to store passwords, usernames, etc. in a database and then use the information to
Also server informations and types of operating systems."""

from server.app import create_app
from database.models import initiate_db

def main():
    """Main function of the application."""
    app = create_app(__name__)
    engine, session = initiate_db()
    app.engine = engine
    app.session = session
    app.run(host='0.0.0.0', port=8080, debug=False)


if __name__ == '__main__':
    main()
