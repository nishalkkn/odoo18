from odoo import fields, models


class AccountMoveLine(models.Model):
    """Adding Product Type field to Account Move Line model."""
    _inherit = ["account.move.line"]

    product_type = fields.Selection([('room', 'Room'), ('food', 'Food'),
                                     ('event', 'Event'),
                                     ('service', 'Service'),
                                     ('fleet', 'Fleet')],
                                    default="room",
                                    string="Product Type",
                                    help="Choose the product type")
