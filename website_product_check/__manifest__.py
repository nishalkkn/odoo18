# -*- coding: utf-8 -*-
{
    'name': "Website Product Check",
    'application': True,
    'version': '18.0.1.0.1',
    'summary': 'showing the available quantity of the product in website',
    'description': """
This module allows to showing the available quantity of the product in a particular warehouse.
    """,

    'depends': [
        'base',
        'website_sale',
    ],

    'data': [
        'views/templates.xml',
    ],

    'license': 'LGPL-3',

}
