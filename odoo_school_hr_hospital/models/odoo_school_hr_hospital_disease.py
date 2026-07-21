from odoo import fields, models


class OSHrHospitalDisease(models.Model):
    _name = 'os.hr.hospital.disease'
    _description = 'Disease'

    name = fields.Char()
    active = fields.Boolean(default=True)
    description = fields.Text()
    code = fields.Char()

    visit_ids = fields.One2many(
        comodel_name='os.hr.hospital.visit',
        inverse_name='disease_id',
        string='Visits',
    )
