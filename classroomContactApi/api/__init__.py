#! python3
from flask import Blueprint
bp = Blueprint('api', __name__, url_prefix='/api')

# Register API Version blueprint(s)
from . import v1
bp.register_blueprint(v1.bp)
