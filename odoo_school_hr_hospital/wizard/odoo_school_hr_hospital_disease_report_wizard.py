from datetime import datetime

from pytz import UTC

from odoo import Command, api, fields, models
from odoo.exceptions import ValidationError
from odoo.fields import Domain


class OSHrHospitalDiseaseReportWizard(models.TransientModel):
    """Build a disease-grouped visit report from selected filters."""

    _name = 'os.hr.hospital.disease.report.wizard'
    _description = 'Disease Report Wizard'

    doctor_ids = fields.Many2many(
        comodel_name='os.hr.hospital.doctor',
        string='Doctors',
    )
    disease_ids = fields.Many2many(
        comodel_name='os.hr.hospital.disease',
        string='Diseases',
    )
    date_from = fields.Date(
        string='Start of Period',
        required=True,
        default=lambda self: fields.Date.start_of(
            fields.Date.context_today(self),
            'month',
        ),
    )
    date_to = fields.Date(
        string='End of Period',
        required=True,
        default=lambda self: fields.Date.end_of(
            fields.Date.context_today(self),
            'month',
        ),
    )

    @api.model
    def default_get(self, fields_list):
        """Prefill doctors from the records that opened the wizard.

        :param list[str] fields_list: Fields whose defaults are requested.
        :return: Default field values for the wizard.
        :rtype: dict
        """
        values = super().default_get(fields_list)
        active_model = self.env.context.get('active_model')
        active_ids = self.env.context.get('active_ids') or []
        if not active_ids and self.env.context.get('active_id'):
            active_ids = [self.env.context['active_id']]

        if active_model == 'os.hr.hospital.doctor' and 'doctor_ids' in fields_list:
            doctors = self.env[active_model].browse(active_ids).exists()
            if doctors:
                values['doctor_ids'] = [Command.set(doctors.ids)]

        return values

    @api.constrains('date_from', 'date_to')
    def _check_period(self):
        """Ensure that the report period has a valid chronological order.

        :raises ValidationError: If the start date is later than the end date.
        """
        for wizard in self:
            if wizard.date_from and wizard.date_to and wizard.date_from > wizard.date_to:
                raise ValidationError(self.env._('The start of the period cannot be later than the end of the period.'))

    def _to_utc_midnight(self, date_value):
        """Convert local midnight for a date to a naive UTC datetime.

        :param date date_value: Date to convert.
        :return: Corresponding UTC datetime without timezone information.
        :rtype: datetime
        """
        local_midnight = self.env.tz.localize(datetime.combine(date_value, datetime.min.time()))
        return local_midnight.astimezone(UTC).replace(tzinfo=None)

    def action_generate_report(self):
        """Open visits matching the period, doctor, and disease filters.

        The resulting records are grouped by disease.

        :return: Window action displaying the matching visits.
        :rtype: dict
        """
        self.ensure_one()
        date_to_exclusive = fields.Date.add(self.date_to, days=1)
        domain = Domain(
            'scheduled_datetime',
            '>=',
            self._to_utc_midnight(self.date_from),
        )
        domain &= Domain(
            'scheduled_datetime',
            '<',
            self._to_utc_midnight(date_to_exclusive),
        )

        if self.doctor_ids:
            domain &= Domain('doctor_id', 'in', self.doctor_ids.ids)
        if self.disease_ids:
            domain &= Domain('disease_id', 'child_of', self.disease_ids.ids)

        action = self.env['ir.actions.act_window']._for_xml_id(
            'odoo_school_hr_hospital.os_hr_hospital_action_visit_window'
        )
        action['domain'] = domain
        action['context'] = {'group_by': 'disease_id'}
        return action
