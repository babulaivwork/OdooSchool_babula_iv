{
    'name': 'QWeb Tutorial',
    'version': '19.0.1.0.0',
    'author': 'Odoo School',
    'website': 'https://odoo.school/',
    'category': 'Tools',
    'summary': 'Module to teach QWeb rendering',
    'license': 'LGPL-3',
    'depends': ['base', 'mail', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'data/qweb_tutorial_data.xml',
        'views/qweb_tutorial_views.xml',
        'views/templates.xml',
    ],
    'installable': True,
    'application': True,
}
