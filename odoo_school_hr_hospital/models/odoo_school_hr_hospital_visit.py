from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class OSHrHospitalVisit(models.Model):
    """Represent a scheduled, completed, or cancelled patient visit."""

    _name = 'os.hr.hospital.visit'
    _description = 'Patient Visit'

    name = fields.Char(
        required=True,
        default=lambda self: self.env._('New Visit'),
    )
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
    disease_visit_count = fields.Integer(
        string='Visits',
        compute='_compute_disease_visit_count',
    )
    scheduled_datetime = fields.Datetime(
        string='Scheduled Date and Time',
        default=fields.Datetime.now,
        required=True,
    )
    actual_datetime = fields.Datetime(string='Actual Date and Time')

    @api.depends(
        'disease_id',
        'disease_id.visit_ids',
        'disease_id.visit_ids.active',
    )
    def _compute_disease_visit_count(self):
        """Compute the number of active visits for each selected disease."""
        visit_count_by_disease = dict(
            self.env['os.hr.hospital.visit']._read_group(
                domain=[('disease_id', 'in', self.disease_id.ids)],
                groupby=['disease_id'],
                aggregates=['__count'],
            )
        )
        for visit in self:
            visit.disease_visit_count = visit_count_by_disease.get(visit.disease_id, 0)

    def action_open_disease_visits(self):
        """Return an action showing visits for the selected disease.

        :return: Window action filtered by the visit's disease.
        :rtype: dict
        """
        self.ensure_one()
        action = self.env['ir.actions.act_window']._for_xml_id(
            'odoo_school_hr_hospital.os_hr_hospital_action_visit_window'
        )
        action['context'] = {}
        action['domain'] = [('disease_id', '=', self.disease_id.id)]
        return action

    def write(self, vals):
        """Update visits while enforcing completed-visit restrictions.

        :param dict vals: Field values to update.
        :return: ``True`` when the records are updated successfully.
        :rtype: bool
        :raises UserError: If the update archives a completed visit or changes
            its assigned doctor or dates.
        """
        completed_visits = self.filtered(lambda visit: visit.state == 'completed')
        archived_completed_visits = self.filtered(
            lambda visit: (
                (visit.state == 'completed' or vals.get('state') == 'completed')
                and not vals.get('active', visit.active)
            )
        )
        if archived_completed_visits:
            raise UserError(self.env._('Completed visits cannot be archived.'))

        protected_fields = {
            'doctor_id',
            'scheduled_datetime',
            'actual_datetime',
        }
        if completed_visits and protected_fields.intersection(vals):
            raise UserError(self.env._('The doctor and dates of a completed visit cannot be changed.'))

        return super().write(vals)

    @api.constrains('state', 'active')
    def _check_completed_visit_is_active(self):
        """Ensure that completed visits remain active.

        :raises ValidationError: If a completed visit is archived.
        """
        for visit in self:
            if visit.state == 'completed' and not visit.active:
                raise ValidationError(self.env._('Completed visits cannot be archived.'))

    @api.ondelete(at_uninstall=False)
    def _unlink_if_completed(self):
        """Prevent non-administrators from deleting completed visits.

        :raises UserError: If a non-administrator tries to delete a completed
            visit.
        """
        is_hospital_administrator = self.env.user.has_group(
            'odoo_school_hr_hospital.os_hr_hospital_group_administrator'
        )
        if not is_hospital_administrator and any(visit.state == 'completed' for visit in self):
            raise UserError(self.env._('Completed visits cannot be deleted.'))
