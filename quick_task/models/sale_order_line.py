from odoo import models, _, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order.line'

    alternate_ids = fields.Many2many('product.template', compute='_compute_alternate_ids')


    @api.depends('order_id')
    def _compute_alternate_ids(self):
        for rec in self:
            if rec.order_id.partner_id.is_only_ordered:
                rec.alternate_ids = rec.env['product.template'].search([('invoice_policy', '=', 'order')])
            else:
                rec.alternate_ids = rec.env['product.template'].search([])
