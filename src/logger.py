import logging
import sys

import settings


# FORMAT = '%(asctime)s %(levelname)s:%(module)s:%(lineno)s: %(message)s'
FORMAT = '[%(levelname)s] %(asctime)s :%(filename)s:%(lineno)s: %(message)s'
FORMAT = logging.Formatter(FORMAT)

general_logger = logging.getLogger('log')

if settings.DEBUG == True:
    general_logger.setLevel(logging.DEBUG)
else:
    general_logger.setLevel(logging.INFO)

if general_logger.handlers:
    for handler in general_logger.handlers:
        general_logger.removeHandler(handler)

ch = logging.StreamHandler(sys.stdout)  # console handler
ch.setFormatter(FORMAT)

general_logger.addHandler(ch)
