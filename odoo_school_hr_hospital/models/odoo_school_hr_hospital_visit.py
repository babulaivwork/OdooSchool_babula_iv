from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class OSHrHospitalVisit(models.Model):
    _name = 'os.hr.hospital.visit'
    _description = 'Patient Visit'

    name = fields.Char(required=True, default='New Visit')
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ('scheduled', 'Scheduled'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
        ],
        string='Status',
        required=True,
        default='scheduled',
    )
    summary = fields.Html()
    description = fields.Text()
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
    disease_id = fields.Many2one(
        comodel_name='os.hr.hospital.disease',
        string='Disease',
    )
    scheduled_datetime = fields.Datetime(
        string='Scheduled Date and Time',
        default=fields.Datetime.now,
        required=True,
    )
    actual_datetime = fields.Datetime(string='Actual Date and Time')

    def write(self, vals):
        completed_visits = self.filtered(lambda visit: visit.state == 'completed')
        archived_completed_visits = self.filtered(
            lambda visit: (
                (visit.state == 'completed' or vals.get('state') == 'completed')
                and not vals.get('active', visit.active)
            )
        )
        if archived_completed_visits:
            raise UserError('Completed visits cannot be archived.')

        protected_fields = {
            'doctor_id',
            'scheduled_datetime',
            'actual_datetime',
        }
        if completed_visits and protected_fields.intersection(vals):
            raise UserError('The doctor and dates of a completed visit cannot be changed.')

        return super().write(vals)

    @api.constrains('state', 'active')
    def _check_completed_visit_is_active(self):
        for visit in self:
            if visit.state == 'completed' and not visit.active:
                raise ValidationError('Completed visits cannot be archived.')

    @api.ondelete(at_uninstall=False)
    def _unlink_if_completed(self):
        if any(visit.state == 'completed' for visit in self):
            raise UserError('Completed visits cannot be deleted.')
