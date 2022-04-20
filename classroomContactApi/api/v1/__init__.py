#! python3
from flask import Blueprint
bp = Blueprint('v1', __name__, url_prefix='/v1')

from . import (
    quarters_all,
    asa_rooms,
    room_info,
    contacts_multi,
    quarter_rooms,
)

bp.register_blueprint(quarters_all.bp)
bp.register_blueprint(asa_rooms.bp)
bp.register_blueprint(room_info.bp)
bp.register_blueprint(contacts_multi.bp)
bp.register_blueprint(quarter_rooms.bp)
