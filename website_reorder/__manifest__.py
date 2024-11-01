# -*- coding: utf-8 -*-
{
    'name': "Website Reorder",
    'application': True,
    'version': '18.0.1.0.1',
    'summary': 'Reordering from the customer portal',
    'description': """
This module allows to set reorder from customer portal.
    """,

    'depends': [
        'base',
        'sale',
        'website'
    ],

    'data': [
        'views/sale_portal_templates.xml',
    ],

    'license': 'LGPL-3',

}
