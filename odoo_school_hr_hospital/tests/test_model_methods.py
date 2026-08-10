from datetime import date, timedelta

from odoo import fields
from odoo.exceptions import UserError, ValidationError

from .common import OSHrHospitalCommon


class TestOSHrHospitalModelMethods(OSHrHospitalCommon):
    """Test hospital computations and business constraints."""

    def test_compute_age(self):
        """Verify age computation with and without a birth date."""
        today = fields.Date.context_today(self.patient)
        self.patient.birth_date = date(today.year - 30, 1, 1)

        self.assertEqual(self.patient.age, 30)

        self.patient.birth_date = False

        self.assertEqual(self.patient.age, 0)

    def test_check_parent_id(self):
        """Verify that cyclic disease hierarchies are rejected."""
        parent_disease = self.env['os.hr.hospital.disease'].create(
            {
                'name': 'Parent Disease',
            }
        )
        child_disease = self.env['os.hr.hospital.disease'].create(
            {
                'name': 'Child Disease',
                'parent_id': parent_disease.id,
            }
        )

        self.assertEqual(child_disease.parent_id, parent_disease)

        with self.assertRaises(ValidationError), self.cr.savepoint():
            parent_disease.parent_id = child_disease

    def test_visit_write(self):
        """Verify editable and protected fields on completed visits."""
        visit = self.env['os.hr.hospital.visit'].create(
            {
                'name': 'Completed Test Visit',
                'patient_id': self.patient.id,
                'doctor_id': self.doctor.id,
                'state': 'completed',
            }
        )

        self.assertTrue(visit.write({'description': 'Updated description'}))
        self.assertEqual(visit.description, 'Updated description')

        new_scheduled_datetime = visit.scheduled_datetime + timedelta(hours=1)
        with self.assertRaises(UserError), self.cr.savepoint():
            visit.write({'scheduled_datetime': new_scheduled_datetime})

        with self.assertRaises(UserError), self.cr.savepoint():
            visit.write({'active': False})
