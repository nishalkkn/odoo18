{
    'name': 'Float Int Widget',
    'version': '18.0.1.0.1',
    'application': True,
    'summary': 'Float to Int Field Widget',
    'description': """
This module will allow to convert the float value given into its nearest int value.
       """,

    'depends': [
        'base',
        'contacts',
    ],

    'data': [
        # 'views/res_partner.xml',
    ],

    'assets':
        {
            'web.assets_backend':
                {
                    # 'float_int_widget/static/src/js/float_int.js',
                    # 'float_int_widget/static/src/xml/float_int.xml',
                },
        },

    'license': 'LGPL-3',
}
