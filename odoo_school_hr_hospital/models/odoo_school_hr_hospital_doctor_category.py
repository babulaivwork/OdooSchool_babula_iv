from odoo import fields, models


class OSHrHospitalDoctorCategory(models.Model):
    """Represent a doctor qualification category."""

    _name = 'os.hr.hospital.doctor.category'
    _description = 'Doctor Qualification'
    _order = 'sequence, id'

    name = fields.Char(translate=True)
    sequence = fields.Integer()
    doctor_ids = fields.One2many(
        comodel_name='os.hr.hospital.doctor',
        inverse_name='category_id',
        string='Doctors',
    )

    _name_unique = models.Constraint(
        'UNIQUE(name)',
        'A doctor qualification with this name already exists.',
    )
