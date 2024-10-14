# -*- coding: utf-8 -*-
{
    'name': 'Math Widget',
    'version': '18.0.1.0.1',
    'application': True,
    'summary': 'Math Field Widget',
    'description': """
This module will allow to return the math value from the field.
       """,

    'depends': [
        'base',
        'contacts',
    ],

    'data': [
        'views/res_partner.xml',
    ],

    'assets':
        {
            'web.assets_backend':
                {
                    'math_widget/static/src/js/math_widget.js',
                    'math_widget/static/src/xml/math_widget.xml',
                },
        },

    'license': 'LGPL-3',
}
