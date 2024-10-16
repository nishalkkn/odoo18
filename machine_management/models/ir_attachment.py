# -*- coding: utf-8 -*-
from odoo import models, fields


class Attachment(models.Model):
    _inherit = 'ir.attachment'

    attach_rel_ids = fields.Many2many('machine.service', 'attachment', 'attachment_id', 'document_id',
                                      string="Attachment")
