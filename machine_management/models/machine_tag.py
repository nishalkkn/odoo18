# -*- coding: utf-8 -*-
from odoo import models, fields


class MachineTag(models.Model):
    _name = "machine.tag"
    _description = "Machine Tags"

    name = fields.Char('Tag', help="Name of the tag")
    color = fields.Integer('Color')
