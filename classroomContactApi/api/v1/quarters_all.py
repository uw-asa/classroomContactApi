#! python3
'''Chase Sawyer, 2022
University of Washington
Academic and Student Affairs, Information Services

Flask blueprint for returning all quarters within a relative range to the current time
from the EDW, then sorts them in proper chronological order before sorting them.
'''

from flask import Blueprint
from flask.json import jsonify

from classroomContactApi import _corsify_actual_response, options_preflight
from classroomContactApi.db import query_edw
from classroomContactApi.cache import cache
bp = Blueprint('quarters_all', __name__)

from flask.json import jsonify

sql_statement = '''
DECLARE @QDATE AS DATETIME = CAST(CONVERT(DATE, GETDATE(), 21) AS DATETIME);
SELECT
	aq.AcademicQtrKeyId
	,aq.AcademicYrQtrDesc
	,aq.AcademicQtr
	,aq.CalendarYr
	,aq.AcademicQtrName
	,CAST(RankTable.qtrRank AS int) AS chronoRank
FROM EDWPresentation.sec.dimAcademicQtr AS aq
JOIN 
	(SELECT AcademicContigYrQtrCode
		,RANK() OVER (ORDER BY AcademicContigYrQtrCode) AS qtrRank
	FROM EDWPresentation.sec.dimDate 
	WHERE CalendarYr BETWEEN YEAR(GETDATE())-8 and YEAR(GETDATE())+1
	AND AcademicContigYrQtrCode > (SELECT TOP 1 AcademicContigYrQtrCode FROM EDWPresentation.sec.dimDate WHERE CalendarDate = @QDATE)
	GROUP BY AcademicContigYrQtrCode

	UNION ALL

	SELECT TOP 1 AcademicContigYrQtrCode, 0 AS qtrRank
	FROM EDWPresentation.sec.dimDate 
	WHERE CalendarDate = @QDATE

	UNION ALL

	SELECT AcademicContigYrQtrCode
		,-RANK() OVER (ORDER BY AcademicContigYrQtrCode DESC) AS qtrRank
	FROM EDWPresentation.sec.dimDate 
	WHERE CalendarYr BETWEEN YEAR(GETDATE())-8 and YEAR(GETDATE())+1
	AND AcademicContigYrQtrCode < (SELECT TOP 1 AcademicContigYrQtrCode FROM EDWPresentation.sec.dimDate WHERE CalendarDate = @QDATE)
	GROUP BY AcademicContigYrQtrCode) AS RankTable
ON aq.AcademicContigYrQtrCode = RankTable.AcademicContigYrQtrCode
ORDER BY aq.AcademicQtrKeyId DESC;
'''

@bp.route('/quarters_all.json', methods=['GET', 'OPTIONS'])
@options_preflight
@cache.cached(timeout=2000, key_prefix='all_quarters')
def get_all_quarters():
    return _corsify_actual_response(jsonify(query_edw(sql_statement)))
