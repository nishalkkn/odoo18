# -*- coding: utf-8 -*-
from odoo import models, fields, api


class MachinePart(models.Model):
    _name = "machine.part"
    _description = "Machine Part"

    machine_id = fields.Many2one('machine.management', 'Machine', help="Machine name")
    product_id = fields.Many2one('product.product', 'Machine Parts', help="Parts used for machine")
    quantity = fields.Integer('Quantity', help="Quantity of the machine part")
    uom = fields.Char('Unit of measure', help="Unit of measure")

    @api.onchange('product_id')
    def onchange_machine_id(self):
        """auto assigning uom"""
        self.write({
            'uom': self.product_id.uom_id.name
        })
