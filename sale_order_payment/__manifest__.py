{
    'name': 'Sale order payment',
    'application': True,
    'version': '18.0.1.0.1',
    'summary': 'Sale order payment',
    'description': """
This is a base module for show the register payment button in sale order and make register the payment from sale order
    """,

    'depends': [
        'sale',
    ],
    'data': [
        'views/sale_order_payment.xml'
    ],

    'license': 'LGPL-3'

}
