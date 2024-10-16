# -*- coding: utf-8 -*-
from odoo import fields, models


class MachineInvoice(models.Model):
    _inherit = 'account.move'

    service_id = fields.Many2one('machine.service', 'Service id')
