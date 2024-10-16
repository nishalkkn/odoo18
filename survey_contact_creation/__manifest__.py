# -*- coding: utf-8 -*-
{
    'name': 'Surveys Contact Creation',
    'version': '18.0.1.0.1',
    'application': True,
    'summary': 'Surveys Contact Creation',
    'description': """
       """,

    'depends': [
        'base',
        'survey',
    ],

    'data': [
        'views/survey_survey_view.xml',
        'views/contact_relation.xml',
        'views/res_partner.xml',

        'security/ir.model.access.csv',
    ],

    'assets':
        {
            'web.assets_backend':
                {
                    'survey_contact_creation/static/css/ribbon.scss',
                },
        },

    'license': 'LGPL-3',
}
