import logging.config
import os
from dotenv import load_dotenv
load_dotenv()
DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

# Configuración de logging
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)d] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'logs/scraper.log',
            'formatter': 'standard',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default', 'console'],
            'level': 'DEBUG',
            'propagate': True
        },
    }
}

WEB_BASE_URL_PUBLIC = 'https://loeu.opsu.gob.ve/oferta-academica/?dep_admin=P%C3%9ABLICA&programa='
WEB_BASE_URL_PRIVATE = 'https://loeu.opsu.gob.ve/oferta-academica/?dep_admin=PRIVADA&programa='

WEB_URL_KNOWLEDGES = 'https://loeu.opsu.gob.ve/area-conocimiento/'

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)
logger.info('Logging configured')
