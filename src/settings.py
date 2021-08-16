from environs import Env

env = Env()


DROPBOX_TOKEN = env('DROPBOX_TOKEN')
URL = env('URL')
STORAGE_PATH = env('STORAGE_PATH')
TIMEOUT = env('TIMEOUT', default=3)
LOG_LEVEL = env('LOG_LEVEL', default='INFO')

LOGGING = {
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s: %(name)s: %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': LOG_LEVEL,
        },
    },
}

