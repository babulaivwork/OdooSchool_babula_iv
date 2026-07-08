import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class OSHrHospitalDoctor(models.Model):
    _name = 'os.hr.hospital.doctor'
    _description = 'Doctor'

    name = fields.Char()
    active = fields.Boolean(default=True)
    specialty = fields.Char()
    phone = fields.Char()
    email = fields.Char()
    notes = fields.Text()

    visit_ids = fields.One2many(
        comodel_name='os.hr.hospital.visit',
        inverse_name='doctor_id',
        string='Visits',
    )
