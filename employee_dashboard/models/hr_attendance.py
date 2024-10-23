# -*- coding: utf-8 -*-
from odoo import models, api


class HrAttendance(models.Model):
    _inherit = "hr.employee"

    @api.model
    def get_tiles_data(self):
        """ Return the tile data"""
        current_employee = self.search([('user_id', '=', self.env.user.id)])

        attendance_count = self.env['hr.attendance'].search_count(
            [('employee_id', '=', current_employee.id)]) if current_employee else 0
        total_attendance_count = self.env['hr.attendance'].search_count([])

        leave_count = self.env['hr.leave'].search_count(
            [('employee_id', '=', current_employee.id)]) if current_employee else 0
        total_leave_count = self.env['hr.leave'].search_count([])

        project_count = self.env['project.project'].search_count([('user_id', '=', self.env.user.id)])
        total_project_count = self.env['project.project'].search_count([])

        return {
            'attendance_count': attendance_count,
            'total_attendance_count': total_attendance_count,
            'leave_count': leave_count,
            'total_leave_count': total_leave_count,
            'project_count': project_count,
            'total_project_count': total_project_count,
        }
