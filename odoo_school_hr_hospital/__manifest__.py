{
    'name': 'Odoo School HR Hospital',
    'author': 'Odoo School Student',
    'website': 'https://odoo.school/',
    'category': 'Customizations',
    'version': '19.0.13.0.0',
    'license': 'OPL-1',

    'depends': [
        'base',
        'web',
    ],

    'external_dependencies': {
        'python': []
    },

    'data': [
        'security/odoo_school_hr_hospital_groups.xml',
        'security/odoo_school_hr_hospital_visit_security.xml',
        'security/ir.model.access.csv',
        'wizard/odoo_school_hr_hospital_mass_reassign_doctor_wizard_views.xml',
        'wizard/odoo_school_hr_hospital_visit_report_wizard_views.xml',
        'wizard/odoo_school_hr_hospital_disease_report_wizard_views.xml',
        'data/doctor_category_data.xml',
        'views/odoo_school_hr_hospital_menu_views.xml',
        'views/odoo_school_hr_hospital_doctor_views.xml',
        'views/odoo_school_hr_hospital_patient_views.xml',
        'views/odoo_school_hr_hospital_disease_views.xml',
        'views/odoo_school_hr_hospital_visit_views.xml',
        'views/odoo_school_hr_hospital_doctor_category_views.xml',
        'views/odoo_school_hr_hospital_doctor_history_views.xml',
        'report/odoo_school_hr_hospital_doctor_report.xml',
    ],

    'demo': [
        'demo/doctor_demo.xml',
        'demo/patient_demo.xml',
        'demo/doctor_history_demo.xml',
        'demo/disease_demo.xml',
        'demo/visit_demo.xml',
    ],

    'images': ['static/description/icon.png'],

    'installable': True,
    'application': False,
    'auto_install': False,
}
