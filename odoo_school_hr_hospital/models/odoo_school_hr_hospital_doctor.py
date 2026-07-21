from odoo import api, fields, models
from odoo.exceptions import ValidationError


class OSHrHospitalDoctor(models.Model):
    _name = 'os.hr.hospital.doctor'
    _inherit = 'os.hr.hospital.medic.info'
    _description = 'Doctor'

    name = fields.Char()
    active = fields.Boolean(default=True)
    specialty = fields.Char()
    phone = fields.Char()
    email = fields.Char()
    notes = fields.Text()
    category_id = fields.Many2one(
        comodel_name='os.hr.hospital.doctor.category',
        string='Qualification',
        ondelete='set null',
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='System User',
    )
    is_intern = fields.Boolean(
        string='Is Intern',
        compute='_compute_is_intern',
        store=True,
    )
    mentor_id = fields.Many2one(
        comodel_name='os.hr.hospital.doctor',
        string='Mentor',
    )

    visit_ids = fields.One2many(
        comodel_name='os.hr.hospital.visit',
        inverse_name='doctor_id',
        string='Visits',
    )

    @api.depends('category_id')
    def _compute_is_intern(self):
        intern_category = self.env.ref(
            'odoo_school_hr_hospital.doctor_category_intern',
            raise_if_not_found=False,
        )
        for doctor in self:
            doctor.is_intern = doctor.category_id == intern_category

    @api.constrains('mentor_id', 'category_id')
    def _check_mentor_is_not_intern(self):
        intern_category = self.env.ref(
            'odoo_school_hr_hospital.doctor_category_intern',
            raise_if_not_found=False,
        )
        for doctor in self:
            if doctor.mentor_id.is_intern:
                raise ValidationError('An intern doctor cannot be selected as a mentor.')

            if doctor.category_id != intern_category:
                continue

            mentored_doctor = self.with_context(active_test=False).search(
                [('mentor_id', '=', doctor.id)],
                limit=1,
            )
            if mentored_doctor:
                raise ValidationError(
                    'A doctor assigned as a mentor cannot be changed to an intern.',
                )
