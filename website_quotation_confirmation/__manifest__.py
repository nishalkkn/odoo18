# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Website Quotation Confirmation",
    'application': True,
    'version': '18.0.1.0.1',
    'summary': 'Website Quotation Confirmation',
    'description': """
This module add feature to allow customer to confirm quotation from the portal.
    """,

    'depends': [
        'base',
        'sale',
    ],

    'data': [
        'views/sale_portal_templates.xml',
    ],

    'license': 'LGPL-3',

}
