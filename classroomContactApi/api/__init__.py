#! python3
'''Chase Sawyer, 2022
University of Washington
Academic and Student Affairs, Information Services

Flask blueprint - Root of API routes.
'''

from flask import Blueprint
bp = Blueprint('api', __name__, url_prefix='/api')

# Register API Version blueprint(s)
from . import v1
bp.register_blueprint(v1.bp)
