from odoo import fields, models


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

    visit_ids = fields.One2many(
        comodel_name='os.hr.hospital.visit',
        inverse_name='patient_id',
        string='Visits',
    )
