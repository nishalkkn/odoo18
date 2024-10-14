# -*- coding: utf-8 -*-


from odoo import models, api
from odoo.exceptions import ValidationError


class HrAttendanceReport(models.AbstractModel):
    _name = "report.hr_attendance_report.hr_attendance_report"
    _description = "Hr Attendance Report"

    @api.model
    def _get_report_values(self, docids, data=None):
        """function for get pdf report values"""
        query = """select
                    hr_employee.name  as employee,
                    hr_employee.work_email  as email,
                    hr_department.complete_name  as department,
                    TO_CHAR(hr_attendance.check_in, 'HH24:MM:SS') as check_in,
                    TO_CHAR(hr_attendance.check_out, 'HH24:MM:SS') as check_out,
                    DATE(hr_attendance.check_in) as date,
                    ROUND(CAST(hr_attendance.worked_hours AS numeric),2)  as worked_hours,
                    ROUND(CAST(hr_attendance.overtime_hours AS numeric),2) as overtime_hours
                    from hr_attendance
                    inner join hr_employee on hr_employee.id = hr_attendance.employee_id
                    inner join hr_department on hr_employee.department_id = hr_department.id
                    where True"""

        if data['from_date']:
            query += """ and DATE(hr_attendance.check_in) >= '%s' """ % data['from_date']
        if data['to_date']:
            query += """ and DATE(hr_attendance.check_out) <= '%s' """ % data['to_date']
        if data['employee_id']:
            query += """ and hr_attendance.employee_id = '%s' """ % data['employee_id']
        self._cr.execute(query)
        report = self._cr.dictfetchall()

        dates = {}
        dates['from_date'] = data['from_date']
        dates['to_date'] = data['to_date']

        print(dates)

        if len(report) == 0:
            raise ValidationError("There is nothing to print")

        return {
            'report': report,
            'date': dates
        }
