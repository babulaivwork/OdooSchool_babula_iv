from odoo import api, fields, models


class OSHrHospitalPatient(models.Model):
    _name = 'os.hr.hospital.patient'
    _inherit = 'os.hr.hospital.medic.info'
    _description = 'Patient'

    name = fields.Char()
    active = fields.Boolean(default=True)
    description = fields.Text()
    phone = fields.Char()
    email = fields.Char()
    address = fields.Char()
    notes = fields.Text()
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='System User',
        copy=False,
        index=True,
        ondelete='set null',
    )
    personal_doctor_id = fields.Many2one(
        comodel_name='os.hr.hospital.doctor',
        string='Personal Doctor',
    )
    doctor_history_ids = fields.One2many(
        comodel_name='os.hr.hospital.doctor.history',
        inverse_name='patient_id',
        string='Personal Doctor History',
    )
    insurance_policy_number = fields.Char(
        string='Insurance Policy Number',
        size=20,
    )

    visit_ids = fields.One2many(
        comodel_name='os.hr.hospital.visit',
        inverse_name='patient_id',
        string='Visits',
    )
    visit_count = fields.Integer(
        string='Visits',
        compute='_compute_visit_count',
    )

    @api.depends('visit_ids', 'visit_ids.active')
    def _compute_visit_count(self):
        visit_count_by_patient = dict(
            self.env['os.hr.hospital.visit']._read_group(
                domain=[('patient_id', 'in', self.ids)],
                groupby=['patient_id'],
                aggregates=['__count'],
            )
        )
        for patient in self:
            patient.visit_count = visit_count_by_patient.get(patient, 0)

    def action_open_visits(self):
        self.ensure_one()
        action = self.env['ir.actions.act_window']._for_xml_id(
            'odoo_school_hr_hospital.os_hr_hospital_action_visit_window'
        )
        action['context'] = {}
        action['domain'] = [('patient_id', '=', self.id)]
        return action

    def action_create_visit(self):
        self.ensure_one()
        visit_form = self.env.ref('odoo_school_hr_hospital.os_hr_hospital_visit_form')
        return {
            'name': 'Create Visit',
            'type': 'ir.actions.act_window',
            'res_model': 'os.hr.hospital.visit',
            'view_mode': 'form',
            'views': [(visit_form.id, 'form')],
            'target': 'new',
            'context': {
                'default_patient_id': self.id,
                'default_doctor_id': self.personal_doctor_id.id or False,
            },
        }
