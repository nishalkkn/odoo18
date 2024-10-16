import base64

from odoo import Command
from odoo.http import Controller, route
from odoo.http import request


class WebFormController(Controller):
    @route('/webform', auth='public', website=True)
    def web_form(self):
        """controller to open view form in website """
        return request.render('machine_management.web_form_template')

    @route('/webform/submit', type='http', auth='public', website=True, methods=['POST'])
    def web_form_submit(self, **post):
        """controller when submitting service request form"""
        attachment = request.env['ir.attachment']
        files = request.httprequest.files.getlist('image')
        machine_service = request.env['machine.service'].sudo().create({
            'customer_id': request.env.user.partner_id.id,
            'machine_id': post.get('machine_id'),
            'service_frequency': post.get('service_frequency'),
            'last_service_date': post.get('last_service_date'),
            'state': 'request',
        })
        for file in files:
            attachment_id = attachment.create({
                'name': file.filename,
                'type': 'binary',
                'datas': base64.b64encode(file.read()),
            })
            machine_service.write({
                'attachment_ids': [Command.link(attachment_id.id)]
            })
        return request.redirect('/service-thank-you')
