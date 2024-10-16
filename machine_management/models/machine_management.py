# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class MachineManagement(models.Model):
    _name = "machine.management"
    _description = "Machine Management"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Name', required=True, help="name of the machine")
    purchase_value = fields.Float('Purchase value', help="Purchase value of the machine")
    customer_id = fields.Many2one('res.partner', 'Customer', help="The value of machine when purchased", readonly=True)
    description = fields.Text('Description')
    warranty = fields.Boolean('Warranty', help="Is any warranty for machine")
    machine_instructions = fields.Html('Machine instructions')
    # image = fields.Image('image', help="Image of the machine")
    image = fields.Binary('imagesss', help="Image of the machine")
    state = fields.Selection(selection=[
        ('active', 'Active'),
        ('in_service', 'In service'),
    ], string='Status', required=True, copy=False,
        tracking=True, default='active')
    serial_no = fields.Char('Serial no', help="Unique serial number for machine")
    sequence_no = fields.Char("Sequence no", default=lambda self: _("New"),
                              copy=False, readonly=True, tracking=True)
    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 default=lambda self: self.env.company, help="Company name")
    machine_type_id = fields.Many2one('machine.type', 'Machine Type', help="Which is the type of the machine")
    transfer_count = fields.Integer(compute='_compute_count_of_transfer')
    service_count = fields.Integer(compute='_compute_count_of_service')
    machine_tag_ids = fields.Many2many('machine.tag', string='Machine Tag', help="Machine tags")
    machine_part_ids = fields.One2many('machine.part', 'machine_id', 'Machine Parts', help="Parts used for machine")
    date_of_purchase = fields.Date('Purchase date', help="Purchase date of machine")
    today_date = fields.Date(default=fields.date.today())
    total_days = fields.Integer('Age (Days)', help="Age of the machine")
    active = fields.Boolean(default=True)

    @api.onchange('date_of_purchase')
    def onchange_calculate_date(self):
        """Finding the age of the machine"""
        if self.date_of_purchase and self.today_date:
            purchase_date = datetime.strptime(str(self.date_of_purchase), '%Y-%m-%d')
            today_date = datetime.strptime(str(self.today_date), '%Y-%m-%d')
            self.total_days = (today_date - purchase_date).days

    def action_get_transfer_count(self):
        """smart button for transfers"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Transfer',
            'view_mode': 'tree,form',
            'res_model': 'machine.transfer',
            'domain': [('machine_id', '=', self.id)],
            'context': "{'create': False}"
        }

    def _compute_count_of_transfer(self):
        """computing count of transfers"""
        for rec in self:
            rec.transfer_count = rec.env['machine.transfer'].search_count([('machine_id', '=', rec.id)])

    @api.model_create_multi
    def create(self, vals_list):
        """code for sequence number"""
        for vals in vals_list:
            if vals.get('sequence_no', _('New')) == _('New'):
                vals['sequence_no'] = self.env['ir.sequence'].next_by_code('machine.management')
        return super().create(vals_list)

    @api.constrains('purchase_value')
    def check_negative_number(self):
        """making purchase value positive"""
        if self.purchase_value <= 0:
            raise ValidationError("Purchase value must be a positive number")

    @api.constrains('serial_no')
    def check_registration_no(self):
        """making serial number unique"""
        domain = [('serial_no', '=', self.serial_no)]
        count = self.search_count(domain)
        if count > 1:
            raise ValidationError(_("The Serial number should be unique"))

    def action_transfer_machine_button(self):
        """button to navigate to machine.transfer"""
        return {
            'name': 'Machine Transfer',
            'res_model': 'machine.transfer',
            'type': 'ir.actions.act_window',
            'view_type': 'tree,form',
            'view_mode': 'form',
            'context': {'default_machine_id': self.id},
            'target': 'current'
        }

    def action_create_service_button(self):
        """button to navigate to machine.service"""
        return {
            'name': 'Machine Service',
            'res_model': 'machine.service',
            'type': 'ir.actions.act_window',
            'view_type': 'tree,form',
            'view_mode': 'form',
            'context': {'default_machine_id': self.id},
            'target': 'current'
        }

    def action_get_service_count(self):
        """smart button for services"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Services',
            'view_mode': 'tree,form',
            'res_model': 'machine.service',
            'domain': [('machine_id', '=', self.id)],
            'context': "{'create': False}"
        }

    def _compute_count_of_service(self):
        """computing count of services"""
        for rec in self:
            rec.service_count = rec.env['machine.service'].search_count([('machine_id', '=', rec.id)])

    @api.ondelete(at_uninstall=False)
    def ondelete_machine(self):
        """on delete function for machine"""
        if self.transfer_count > 0 or self.service_count > 0:
            raise ValidationError("You can't delete a machine when there is a transfer or  a service ")

    def action_archive(self):
        """archive function for machine"""
        if not self.env.user.has_group('machine_management.machine_manager'):
            raise ValidationError("Only Manager can archive machine")
        if self.state == 'in_service':
            raise ValidationError("You can only archive the machine in active state")
        res = super().action_archive()
        machine_transfer = self.env['machine.transfer'].search([('machine_id.id', '=', self.id)])
        machine_transfer.write({'active': False})
        machine_service = self.env['machine.service'].search([('machine_id.id', '=', self.id), ('state', '=', 'open')])
        if machine_service:
            machine_service.write({'state': 'cancel'})
            notification = {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Warning'),
                    'type': 'warning',
                    'message': 'We cancelling the open machine services',
                    'sticky': True,
                }
            }
            return notification
        return res
