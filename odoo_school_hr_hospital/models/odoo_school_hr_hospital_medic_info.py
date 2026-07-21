from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class OSHrHospitalMedicInfo(models.AbstractModel):
    _name = 'os.hr.hospital.medic.info'
    _description = 'Medical Information'

    blood_group = fields.Selection(
        selection=[
            ('o_positive', 'O(I) Rh+'),
            ('o_negative', 'O(I) Rh-'),
            ('a_positive', 'A(II) Rh+'),
            ('a_negative', 'A(II) Rh-'),
            ('b_positive', 'B(III) Rh+'),
            ('b_negative', 'B(III) Rh-'),
            ('ab_positive', 'AB(IV) Rh+'),
            ('ab_negative', 'AB(IV) Rh-'),
        ],
        string='Blood Group',
    )
    gender = fields.Selection(
        selection=[
            ('male', 'Male'),
            ('female', 'Female'),
        ],
    )
    birth_date = fields.Date()
    age = fields.Integer(compute='_compute_age')

    @api.depends('birth_date')
    def _compute_age(self):
        today = fields.Date.context_today(self)
        for medic_info in self:
            if medic_info.birth_date:
                medic_info.age = relativedelta(today, medic_info.birth_date).years
            else:
                medic_info.age = 0
