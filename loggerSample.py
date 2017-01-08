# Import the Standard Library modules we need
import logging
import logging.handlers

def set_up_logging():

    # Combined logger used elsewhere in the script
    logger = logging.getLogger('app-log')
    logger.setLevel(logging.DEBUG)
    return logger

logger = set_up_logging()
logger.debug('This message should go to the log file')
logger.info('So should this')
logger.warning('And this, too')