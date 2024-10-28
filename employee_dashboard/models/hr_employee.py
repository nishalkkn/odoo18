# -*- coding: utf-8 -*-
from odoo import models, api
from datetime import datetime


class HrAttendance(models.Model):
    _inherit = "hr.employee"

    @api.model
    def get_tiles_data(self):
        """ Return the tile data"""

        employees = self.search([])
        employee_data = []
        for employee in employees:
            employee_data.append({
                'name': employee.name,
                'id': employee.id,
            })

        current_employee = self.search([('user_id', '=', self.env.user.id)])
        attendance_count = self.env['hr.attendance'].search_count(
            [('employee_id', '=', current_employee.id)]) if current_employee else 0
        leave_count = self.env['hr.leave'].search_count(
            [('employee_id', '=', current_employee.id)]) if current_employee else 0
        project_count = self.env['project.project'].search_count([('user_id', '=', self.env.user.id)])
        years_of_experience = ((datetime.today() - current_employee.create_date).days) // 365
        return {
            'employees': employee_data,
            'current_employee_id': current_employee.id,
            'employee_job_title': current_employee.job_id.name,
            'years_of_experience': years_of_experience,
            'attendance_count': attendance_count,
            'leave_count': leave_count,
            'project_count': project_count,
        }
