from odoo import http
from odoo.http import request


class WebsiteReorder(http.Controller):

    @http.route(['/order/<int:order_id>/reorder'], type='http', auth="user", methods=['POST'], website=True)
    def portal_reorder(self, order_id):
        """update the cart on button click"""
        sale_order = request.env['sale.order'].sudo().browse(order_id)
        cart = request.website.sale_get_order(force_create=True)
        for rec in sale_order.order_line:
            if rec.product_id:
                existing_cart = cart.order_line.filtered(lambda l: l.product_id == rec.product_id)
                if existing_cart:
                    product_qty = rec.product_uom_qty + existing_cart.product_uom_qty
                else:
                    product_qty = rec.product_uom_qty
                cart._cart_update(
                    product_id=rec.product_id.id,
                    set_qty=product_qty,
                )
        return request.redirect("/shop/cart")
