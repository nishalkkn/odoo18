# -*- coding: utf-8 -*-
from odoo import models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def get_warehouse_stock_info(self):
        """function to get the available quantity of the selected product wrt warehouses inside website product view."""
        product_product_ids = self.env['product.product'].sudo().search([('product_tmpl_id', '=', self.id)])
        warehouses = self.env['stock.warehouse'].sudo().search([('company_id', '=', self.env.company.id)])
        return [{
            'warehouse_name': warehouse.name,
            'quantity': sum(product_id.with_context(warehouse_id=warehouse.id).virtual_available for product_id in
                            product_product_ids),
        } for warehouse in warehouses]
