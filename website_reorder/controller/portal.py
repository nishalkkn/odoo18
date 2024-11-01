from odoo.addons.payment.controllers import portal as payment_portal

from odoo import http, _
from odoo.http import request


class CustomerPortal(payment_portal.PaymentPortal):

    @http.route(['/my/orders/<int:order_id>/reorder'], type='http', auth="public", methods=['POST'], website=True)
    def portal_reorder(self, order_id, access_token=None):
        # print("hi")
        # print(self)
        # print(order_id)
        order_lines = request.env['sale.order.line'].search([('order_id','=',order_id)])
        for rec in order_lines:
            print(rec.product_id)
            print(rec.product_uom_qty)
        # print(order_lines)


