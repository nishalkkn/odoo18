from odoo import models, _, fields, api


class SaleOrderPayment(models.Model):
    _inherit = 'sale.order'

    payment = fields.Boolean(default=False)
    button_state = fields.Selection(selection=[('hidden', 'Hidden'), ('visible', 'Visible')], required=True, copy=False,
                                    store=True, tracking=True, default='hidden', compute='_compute_button_state')
    fully_paid_ribbon = fields.Boolean(default=False)
    partial_paid_ribbon = fields.Boolean(default=False)

    def action_register_payment(self):
        """button for register payment in sale order"""
        return {
            'name': _('Register Payment'),
            'res_model': 'account.payment.register',
            'view_mode': 'form',
            'views': [[False, 'form']],
            'context': {
                'active_model': 'account.move',
                'active_ids': self.invoice_ids.ids,
            },
            'target': 'new',
            'type': 'ir.actions.act_window',
        }

    @api.depends('invoice_ids.payment_state', 'invoice_ids.state')
    def _compute_button_state(self):
        """computing the button state"""
        for rec in self:
            if rec.invoice_ids:
                payment_state = rec.invoice_ids.mapped('payment_state')
                for invoice in rec.invoice_ids:
                    if invoice.state == 'posted':
                        rec.write({
                            'button_state': 'visible'
                        })
                    if 'paid' in payment_state:
                        rec.write({
                            'partial_paid_ribbon': True
                        })
                if 'paid' in payment_state and 'not_paid' not in payment_state:
                    rec.write({
                        'button_state': 'hidden',
                        'partial_paid_ribbon': False,
                        'fully_paid_ribbon': True
                    })
