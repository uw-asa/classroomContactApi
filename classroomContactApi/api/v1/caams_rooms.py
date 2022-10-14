#! python3
'''Chase Sawyer, 2022
University of Washington
Academic and Student Affairs, Information Services

Returns a static list of rooms that classify as having CAAMS access.
'''

from flask import Blueprint
from flask.json import jsonify

from classroomContactApi import _corsify_actual_response, options_preflight
bp = Blueprint('caams_rooms', __name__)

from flask.json import jsonify

caams_rooms = [
    'ARC 147',
    'ARC 160',
    'ARC G070',
    'BAG 260',
    'BAG 261',
    'CDH 101',
    'CDH 105',
    'CDH 109',
    'CDH 115',
    'CDH 125',
    'CDH 135',
    'CDH 139',
    'CSE2 G01',
    'CSE2 G10',
    'CSE2 G20',
    'ECE 003',
    'ECE 025',
    'ECE 026',
    'ECE 031',
    'ECE 037',
    'ECE 042',
    'ECE 045',
    'ECE 054',
    'EGL G01',
    'HRC 135',
    'HRC 145',
    'HRC 155',
    'JHN 022',
    'JHN 026',
    'JHN 075',
    'JHN 102',
    'JHN 111',
    'JHN 175',
    'MGH 030',
    'MGH 044',
    'NAN 181',
    'SMI 205',
    'SMI 211',
]

@bp.route('/caams_rooms.json', methods=['GET', 'OPTIONS'])
@options_preflight
def get_caams_rooms():
    return _corsify_actual_response(jsonify(caams_rooms))
