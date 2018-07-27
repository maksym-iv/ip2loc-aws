import os


def str2bool(v):
  return str(v).lower() in ("yes", "true", "t", "1")


DEBUG = str2bool(os.getenv('DEBUG', True))
DB_FILE = os.environ['DB_FILE']
CSV_DELIMITER = os.environ['CSV_DELIMITER']