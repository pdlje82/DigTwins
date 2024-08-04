# logger_config.py
import logging
import logging.config

def setup_logging(default_level=logging.INFO):
    """
    Set up logging configuration.
    """
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
            },
            'file_main': {
                'class': 'logging.FileHandler',
                'formatter': 'standard',
                'filename': 'main.log',
                'mode': 'a',
            },
            'file_data': {
                'class': 'logging.FileHandler',
                'formatter': 'standard',
                'filename': 'data.log',
                'mode': 'a',
            },
        },
        'loggers': {
            'main': {
                'handlers': ['console', 'file_main'],
                'level': default_level,
                'propagate': False,
            },
            'data': {
                'handlers': ['console', 'file_data'],
                'level': default_level,
                'propagate': False,
            },
            'utils_geo': {
                'handlers': ['console', 'file_data'],
                'level': default_level,
                'propagate': False,
            },
            'torch_img': {
                'handlers': ['console', 'file_data'],
                'level': default_level,
                'propagate': False,
            },
        },
        'root': {
            'handlers': ['console'],
            'level': default_level,
        },
    }

    logging.config.dictConfig(logging_config)

# Initialize logging setup
setup_logging()
