"""Method to handle log creation."""
import logging
import logging.handlers
import os


def set_logger(app, log_dir: str = None):

    log_file_name = os.path.join(log_dir, 'api.log')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler = logging.handlers.RotatingFileHandler(log_file_name, maxBytes=1024 * 1000,
                                                   backupCount=10)

    handler.setFormatter(formatter)

    # app.logger.name = 'api'

    terminal_handler = logging.StreamHandler()
    terminal_handler.setFormatter(formatter)

    app.logger.setLevel(logging.DEBUG)
    # app.logger.setLevel(eval('logging.{}'.format("DEBUG")))
    app.logger.addHandler(handler)
    app.logger.addHandler(terminal_handler)
    app.logger.info('Logger set up' + app.logger.name)
