{
    'name': 'Attendances Report',
    'version': '18.0.1.0.1',
    'application': True,
    'category': 'Human Resources/Attendances',
    'summary': 'Track employee attendance',
    'description': """
This module allow employees to print their attendance report.
       """,

    'depends': [
        'hr_attendance',
    ],

    'data': [
        'wizard/hr_attendance_report_wizard.xml',

        'security/ir.model.access.csv',

        'report/ir_actions_report.xml',
        'report/hr_attendance_report.xml',
    ],

    'license': 'LGPL-3',
}
