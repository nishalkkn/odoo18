# -*- coding: utf-8 -*-
import xmlrpc.client

from odoo import models


class PurchaseMigrationWizard(models.TransientModel):
    _name = "purchase.migration.wizard"
    _description = "Purchase Order Migration Wizard"

    def fetch_po(self):
        url_db1 = "http://localhost:8016"
        db_1 = 'odoo17'
        username_db_1 = '2'
        password_db_1 = '2'
        common_1 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url_db1))
        models_1 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url_db1))
        version_db1 = common_1.version()

        url_db2 = "http://cybrosys:8018"
        db_2 = 'odoo18_migration'
        username_db_2 = '2'
        password_db_2 = '2'
        common_2 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url_db2))
        models_2 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url_db2))
        version_db2 = common_2.version()

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
        db_1_po = models_1.execute_kw(db_1, uid_db1, password_db_1, 'purchase.order', 'search_read', [],
                                      {'fields': ['id','name', 'partner_id', 'user_id', 'amount_total']})

        # creating res_partner in odoo 18 database
        [models_2.execute_kw(db_2, uid_db2, password_db_2, 'res.partner', 'create', [rec]) for rec in
         db_1_partners if not self.env['res.partner'].search_read([('name', '=', rec['name'])])]
        # creating product_template in odoo 18 database
        [models_2.execute_kw(db_2, uid_db2, password_db_2, 'product.template', 'create', [rec]) for rec in
         db_1_products if not self.env['product.template'].search_read([('name', '=', rec['name'])])]



        # for rec in db_1_po:
        #     new_purchase = models_2.execute_kw(db_2, uid_db2, password_db_2, 'purchase.order', 'create', [{
        #         'id': rec['id'],
        #         'name': rec['name'],
        #         'partner_id': rec['partner_id'],
        #         'user_id': rec['user_id'],
        #     }])
