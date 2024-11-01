from odoo import models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_reorder(self):
        print("hello")

