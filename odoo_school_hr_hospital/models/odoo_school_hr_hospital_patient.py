import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class OSHrHospitalPatient(models.Model):
    _name = 'os.hr.hospital.patient'
    _description = 'Patient'

    name = fields.Char()
    active = fields.Boolean(default=True)
    description = fields.Text()
    birth_date = fields.Date()
    phone = fields.Char()
    email = fields.Char()
    address = fields.Char()
    notes = fields.Text()

    visit_ids = fields.One2many(
        comodel_name='os.hr.hospital.visit',
        inverse_name='patient_id',
        string='Visits',
    )
