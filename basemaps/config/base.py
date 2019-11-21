import os
from basemaps.utils.files import BASE_DIR

SETTINGS = {
    'logging': {
        'level': 'DEBUG'
    },
    'service': {
        'port': 4502
    },
    'gee': {
        'service_account': 'skydipper@skydipper-196010.iam.gserviceaccount.com',
        'privatekey_file': BASE_DIR + '/privatekey.json',
        'assets': {}
        },
    'redis': {
            'url': os.getenv('REDIS_URL')
            }
    }