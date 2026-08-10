from odoo.tests import TransactionCase


class OSHrHospitalCommon(TransactionCase):
    """Provide shared hospital records for model tests."""

    @classmethod
    def setUpClass(cls):
        """Create reusable doctor and patient fixtures for the test class."""
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
