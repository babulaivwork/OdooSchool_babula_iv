from odoo.tests import TransactionCase


class OSHrHospitalCommon(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.doctor = cls.env['os.hr.hospital.doctor'].create(
            {
                'name': 'Test Doctor',
            }
        )
        cls.patient = cls.env['os.hr.hospital.patient'].create(
            {
                'name': 'Test Patient',
            }
        )
