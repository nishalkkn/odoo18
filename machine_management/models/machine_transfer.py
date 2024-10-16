# -*- coding: utf-8 -*-
from odoo import models, fields, api


class MachineTransfer(models.Model):
    _name = "machine.transfer"
    _description = "Machine Transfer"
    _rec_name = 'machine_id'

    machine_id = fields.Many2one('machine.management', 'Machine', required=True, help="Name of the machine")
    serial_no = fields.Char('Serial no', help="Unique serial number of the machine")
    transfer_date = fields.Date('Transfer date', help="Transferring date")
    transfer_type = fields.Selection([('install', 'Install'), ('remove', 'Remove')], required=True,
                                     help="Type of transfer")
    customer_id = fields.Many2one('res.partner', 'Customer', help="Customer who bought the machine")
    internal_notes = fields.Html('Internal notes')
    alternate_ids = fields.Many2many('machine.management', compute='_compute_alternate_ids')
    active = fields.Boolean(default=True)
    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 default=lambda self: self.env.company, help="Company name")
    from_location = fields.Text('From Location')
    to_location = fields.Text('To Location')

    @api.onchange('machine_id')
    def _onchange_machine_id(self):
        """auto getting serial_no"""
        self.write({
            'serial_no': self.machine_id.serial_no,
        })

    def action_add_transfer(self):
        """updating values in machine.management"""
        self.machine_id.write({
            'customer_id': self.customer_id.id,
            'state': 'in_service',
        })

    @api.depends('transfer_type')
    def _compute_alternate_ids(self):
        """dynamic domain for machine_id wrt transfer_type"""
        for rec in self:
            if rec.transfer_type == 'remove':
                rec.customer_id = False
                rec.alternate_ids = rec.env['machine.management'].search([('state', '=', 'in_service')])
            elif rec.transfer_type == 'install':
                rec.alternate_ids = rec.env['machine.management'].search([('state', '=', 'active')])
            else:
                rec.alternate_ids = rec.env['machine.management'].search([])
