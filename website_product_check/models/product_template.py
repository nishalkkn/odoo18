from odoo import models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def get_warehouse_stock_info(self):
        stock_info = []
        warehouses = self.env['stock.warehouse'].search([])
        for warehouse in warehouses:
            total_quantity = 0
            locations = self.env['stock.location'].search([('warehouse_id', '=', warehouse.id)])
            for location in locations:
                quantity = self.env['stock.quant'].search(
                    [('product_id', '=', self.id), ('location_id', '=', location.id)],
                    limit=1)
                total_quantity += quantity.quantity if quantity else 0
            stock_info.append({
                'warehouse_name': warehouse.name,
                'quantity': total_quantity,
            })
            return stock_info
