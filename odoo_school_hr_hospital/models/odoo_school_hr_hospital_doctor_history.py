from odoo import api, fields, models
from odoo.exceptions import ValidationError


class OSHrHospitalDoctorHistory(models.Model):
    _name = 'os.hr.hospital.doctor.history'
    _description = 'Personal Doctor History'

    patient_id = fields.Many2one(
        comodel_name='os.hr.hospital.patient',
        string='Patient',
        required=True,
    )
    doctor_id = fields.Many2one(
        comodel_name='os.hr.hospital.doctor',
        string='Doctor',
        required=True,
    )
    assignment_date = fields.Date(
        string='Assignment Date',
        required=True,
        default=fields.Date.today,
    )
    change_date = fields.Date(string='Doctor Change Date')
    active = fields.Boolean(default=True)

    @api.depends(
        'patient_id.name',
        'doctor_id.name',
        'doctor_id.category_id.name',
        'assignment_date',
    )
    def _compute_display_name(self):
        for history in self:
            patient_name = history.patient_id.name or ''
            doctor_name = history.doctor_id.name or ''
            category_name = history.doctor_id.category_id.name or ''
            assignment_date = fields.Date.to_string(history.assignment_date)

            if patient_name and doctor_name:
                display_name = f'{patient_name} - {doctor_name}'
                if category_name:
                    display_name += f' ({category_name})'
            else:
                display_name = patient_name or doctor_name or 'New Doctor History'
                if category_name:
                    display_name += f' ({category_name})'
            if assignment_date:
                display_name += f' {assignment_date}'

            history.display_name = display_name

    @api.onchange('assignment_date', 'change_date')
    def _onchange_dates(self):
        if self.assignment_date and self.change_date and self.change_date < self.assignment_date:
            return {
                'warning': {
                    'title': 'Invalid Dates',
                    'message': 'The doctor change date cannot be earlier than the assignment date.',
                },
            }
        return None

    @api.constrains('assignment_date', 'change_date')
    def _check_dates(self):
        for history in self:
            if history.assignment_date and history.change_date and history.change_date < history.assignment_date:
                raise ValidationError('The doctor change date cannot be earlier than the assignment date.')
