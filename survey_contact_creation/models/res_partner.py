# -*- coding: utf-8 -*-
from odoo import fields, models


class Survey(models.Model):
    _inherit = 'res.partner'

    from_survey = fields.Boolean('From Survey', default=False)
