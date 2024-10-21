# -*- coding: utf-8 -*-
import xmlrpc.client

from odoo import models,fields


class PurchaseMigrationWizard(models.TransientModel):
    _name = "purchase.migration.wizard"
    _description = "Purchase Order Migration Wizard"

    is_product = fields.Boolean('Product', help="Fetch product")
    is_goods = fields.Boolean('Goods', help="Goods")
    is_service = fields.Boolean('Service', help="Service")
    is_combo = fields.Boolean('Combo', help="Combo")
    is_po = fields.Boolean('Purchase order', help="Purchase order")
    is_rfq = fields.Boolean('RFQ', help="RFQ")
    is_rfq_sent = fields.Boolean('RFQ Sent', help="RFQ Sent")
    is_to_approve = fields.Boolean('To Approve', help="To Approve")
    is_purchase = fields.Boolean('Purchase Order', help="Purchase order")
    is_done = fields.Boolean('Locked', help="Locked")
    is_cancelled = fields.Boolean('Cancelled', help="Cancelled")


    def action_fetch_po(self):
        """This is the function to fetch purchase order from odoo 17 and migrate it to odoo 18
        on a button click from a wizard."""
        url_db1 = "http://localhost:8016"
        db_1 = 'odoo17'
        username_db_1 = '2'
        password_db_1 = '2'
        common_1 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url_db1))
        models_1 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url_db1))

        url_db2 = "http://cybrosys:8018"
        db_2 = 'odoo18_migration'
        username_db_2 = '2'
        password_db_2 = '2'
        common_2 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url_db2))
        models_2 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url_db2))

        uid_db1 = common_1.authenticate(db_1, username_db_1, password_db_1, {})
        uid_db2 = common_2.authenticate(db_2, username_db_2, password_db_2, {})

        # fetching res_partner from odoo 17 database
        db_1_partners = models_1.execute_kw(db_1, uid_db1, password_db_1, 'res.partner', 'search_read', [],
                                            {'fields': ['id', 'name', 'complete_name', 'company_name', 'email', 'phone',
                                                        'is_company']})
        # fetching product_template from odoo 17 database
        db_1_products = models_1.execute_kw(db_1, uid_db1, password_db_1, 'product.template', 'search_read', [],
                                            {'fields': ['name', 'type', 'list_price', 'default_code', 'purchase_ok',
                                                        'standard_price']})
        # fetching purchase order from odoo 17 database
        db_1_po = models_1.execute_kw(db_1, uid_db1, password_db_1, 'purchase.order', 'search_read', [],
                                      {'fields': ['id', 'name', 'partner_id', 'user_id', 'amount_total', 'order_line',
                                                  'state']})

        # creating res_partner in odoo 18 database
        [models_2.execute_kw(db_2, uid_db2, password_db_2, 'res.partner', 'create', [rec]) for rec in
         db_1_partners if not self.env['res.partner'].search_read([('name', '=', rec['name'])])]
        # creating product_template in odoo 18 database
        [models_2.execute_kw(db_2, uid_db2, password_db_2, 'product.template', 'create', [rec]) for rec in
         db_1_products if not self.env['product.template'].search_read([('name', '=', rec['name'])])]

        # creating purchase order in odoo 18 database
        for rec in db_1_po:
            partner = self.env['res.partner'].search([('complete_name', '=', rec['partner_id'][1])]).id
            db_2_po = self.env['purchase.order'].search_read([('name', '=', rec['name'])])
            if partner and not db_2_po:
                db2_po_new = models_2.execute_kw(db_2, uid_db2, password_db_2, 'purchase.order', 'create', [{
                    'id': rec['id'],
                    'name': rec['name'],
                    'partner_id': partner,
                    'amount_total': rec['amount_total'],
                    'state': rec['state']
                }])
                db1_order_line = models_1.execute_kw(db_1, uid_db1, password_db_1, 'purchase.order.line', 'search_read',
                                                     [], {'domain': [('id', 'in', rec['order_line'])],
                                                          'fields': ['product_id', 'product_qty', 'price_unit']})
                # creating purchase order line
                [models_2.execute_kw(db_2, uid_db2, password_db_2, 'purchase.order.line', 'create', [{
                    'product_id': self.env['product.template'].search(
                        [('name', '=', line['product_id'][1].split(']')[-1].strip())]).id,
                    'product_qty': line['product_qty'],
                    'price_unit': line['price_unit'],
                    'order_id': db2_po_new
                }]) for line in db1_order_line if self.env['product.template'].search(
                    [('name', '=', line['product_id'][1].split(']')[-1].strip())]).id]
