from odoo.addons.payment.controllers import portal as payment_portal

from odoo import http, _
from odoo.http import request


class CustomerPortal(payment_portal.PaymentPortal):

    @http.route(['/my/orders/<int:order_id>/confirm'], type='http', auth="public", methods=['POST'], website=True)
    def portal_quote_confirm(self, order_id, access_token=None):
        """function working on confirm button"""
        order_sudo = self._document_check_access('sale.order', order_id, access_token=access_token)
        order_sudo.with_context(send_email=True).action_confirm()

        # redirect url to show confirm message on the window
        redirect_url = order_sudo.get_portal_url(query_string="&message=sign_ok")

        # message shown on portal chatter when order confirmed
        order_sudo.message_post(
            author_id=(
                order_sudo.partner_id.id
                if request.env.user._is_public()
                else request.env.user.partner_id.id
            ),
            body=_('The Order has been confirmed by OdooBot', ),
            message_type='comment',
            subtype_xmlid='mail.mt_comment',
        )
        return request.redirect(redirect_url)
