# -*- coding: utf-8 -*-

from odoo import fields, models


class HrAttendanceReportWizard(models.TransientModel):
    _name = 'hr.attendance.report.wizard'
    _description = "Hr Attendance Report Wizard"

    from_date = fields.Date('From Date', help="Attendance shown from which date")
    to_date = fields.Date('To Date', help="Attendance shown upto which date")
    employee_id = fields.Many2one('hr.employee', 'Employee', help="Attendance shown for which employee")

    def action_print_record(self):
        """print pdf button in wizard"""
        data = {
            'from_date': self.from_date,
            'to_date': self.to_date,
            'employee_id': self.employee_id.id,
        }
        return self.env.ref('hr_attendance_report.action_report_hr_attendance').report_action(None, data=data)
