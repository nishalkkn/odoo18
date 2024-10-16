# -*- coding: utf-8 -*-
from odoo import models, fields


class MachineType(models.Model):
    _name = 'machine.type'
    _description = 'Machine Type'

    name = fields.Char('Machine Type', help="Machine type")
