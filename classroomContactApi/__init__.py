#! python3
'''Chase Sawyer, 2022
University of Washington
Academic and Student Affairs, Information Services

Flask application root for the classroom contacts tool api.
'''

import os
import functools
from flask import Flask, request, make_response

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLITE_DATABASE=os.path.join(app.instance_path, 'cct_templates.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # setup databases
    from . import db
    db.init_app(app)

    from . import api
    app.register_blueprint(api.bp)

    from .cache import cache
    cache.init_app(app)

    return app

def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    response.headers.add("Access-Control-Max-Age", 60)
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

def options_preflight(func):
    @functools.wraps(func)
    def wrapper_options_preflight(*args, **kwargs):
        if request.method == "OPTIONS":  #CORS Preflight
            return _build_cors_preflight_response()
        return func(*args, **kwargs)
    return wrapper_options_preflight
