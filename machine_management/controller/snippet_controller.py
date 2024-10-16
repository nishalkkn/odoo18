from odoo import http
from odoo.http import request


class MachineList(http.Controller):
    @http.route('/top_selling_machine', type='json', auth='public')
    def top_selling(self):
        machine = request.env['machine.management'].search_read([], ['name', 'image'], order='id desc')
        return machine
