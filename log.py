import logging
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'handlers': {
        'stream': {
            'class': 'logging.StreamHandler',
        }, 
    },
     'root': {
        'level': 'DEBUG',
        'handlers': ['stream']
    }
})

logger = logging.getLogger(__name__)