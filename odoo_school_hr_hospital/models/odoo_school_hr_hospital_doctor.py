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
    intern_ids = fields.One2many(
        comodel_name='os.hr.hospital.doctor',
        inverse_name='mentor_id',
        string='Interns',
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
    def _check_mentor_assignment(self):
        intern_category = self.env.ref(
            'odoo_school_hr_hospital.doctor_category_intern',
            raise_if_not_found=False,
        )
        for doctor in self:
            if doctor.mentor_id and doctor.category_id != intern_category:
                raise ValidationError(
                    self.env._('Only an intern doctor can have a mentor.')
                )

            if doctor.mentor_id.is_intern:
                raise ValidationError(
                    self.env._('An intern doctor cannot be selected as a mentor.')
                )

            if doctor.category_id != intern_category:
                continue

            mentored_doctor = self.with_context(active_test=False).search(
                [('mentor_id', '=', doctor.id)],
                limit=1,
            )
            if mentored_doctor:
                raise ValidationError(
                    self.env._(
                        'A doctor assigned as a mentor cannot be changed to an intern.'
                    )
                )

    def action_create_visit(self):
        self.ensure_one()
        visit_form = self.env.ref('odoo_school_hr_hospital.os_hr_hospital_visit_form')
        return {
            'name': self.env._('Create Visit'),
            'type': 'ir.actions.act_window',
            'res_model': 'os.hr.hospital.visit',
            'view_mode': 'form',
            'views': [(visit_form.id, 'form')],
            'target': 'new',
            'context': {
                'default_doctor_id': self.id,
            },
        }
