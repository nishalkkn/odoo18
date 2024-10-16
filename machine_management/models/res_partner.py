# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    machine_ids = fields.One2many('machine.management', 'customer_id', string="Machine")
    alternative_cust_ids = fields.Many2many('machine.management', compute="_compute_employee_machine_count")

    @api.depends('name')
    def _compute_employee_machine_count(self):
        """domain setting for machine_ids"""
        for rec in self:
            rec.alternative_cust_ids = rec.env['machine.management'].search([('customer_id', '=', self.name)])

    def action_archive(self):
        """archiving machine belongs to customer"""
        res = super().action_archive()
        machine = self.env['machine.management'].search([('customer_id.id', '=', self.id)])
        machine.write({'active': False})
        return res

    def action_unarchive(self):
        """un-archiving machine belongs to customer"""
        res = super().action_unarchive()
        machine = self.env['machine.management'].search([('customer_id.id', '=', self.id), ('active', '=', False)])
        machine.write({'active': True})
        return res
