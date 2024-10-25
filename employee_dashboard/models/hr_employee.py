# -*- coding: utf-8 -*-
from odoo import models, api
from datetime import datetime


class HrAttendance(models.Model):
    _inherit = "hr.employee"

    @api.model
    def get_tiles_data(self):
        """ Return the tile data"""
        current_employee = self.search([('user_id', '=', self.env.user.id)])
        attendance_count = self.env['hr.attendance'].search_count(
            [('employee_id', '=', current_employee.id)]) if current_employee else 0
        leave_count = self.env['hr.leave'].search_count(
            [('employee_id', '=', current_employee.id)]) if current_employee else 0
        project_count = self.env['project.project'].search_count([('user_id', '=', self.env.user.id)])
        years_of_experience = ((datetime.today() - current_employee.create_date).days) // 365
        return {
            'current_employee_id': current_employee.id,
            'employee_job_title': current_employee.job_id.name,
            'years_of_experience': years_of_experience,
            'attendance_count': attendance_count,
            'leave_count': leave_count,
            'project_count': project_count,
        }

    @api.model
    def get_org_chart_data(self):
        """ Return the organization chart data for the current employee"""
        current_employee = self.search([('user_id', '=', self.env.user.id)])
        if current_employee:
            parent_id = current_employee.parent_id
            child_ids = self.search([('parent_id', '=', current_employee.id)])
            if parent_id:
                org_chart_html = f"<div style='color: #bf80ff;'>{parent_id.name}</div>"
                org_chart_html += f"<div style='margin-left: 20px;' class='o_treeEntry py-2'>{current_employee.name}</div>"
                org_chart_html += ''.join(
                    f"<div style='margin-left: 40px; color: #bf80ff;' class='o_treeEntry py-2'>{rec.name}</div>"
                    for rec in child_ids)
                return org_chart_html
            org_chart_html = f"<div>{current_employee.name}</div>"
            org_chart_html += ''.join(
                f"<div style='margin-left: 20px; color: #bf80ff;' class='o_treeEntry py-2'>{rec.name}</div>" for
                rec in child_ids)
            return org_chart_html
        return ""
