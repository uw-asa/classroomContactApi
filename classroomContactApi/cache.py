#! python3
import os
from flask_caching import Cache

cache = Cache(config={
    'CACHE_TYPE': 'FileSystemCache',  # Flask-Caching related configs
    'CACHE_DIR': os.path.join(os.path.curdir, 'cache'),
    'CACHE_DEFAULT_TIMEOUT': 300,
})
