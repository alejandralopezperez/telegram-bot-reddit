import logging


def setup_logging():
    msg_format = '%(levelname)s: %(asctime)s - %(funcName)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=msg_format)


setup_logging()
log = logging.getLogger(__name__)
