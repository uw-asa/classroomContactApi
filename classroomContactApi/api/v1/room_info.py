#! python3
from flask import Blueprint
from flask.json import jsonify

from classroomContactApi import _corsify_actual_response, options_preflight
from classroomContactApi.db import query_edw
bp = Blueprint('room_info', __name__)

from flask.json import jsonify

sql_statement = '''
SELECT trim([sr_room_bldg]) as bld
    ,trim([sr_room_room_no]) as rm_no
    -- ,[sr_room_s25_part]
    ,CONCAT(trim([sr_room_bldg]), ' ', trim([sr_room_room_no])) as bld_rm
    ,[sr_room_capacity] as capacity
    -- ,[sr_room_no_attrib]
    ,[sr_room_gen_assgn] as gen_assign
  FROM [UWSDBDataStore].[sec].[sr_room_master]
  WHERE sr_room_campus = 0 /*Seattle*/
'''

@bp.route('/room_info.json', methods=['GET', 'OPTIONS'])
@options_preflight
def get_room_info():
    return _corsify_actual_response(jsonify(query_edw(sql_statement)))
