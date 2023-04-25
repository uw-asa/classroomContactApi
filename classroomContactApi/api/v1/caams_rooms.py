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
    'DEM 002',
    'DEM 004',
    'DEM 012',
    'DEM 024',
    'DEM 102',
    'DEM 104',
    'DEM 112',
    'DEM 124',
    'DEM 126',
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
    'MGH 074',
    'MGH 082A',
    'MGH 085',
    'MGH 097',
    'MGH 228',
    'MGH 231',
    'MGH 234',
    'MGH 238',
    'MGH 241',
    'MGH 242',
    'MGH 248',
    'MGH 251',
    'MGH 253',
    'MGH 254',
    'MGH 255',
    'MGH 271',
    'MGH 278',
    'MGH 282',
    'MGH 284',
    'MGH 286',
    'MGH 287',
    'MGH 288',
    'MGH 291',
    'MGH 295',
    'MGH 389',
    'NAN 181',
    'PCAR 192',
    'PCAR 290',
    'PCAR 291',
    'PCAR 293',
    'PCAR 295',
    'PCAR 297',
    'PCAR 391',
    'PCAR 395',
    'PCAR 492',
    'SMI 205',
    'SMI 211',
]

@bp.route('/caams_rooms.json', methods=['GET', 'OPTIONS'])
@options_preflight
def get_caams_rooms():
    return _corsify_actual_response(jsonify(caams_rooms))
