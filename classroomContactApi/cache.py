#! python3
'''Chase Sawyer, 2022
University of Washington
Academic and Student Affairs, Information Services

Flask cache utility module. Configures pluggable filesystem -based request caching.
'''

import os
from flask_caching import Cache

cache = Cache(config={
    'CACHE_TYPE': 'FileSystemCache',  # Flask-Caching related configs
    'CACHE_DIR': os.path.join(os.path.curdir, 'cache'),
    'CACHE_DEFAULT_TIMEOUT': 300,
})
