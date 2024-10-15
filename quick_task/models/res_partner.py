# -*- coding: utf-8 -*-
from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_only_ordered = fields.Boolean('Only ordered', help="Is only ordered")
