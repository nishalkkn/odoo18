from odoo.http import Controller, route
from odoo.http import request


class WebTransferTrackController(Controller):
    @route('/webtransfer', type='http', auth='public', website=True)
    def web_transfer_track(self):
        """controller for showing macine transfers in website"""
        if request.env.user.has_group('machine_management.machine_manager'):
            data = request.env['machine.transfer'].search([])
        else:
            data = request.env['machine.transfer'].search([('customer_id.id', '=', request.env.user.partner_id.id)])
        value = {
            'data': data
        }
        return request.render('machine_management.web_transfer_track_template', value)

    @route('/webtransfer/<int:id>', type='http', auth='public', website=True)
    def selected_transfer(self, id):
        """controller for redirect to transfer details"""
        selected_transfer = request.env['machine.transfer'].browse(id)
        values = {
            'selected_transfer': selected_transfer
        }
        return request.render('machine_management.selected_transfer_template_details', values)
