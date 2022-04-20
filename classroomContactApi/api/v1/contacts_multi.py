#! python3
from flask import Blueprint, request
from flask.json import jsonify

from classroomContactApi import _corsify_actual_response, options_preflight
from classroomContactApi.db import query_edw
bp = Blueprint('contacts_multi', __name__)

@bp.route('/contacts_multi.json', methods=['POST', 'OPTIONS'])
@options_preflight
def get_contacts_multi():
    json = request.get_json()
    sql_statement = f'''
        SELECT
            mt.dept_abbrev
            , mt.course_no
            , mt.section_id
            , ts.sln
            ,COALESCE(
                p.PreferredName
                , p.DisplayName
                , i.instr_name
                , ci.fac_name
            ) as DisplayName
            ,COALESCE(
                p.UWNetID
                , i.instr_netid
            ) as UWNetID
            , mtbld.bld_rm as bld_rm
        FROM UWSDBDataStore.sec.time_sched_meeting_times mt
        INNER JOIN UWSDBDataStore.sec.time_schedule ts ON 
            mt.ts_year = ts.ts_year
            AND mt.ts_quarter = ts.ts_quarter
            AND mt.course_no = ts.course_no
            AND mt.dept_abbrev = ts.dept_abbrev
            AND mt.section_id = ts.section_id
        LEFT JOIN UWSDBDataStore.sec.sr_course_instr ci ON 	
            mt.ts_year = ci.fac_yr
            AND mt.ts_quarter = ci.fac_qtr
            AND mt.course_no = ci.fac_course_no
            AND mt.dept_abbrev = ci.fac_curric_abbr
            AND mt.section_id = ci.fac_sect_id
            AND mt.index1 = ci.fac_meet_no
        LEFT JOIN UWSDBDataStore.sec.sr_instructor i ON 
            ci.fac_ssn = i.instr_ssn
            AND ci.fac_yr = i.instr_yr
            AND ci.fac_qtr = i.instr_qtr
        LEFT JOIN ODS.sec.Person p ON 
            p.EmployeeID = ci.fac_ssn
        LEFT JOIN 
            (SELECT DISTINCT
                building
                , room_number
                , CONCAT_WS(' ', TRIM(building), TRIM(room_number)) AS bld_rm
            FROM UWSDBDataStore.sec.time_sched_meeting_times
            WHERE ts_year = ?
                AND ts_quarter = ?
                AND len(trim(building)) >= 2
                AND len(trim(room_number)) >= 2
                AND trim(building) NOT LIKE '*%'
                AND trim(room_number) NOT LIKE '*%'
                AND course_branch = 0
            ) as mtbld ON
            mt.building = mtbld.building
            AND mt.room_number = mtbld.room_number
        WHERE mt.ts_year = ?
            AND mt.ts_quarter = ?
            AND len(trim(mt.building)) >= 2
            AND len(trim(mt.room_number)) >= 2
            AND trim(mt.building) NOT LIKE '*%'
            AND trim(mt.room_number) NOT LIKE '*%'
            AND mt.course_branch = 0 
            AND bld_rm IN ({(',?' * len(json['rooms']))[1:]})
            AND ts.delete_flag <> '@'
            AND ts.delete_flag <> 'S'
            AND p.UWNetID IS NOT NULL
        ORDER BY bld_rm, CASE WHEN UWNetID IS NULL THEN 1 ELSE 0 END, UWNetID
    '''
    calendar_yr = int(json['AcademicQtrKeyId'] / 10)
    academic_qtr = int(json['AcademicQtrKeyId'] % 10)
    params = [calendar_yr, academic_qtr, calendar_yr, academic_qtr] + json['rooms']
    return _corsify_actual_response(jsonify(query_edw(sql_statement, params)))
