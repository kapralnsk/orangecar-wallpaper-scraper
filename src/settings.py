from environs import Env

from enums import Teams, ImagesetSizes

env = Env()


DROPBOX_TOKEN = env("DROPBOX_TOKEN")
DOWNLOADS_ENDPNT_URL = env("DOWNLOADS_ENDPNT_URL")

STORAGE_PATH = env("STORAGE_PATH")
TIMEOUT = env("TIMEOUT", default=3)
LOG_LEVEL = env("LOG_LEVEL", default="INFO")

TEAMS = env.list("TEAMS", default=Teams._member_names_)
IMAGESET_SIZES = (env.list("IMAGESET_SIZES", default=[ImagesetSizes.ORIGINAL]),)


LOGGING = {
    "version": 1,
    "formatters": {
        "verbose": {
            "format": "[%(asctime)s] %(levelname)s: %(name)s: %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
        },
    },
}
