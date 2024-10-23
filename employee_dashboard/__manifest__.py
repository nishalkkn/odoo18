# -*- coding: utf-8 -*-
{
    'name': 'Employee Dashboard',
    'version': '18.0.1.0.1',
    'application': True,
    'summary': 'Employee Dashboard',
    'description': """
This module provide the employee dashboard
""",

    'depends': [
        'base',
        'hr',
        'hr_attendance',
    ],

    'data': [
        'views/dashboard_views.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'employee_dashboard/static/src/js/dashboard.js',
            'employee_dashboard/static/src/xml/dashboard.xml',
        ],
    },

    'license': 'LGPL-3',
}
