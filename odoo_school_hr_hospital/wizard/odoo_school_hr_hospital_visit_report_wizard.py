from odoo import Command, api, fields, models
from odoo.exceptions import ValidationError
from odoo.fields import Domain


class OSHrHospitalVisitReportWizard(models.TransientModel):
    _name = 'os.hr.hospital.visit.report.wizard'
    _description = 'Visit Report Wizard'

    doctor_ids = fields.Many2many(
        comodel_name='os.hr.hospital.doctor',
        string='Doctors',
    )
    patient_ids = fields.Many2many(
        comodel_name='os.hr.hospital.patient',
        string='Patients',
    )
    date_from = fields.Date(string='Start of Period')
    date_to = fields.Date(string='End of Period')
    only_completed = fields.Boolean(string='Only Completed Visits')
    disease_id = fields.Many2one(
        comodel_name='os.hr.hospital.disease',
        string='Disease',
    )

    @api.model
    def default_get(self, fields_list):
        values = super().default_get(fields_list)
        active_model = self.env.context.get('active_model')
        active_ids = self.env.context.get('active_ids') or []
        if not active_ids and self.env.context.get('active_id'):
            active_ids = [self.env.context['active_id']]

        if active_model == 'os.hr.hospital.doctor' and 'doctor_ids' in fields_list:
            doctors = self.env[active_model].browse(active_ids).exists()
            if doctors:
                values['doctor_ids'] = [Command.set(doctors.ids)]
        elif active_model == 'os.hr.hospital.patient' and 'patient_ids' in fields_list:
            patients = self.env[active_model].browse(active_ids).exists()
            if patients:
                values['patient_ids'] = [Command.set(patients.ids)]

        return values

    @api.constrains('date_from', 'date_to')
    def _check_period(self):
        for wizard in self:
            if wizard.date_from and wizard.date_to and wizard.date_from > wizard.date_to:
                raise ValidationError('The start of the period cannot be later than the end of the period.')

    def action_generate_report(self):
        self.ensure_one()
        domain = Domain.TRUE

        if self.doctor_ids:
            domain &= Domain('doctor_id', 'in', self.doctor_ids.ids)
        if self.patient_ids:
            domain &= Domain('patient_id', 'in', self.patient_ids.ids)
        if self.date_from:
            domain &= Domain('scheduled_datetime', '>=', self.date_from)
        if self.date_to:
            domain &= Domain(
                'scheduled_datetime',
                '<',
                fields.Date.add(self.date_to, days=1),
            )
        if self.only_completed:
            domain &= Domain('state', '=', 'completed')
        if self.disease_id:
            domain &= Domain('disease_id', 'child_of', self.disease_id.id)

        action = self.env['ir.actions.act_window']._for_xml_id(
            'odoo_school_hr_hospital.os_hr_hospital_action_visit_window'
        )
        action['domain'] = domain
        return action
