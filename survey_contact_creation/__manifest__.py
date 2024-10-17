# -*- coding: utf-8 -*-
{
    'name': 'Surveys Contact Creation',
    'version': '18.0.1.0.1',
    'application': True,
    'summary': 'Surveys Contact Creation',
    'description': """
This module allow to create contact from survey
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

    'license': 'LGPL-3',
}
