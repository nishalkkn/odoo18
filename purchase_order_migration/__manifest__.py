# -*- coding: utf-8 -*-
{
    'name': 'Purchase Order Migration',
    'application': True,
    'version': '18.0.1.0.1',
    'summary': 'Purchase Order Migration',
    'description': """
This module allow to migrate purchase orders from odoo17 to odoo18
    """,

    'depends': [
        'base',
        'purchase',
    ],

    'data': [
        'security/ir.model.access.csv',

        'wizard/purchase_migration_wizard.xml',
    ],

    'license': 'LGPL-3',

}
