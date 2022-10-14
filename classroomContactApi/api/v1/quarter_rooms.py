#! python3
'''Chase Sawyer, 2022
University of Washington
Academic and Student Affairs, Information Services

Gathers the distinct rooms that are scheduled for a particular quarter and year, selected by the user.
This way the following queries can only select from rooms that have classes actually scheduled in them.
'''

from flask import Blueprint, request
from flask.json import jsonify

from classroomContactApi import _corsify_actual_response, options_preflight
from classroomContactApi.db import query_edw
from classroomContactApi.cache import cache
bp = Blueprint('quarter_rooms', __name__)


@bp.route('/quarter_rooms.json', methods=['GET', 'OPTIONS'])
@options_preflight
@cache.cached(timeout=2000, key_prefix='quarter_rooms', query_string=True)
def get_quarter_rooms():
    sql_statement = '''
        SELECT DISTINCT
            trim(building) as building
            ,trim(room_number)as room_number
            ,CONCAT(trim(building), ' ', trim(room_number)) as building_room
        FROM UWSDBDataStore.sec.time_sched_meeting_times
        WHERE ts_year = ?
            AND ts_quarter = ?
            AND len(trim(building)) >= 2
            AND len(trim(room_number)) >= 2
            AND trim(building) NOT LIKE '*%'
            AND trim(room_number) NOT LIKE '*%'
            AND course_branch = 0 /* course branch: 0=seattle, 1=bothell, 2=tacoma */
        ORDER BY trim(building), trim(room_number)
    '''
    calendar_yr = int(int(request.args['AcademicQtrKeyId']) / 10)
    academic_qtr = int(int(request.args['AcademicQtrKeyId']) % 10)
    return _corsify_actual_response(jsonify(query_edw(sql_statement, [calendar_yr, academic_qtr])))
